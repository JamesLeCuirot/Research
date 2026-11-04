"""Check a paper's references.bib against Crossref (DOIs) and arXiv (IDs), and \\cite keys against the bib.

Usage (from the repo root):
  uv run --no-project --with bibtexparser==1.4.3 --with requests python papers/_build/check_bib.py papers/03-from-rsp-to-sms

Reports, per entry: DOI/arXiv found?, title similarity, first-author surname match, year match,
and volume/pages match where Crossref has them. Also lists cite keys missing from the bib and bib
entries never cited. Exit code 1 if any hard mismatch is found.
"""
import re, sys, json, difflib, time, pathlib
import bibtexparser, requests

folder = pathlib.Path(sys.argv[1])
bib = bibtexparser.load(open(folder / "references.bib", encoding="utf-8"),
                        parser=bibtexparser.bparser.BibTexParser(common_strings=True))
tex = (folder / "paper.tex").read_text(encoding="utf-8")
cited = set(k.strip() for grp in re.findall(r"\\cite[a-z]*\*?(?:\[[^\]]*\])?\{([^}]*)\}", tex) for k in grp.split(","))
keys = {e["ID"] for e in bib.entries}

def norm(s):
    s = re.sub(r"[{}\\$]", "", s or "").lower()
    s = re.sub(r"\s+", " ", re.sub(r"[^a-z0-9 ]", " ", s))
    return s.strip()

def surname(bibauthor):
    first = (bibauthor or "").split(" and ")[0].strip().strip("{}")
    return norm(first.split(",")[0] if "," in first else first.split(" ")[-1])

problems = 0
rows = []
H = {"User-Agent": "papers-bib-check/1.0 (research tooling)"}
for e in bib.entries:
    key, title = e["ID"], e.get("title", "")
    doi = e.get("doi", "").strip()
    m = re.search(r"(\d{4}\.\d{4,5})", " ".join([e.get("eprint", ""), e.get("url", ""), e.get("howpublished", ""), e.get("note", ""), e.get("journal", "")]))
    arx = m.group(1) if m else ""
    status, detail = "unchecked", ""
    try:
        if doi:
            r = requests.get(f"https://api.crossref.org/works/{doi}", headers=H, timeout=30)
            if r.status_code != 200:
                status, detail = "DOI-NOT-FOUND", f"HTTP {r.status_code}"
            else:
                w = r.json()["message"]
                t = (w.get("title") or [""])[0]
                sim = difflib.SequenceMatcher(None, norm(t), norm(title)).ratio()
                fa = norm((w.get("author") or [{}])[0].get("family", "")) if w.get("author") else ""
                yr = str((w.get("issued", {}).get("date-parts") or [[None]])[0][0])
                issues = []
                if sim < 0.85: issues.append(f"title sim {sim:.2f}: CR='{t[:80]}'")
                if fa and surname(e.get("author", "")) and fa != surname(e.get("author", "")): issues.append(f"1st author CR={fa} bib={surname(e.get('author',''))}")
                if yr and e.get("year") and yr != e.get("year") and not (yr.isdigit() and abs(int(yr) - int(e["year"][:4])) <= 1): issues.append(f"year CR={yr} bib={e.get('year')}")
                for f_bib, f_cr in (("volume", "volume"), ("pages", "page")):
                    if e.get(f_bib) and w.get(f_cr) and norm(e[f_bib]).replace(" ", "") != norm(w[f_cr]).replace(" ", ""):
                        issues.append(f"{f_bib} CR={w[f_cr]} bib={e[f_bib]}")
                status = "OK" if not issues else "CHECK"
                detail = "; ".join(issues)
        elif arx:
            r = requests.get(f"https://export.arxiv.org/api/query?id_list={arx}", headers=H, timeout=30)
            ent = r.text.split("<entry>")[1] if "<entry>" in r.text else ""
            t = re.sub(r"\s+", " ", (re.search(r"<title>(.*?)</title>", ent, re.S) or [None, ""])[1] if ent else "")
            if not t:
                status, detail = "ARXIV-NOT-FOUND", arx
            else:
                sim = difflib.SequenceMatcher(None, norm(t), norm(title)).ratio()
                names = re.findall(r"<name>(.*?)</name>", ent)
                fa = norm(names[0].split(" ")[-1]) if names else ""
                yr = (re.search(r"<published>(\d{4})", ent) or [None, ""])[1]
                issues = []
                if sim < 0.85: issues.append(f"title sim {sim:.2f}: arXiv='{t[:80]}'")
                if fa and surname(e.get("author", "")) and fa != surname(e.get("author", "")): issues.append(f"1st author arXiv={fa} bib={surname(e.get('author',''))}")
                if yr and e.get("year") and yr != e.get("year"): issues.append(f"year arXiv v1={yr} bib={e.get('year')} (ok if a later published version is cited)")
                status = "OK" if not issues else "CHECK"
                detail = "; ".join(issues)
        else:
            status = "NO-ID"
            detail = "no DOI or arXiv ID: verify manually against sources.md"
    except Exception as ex:  # network etc.
        status, detail = "ERROR", str(ex)[:120]
    if status in ("DOI-NOT-FOUND", "ARXIV-NOT-FOUND"): problems += 1
    rows.append((key, status, detail))
    time.sleep(0.3)

print(f"# Bibliography check: {folder.name}\n")
print("| key | status | detail |\n|---|---|---|")
for k, s, d in rows:
    print(f"| {k} | {s} | {d} |")
missing = sorted(cited - keys)
unused = sorted(keys - cited)
print(f"\nCite keys missing from bib: {missing or 'none'}")
print(f"Bib entries never cited: {unused or 'none'}")
problems += len(missing)
sys.exit(1 if problems else 0)
