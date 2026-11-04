"""Build cases/review-side-by-side.html: for each case, the original NASA report beside the case
text the AI will see, with the condenser's notes underneath. Flagged cases come first, each with
its question from review-flags.md.
"""
import csv
import html
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[1]


def flags():
    q = {}
    for line in (ROOT / "cases" / "review-flags.md").read_text(encoding="utf-8").splitlines():
        if line.startswith("| ") and not line.startswith("| ACN") and not line.startswith("|---"):
            cells = [c.strip() for c in line.strip("|").split("|")]
            for acn in re.findall(r"\d{7}", cells[0]):
                q[acn] = re.sub(r"\*\*(.*?)\*\*", r"\1", cells[2])
    return q


def source_sections(acn):
    txt = (ROOT / "cases" / "sources" / f"{acn}.txt").read_text(encoding="utf-8")
    parts = []
    for label in ("Narrative 1", "Callback 1", "Narrative 2", "Callback 2", "Synopsis"):
        m = re.search(rf"^{label}: (.*?)(?=^\w[\w ]*: |\Z)", txt, re.S | re.M)
        if m:
            parts.append((label, m.group(1).strip()))
    meta = [l for l in txt.splitlines()[2:] if re.match(r"^(Flight phase|Aircraft 1|Mission|Reporter 1 function|"
                                                       r"Reporter 1 experience|Anomaly|Primary problem):", l)]
    return meta, parts


def esc(s):
    return html.escape(s).replace("\n\n", "<br><br>").replace("\n", "<br>")


def main():
    cases = [c for c in json.loads((ROOT / "cases" / "cases.json").read_text(encoding="utf-8")) if c["set"] == "main"]
    drafts = {p.stem: json.loads(p.read_text(encoding="utf-8")) for p in (ROOT / "cases" / "drafts").glob("*.json")}
    fq = flags()
    cases.sort(key=lambda c: (c["acn"] not in fq, c["case_id"]))
    blocks = []
    for c in cases:
        meta, parts = source_sections(c["acn"])
        flag = (f'<div class="flag"><b>Question for you:</b> {html.escape(fq[c["acn"]])}</div>'
                if c["acn"] in fq else "")
        src = "".join(f"<h4>{html.escape(l)}</h4><p>{esc(t)}</p>" for l, t in parts)
        metah = "".join(f"<div class='meta'>{html.escape(m)}</div>" for m in meta)
        blocks.append(f"""
<section id="{c['case_id']}" class="case{' flagged' if c['acn'] in fq else ''}">
  <h2>{c['case_id']} <span class="sub">category {c['category']} · ACN {c['acn']} · {html.escape(c['primary_problem'])}
  · {len(c['shared_text'].split())} words{' · FLAGGED' if c['acn'] in fq else ''}</span></h2>
  {flag}
  <div class="cols">
    <div class="col src"><h3>Original NASA report</h3>{metah}{src}</div>
    <div class="col case"><h3>What the AI sees</h3><p>{esc(c['shared_text'])}</p>
      <h4>Safe ending</h4><p>{esc(c['safe_outcome'])}</p>
      <h4>Bad ending ({html.escape(c['bad_ending_variant'])})</h4><p>{esc(c['bad_outcome'])}</p></div>
  </div>
  <details open><summary>What was cut, moved or changed (condenser's notes)</summary><p>{esc(drafts[c['acn']]['notes'])}</p></details>
  <div class="checks">Faithful? · Neutral wording? · Reads right to a pilot (and bad ending plausible)? · Nothing before the ending gives the real outcome away?</div>
</section>""")
    nav = " ".join(f"<a href='#{c['case_id']}' class='{'fl' if c['acn'] in fq else ''}'>{c['case_id']}</a>" for c in cases)
    page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Case review</title><style>
:root{{--bg:#fbfaf7;--fg:#1d1d1b;--muted:#6b6a65;--card:#ffffff;--line:#e3e1da;--src:#f3f1ea;--flag:#fff4d6;--flagline:#e0b84a;--accent:#2b5c8a}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#161615;--fg:#e9e7e1;--muted:#a3a19a;--card:#1f1f1d;--line:#34332f;--src:#262522;--flag:#3a3220;--flagline:#a8862e;--accent:#8fb6dc}}}}
:root[data-theme="dark"]{{--bg:#161615;--fg:#e9e7e1;--muted:#a3a19a;--card:#1f1f1d;--line:#34332f;--src:#262522;--flag:#3a3220;--flagline:#a8862e;--accent:#8fb6dc}}
body{{margin:0;background:var(--bg);color:var(--fg);font:15px/1.55 system-ui,-apple-system,Segoe UI,sans-serif}}
main{{max-width:1200px;margin:0 auto;padding:16px}}
header p{{color:var(--muted);max-width:75ch}}
nav{{position:sticky;top:0;background:var(--bg);padding:8px 0;border-bottom:1px solid var(--line);z-index:2;line-height:2}}
nav a{{color:var(--accent);margin-right:6px;text-decoration:none;font-size:13px}} nav a.fl{{font-weight:700}}
.case{{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:16px;margin:20px 0}}
.case.flagged{{border-left:5px solid var(--flagline)}}
h2{{margin:0 0 8px;font-size:20px}} .sub{{font-size:13px;color:var(--muted);font-weight:400}}
h3{{margin:0 0 8px;font-size:14px;text-transform:uppercase;letter-spacing:.04em;color:var(--muted)}}
h4{{margin:12px 0 4px;font-size:13px;color:var(--muted)}}
.flag{{background:var(--flag);border:1px solid var(--flagline);border-radius:8px;padding:10px 12px;margin:0 0 12px}}
.cols{{display:grid;grid-template-columns:1fr 1fr;gap:16px}}
.col{{min-width:0}} .col.src{{background:var(--src);border-radius:8px;padding:12px;font-size:14px}}
.meta{{font-size:12px;color:var(--muted)}}
details{{margin-top:12px;font-size:14px}} summary{{cursor:pointer;color:var(--accent)}}
.checks{{margin-top:10px;font-size:12px;color:var(--muted)}}
@media (max-width:760px){{.cols{{grid-template-columns:1fr}}}}
</style></head><body><main>
<header><h1>Case review: original report beside what the AI sees</h1>
<p>Flagged cases come first (bold in the list, gold edge), each with its question. For every case, check that it is faithful to the report,
that the wording is neutral, that it reads right to a pilot with a plausible bad ending, and that nothing before the ending gives the real
outcome away. Don't judge blame or polish the style. Send back the case ID and what's wrong.</p></header>
<nav>{nav}</nav>{''.join(blocks)}</main></body></html>"""
    (ROOT / "cases" / "review-side-by-side.html").write_text(page, encoding="utf-8")
    print(f"wrote cases/review-side-by-side.html ({len(cases)} cases, {sum(c['acn'] in fq for c in cases)} flagged)")


if __name__ == "__main__":
    main()
