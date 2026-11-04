"""Build the paper's PDF from its Markdown source.

Usage:
  python paper/build_pdf.py                       builds paper/preprint-v1.md
  python paper/build_pdf.py paper/preprint-v2.md  builds another version

Converts the Markdown subset the paper uses (headings, paragraphs, bold, italic, code, nested
lists, tables, block quotes, figures, rules) to one HTML file with the figures inlined, then prints
it to PDF with headless Microsoft Edge. A line ending in a backslash is a line break, as in CommonMark. No third-party Python packages. [AUTHOR] and [CHECK] notes
are highlighted so they can't be missed in review.

Writes paper/build/<name>.html and paper/<name>.pdf.
"""
import html
import pathlib
import re
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
EDGE = pathlib.Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")

CSS = """
@page { size: A4; margin: 22mm 20mm 22mm 20mm;
  @bottom-center { content: counter(page); font: 9pt Georgia, serif; color: #555; } }
@page draft { @top-right { content: "Draft for review, not for circulation"; font: 8pt Georgia, serif; color: #a33; } }
body.draft { page: draft; }
body { font: 10.5pt/1.45 Georgia, 'Times New Roman', serif; color: #111; }
h1 { font: bold 17pt/1.25 Georgia, serif; margin: 0 0 10pt; }
h2 { font: bold 13pt Georgia, serif; margin: 18pt 0 6pt; break-after: avoid; }
h3 { font: bold 11pt Georgia, serif; margin: 12pt 0 4pt; break-after: avoid; }
p { margin: 0 0 7pt; text-align: justify; hyphens: auto; }
ul, ol { margin: 0 0 7pt; padding-left: 18pt; }
li { margin: 0 0 2pt; }
li > ul, li > ol { margin: 2pt 0 2pt; }
table { border-collapse: collapse; width: 100%; margin: 6pt 0 4pt; font-size: 9pt; line-height: 1.3; break-inside: avoid; }
th, td { border-top: 0.6pt solid #999; border-bottom: 0.6pt solid #999; padding: 3pt 4pt; text-align: left; vertical-align: top; }
th { font-weight: bold; border-top: 1.2pt solid #111; }
blockquote { margin: 4pt 0 8pt 10pt; padding-left: 8pt; border-left: 2pt solid #ccc; font-size: 9.5pt; }
blockquote p { text-align: left; margin-bottom: 4pt; }
code { font: 9pt Consolas, monospace; }
hr { border: 0; border-top: 0.6pt solid #bbb; margin: 12pt 0; }
figure { margin: 8pt 0 10pt; break-inside: avoid; }
figure svg { width: 100%; height: auto; }
.note { background: #fff3b0; }
"""


def inline(text):
    t = html.escape(text, quote=False)
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", t)
    t = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', t)
    t = re.sub(r"(?<![\"'>=])(https?://[^\s<]+[^\s<.,;)])", r'<a href="\1">\1</a>', t)
    t = re.sub(r"(\[(?:AUTHOR|CHECK)[^\]]*\])", r'<span class="note">\1</span>', t)
    return t


def parse_list(lines, i):
    """Parse a (possibly nested) list starting at lines[i]; return (html, next index)."""
    m = re.match(r"^(\s*)([-*]|\d+\.)\s", lines[i])
    indent, ordered = len(m.group(1)), m.group(2)[0].isdigit()
    out = ["<ol>" if ordered else "<ul>"]
    while i < len(lines):
        m = re.match(r"^(\s*)([-*]|\d+\.)\s+(.*)$", lines[i])
        if not m or len(m.group(1)) < indent:
            break
        if len(m.group(1)) > indent:
            sub, i = parse_list(lines, i)
            out[-1] = out[-1][:-5] + sub + "</li>"
            continue
        item = [m.group(3)]
        i += 1
        while i < len(lines) and lines[i].strip() and not re.match(r"^\s*([-*]|\d+\.)\s", lines[i]):
            item.append(lines[i].strip())
            i += 1
        out.append(f"<li>{inline(' '.join(item))}</li>")
        while i < len(lines) and not lines[i].strip() and i + 1 < len(lines) \
                and re.match(r"^(\s*)([-*]|\d+\.)\s", lines[i + 1]) \
                and len(re.match(r"^(\s*)", lines[i + 1]).group(1)) >= indent:
            i += 1
    out.append("</ol>" if ordered else "</ul>")
    return "".join(out), i


def figure(src, md_path):
    p = (md_path.parent / src).resolve()
    svg = p.read_text(encoding="utf-8")
    svg = re.sub(r'\swidth="\d+"\sheight="\d+"', "", svg, count=1)
    return f"<figure>{svg}</figure>"


def convert(md, md_path):
    lines = md.splitlines()
    out, i = [], 0
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
        elif line.startswith("#"):
            n = len(line) - len(line.lstrip("#"))
            out.append(f"<h{n}>{inline(line[n:].strip())}</h{n}>")
            i += 1
        elif line.strip() == "---":
            out.append("<hr>")
            i += 1
        elif m := re.match(r"^!\[[^\]]*\]\(([^)]+)\)\s*$", line):
            out.append(figure(m.group(1), md_path))
            i += 1
        elif line.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            head, body = rows[0], [r for r in rows[2:]]
            t = ["<table><thead><tr>" + "".join(f"<th>{inline(c)}</th>" for c in head) + "</tr></thead><tbody>"]
            t += ["<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>" for r in body]
            out.append("".join(t) + "</tbody></table>")
        elif line.startswith(">"):
            paras, cur = [], []
            while i < len(lines) and lines[i].startswith(">"):
                s = lines[i][1:].strip()
                if s:
                    cur.append(inline(s))
                elif cur:
                    paras.append("<br>".join(cur))
                    cur = []
                i += 1
            if cur:
                paras.append("<br>".join(cur))
            out.append("<blockquote>" + "".join(f"<p>{p}</p>" for p in paras) + "</blockquote>")
        elif re.match(r"^\s*([-*]|\d+\.)\s", line):
            h, i = parse_list(lines, i)
            out.append(h)
        else:
            para = [line.strip()]
            i += 1
            while i < len(lines) and lines[i].strip() and not re.match(r"^(#|\||>|!\[|---|\s*([-*]|\d+\.)\s)", lines[i]):
                para.append(lines[i].strip())
                i += 1
            # A line ending in a backslash is a line break. The marker is set off by
            # spaces so that a link at the end of the line can't swallow it.
            joined = " ".join(ln[:-1].rstrip() + " \x00BR\x00" if ln.endswith("\\") else ln for ln in para)
            out.append("<p>" + inline(joined).replace(" \x00BR\x00 ", "<br>") + "</p>")
    return "\n".join(out)


def main():
    md_path = pathlib.Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else HERE / "preprint-v1.md"
    md = md_path.read_text(encoding="utf-8")
    title = re.search(r"^# (.+)$", md, re.M).group(1)
    draft = "DRAFT" in md[:400]
    body = convert(md, md_path)
    doc = (f"<!doctype html><html lang='en-GB'><head><meta charset='utf-8'><title>{html.escape(title)}</title>"
           f"<style>{CSS}</style></head><body{' class=draft' if draft else ''}>"
           + body + "</body></html>")
    build = HERE / "build"
    build.mkdir(exist_ok=True)
    html_path = build / f"{md_path.stem}.html"
    html_path.write_text(doc, encoding="utf-8")
    pdf_path = HERE / f"same-actions-different-endings-{md_path.stem}.pdf"
    subprocess.run([str(EDGE), "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                    f"--print-to-pdf={pdf_path}", html_path.as_uri()], check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=120)
    print(f"wrote {html_path.relative_to(HERE.parent)} and {pdf_path.relative_to(HERE.parent)}")


if __name__ == "__main__":
    main()
