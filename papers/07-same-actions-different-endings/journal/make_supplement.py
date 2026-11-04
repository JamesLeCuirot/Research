"""Build the anonymised supplementary ZIP for the Safety Science submission.

The study's OSF projects are public and name the author, so anonymised OSF view-only links would
not anonymise anything. Instead this copies the study's materials (protocol, pre-registration
text, data, cases, prompts, scripts, results) into build/supplement/, replaces the author's name
and company, removes contact details and commit identifiers, leaves out the preprint itself,
checks for a list of identifying patterns, and writes build/supplement.zip.

    python3 papers/07-same-actions-different-endings/journal/make_supplement.py
"""
import re
import shutil
import sys
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
STUDY = HERE.parent
OUT = HERE / "build" / "supplement"
ZIP = HERE / "build" / "supplement.zip"

COPY = ["protocol", "prereg", "data", "cases", "prompts", "scripts", "results", "check_key.py"]
TEXT = {".md", ".py", ".txt", ".json", ".jsonl", ".csv", ".html", ".toml", ".sha256"}
FORBIDDEN = re.compile(
    r"cuirot|citadel|\bjames\b(?! reason)|investigator reason|orcid|0009-0009|@citadelaero|osf\.io/(s8q24|dhf38)|dhf38|s8q24|"
    r"7260f7b|research-studies|/home/user|jersey", re.I)

README = """# Supplementary material

Anonymised materials for "Same Actions, Different Endings: Outcome Severity Shifts How AI Models
Apply Reason's Culpability Decision Tree to Airline Flight Crews". These are the materials of the
public study record, with the author's name, company and contact details removed. "The
investigator" stands for the author. "Claude" in the protocol and file notes refers to the Claude
models that assisted with preparation under the investigator's direction (manuscript Section 2.3).

| Folder | Contents |
|---|---|
| `protocol/` | Sampling rule, implementation notes, screening guide, case template and endings, prompts and analysis plan, condensing brief, approvals and freeze, deviations log (D1-D11) |
| `prereg/` | The text submitted to the registry |
| `data/` | The ASRS export (NASA public records) with its search criteria and hash, the seeded draw order, every screening decision with its reason, the selected cases and exclusions |
| `cases/` | The 48 main cases, 2 pilot cases and 6 controls as the models saw them, each case's source report, drafts and review files |
| `prompts/` | Reason's tree and the response instructions, exactly as sent |
| `scripts/` | Every step, from the draw to the registered analysis and the paper's tables. Plain Python 3, no third-party packages |
| `results/` | Every model reply (pilot and main), the registered analysis, the descriptive tables, the figures and the simulated data the analysis was tested on |

To reproduce the analysis: `python scripts/07_analyse.py` and `python scripts/09_paper_tables.py`.

Licence: CC BY 4.0 for the materials written for the study. The ASRS reports in `data/raw/` and
`cases/sources/` are NASA's public records.
"""


def anonymise(text: str) -> str:
    text = re.sub(r"[\w.+-]+@citadelaero\.com", "[e-mail withheld]", text)
    text = re.sub(r"https?://(www\.)?citadelaero\.com\S*", "[website withheld]", text)
    text = re.sub(r"https?://osf\.io/\w+/?", "[registry link withheld]", text)
    text = re.sub(r"10\.17605/OSF\.IO/\w+", "[DOI withheld]", text)
    text = re.sub(r"(ORCID[^\n]*?)?0009-0009-6014-1298", "[ORCID withheld]", text)
    text = re.sub(r"\b7260f7b[0-9a-f]*\b", "[commit withheld]", text)
    text = text.replace("James Reason", "\x00REASON\x00")   # the safety scientist, not the author
    text = text.replace("James Le Cuirot", "the investigator")
    text = re.sub(r"\bJames's\b", "the investigator's", text)
    text = re.sub(r"\bJames\b", "the investigator", text)
    text = re.sub(r"CitadelAero( Limited)?", "[company]", text)
    text = re.sub(r",? ?Jersey(, Channel Islands)?", "", text)
    text = text.replace("research-studies", "[study repository]")
    return text.replace("\x00REASON\x00", "James Reason")


def main() -> int:
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    for name in COPY:
        src = STUDY / name
        if src.is_dir():
            shutil.copytree(src, OUT / name, ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".env*"))
        elif src.exists():
            shutil.copy2(src, OUT / name)
    for path in OUT.rglob("*"):
        if path.is_file() and path.suffix in TEXT:
            text = path.read_text(encoding="utf-8", errors="surrogateescape")
            new = anonymise(text)
            if new != text:
                path.write_text(new, encoding="utf-8", errors="surrogateescape")
    (OUT / "README.md").write_text(README, encoding="utf-8")

    problems = []
    for path in OUT.rglob("*"):
        if path.is_file():
            data = path.read_bytes().decode("utf-8", errors="ignore")
            for m in FORBIDDEN.finditer(data):
                problems.append(f"{path.relative_to(OUT)}: {data[max(0, m.start()-40):m.end()+40]!r}")
    if problems:
        print(f"Identifying strings remain ({len(problems)}):\n" + "\n".join(problems[:30]), file=sys.stderr)
        return 1
    if ZIP.exists():
        ZIP.unlink()
    with zipfile.ZipFile(ZIP, "w", zipfile.ZIP_DEFLATED) as z:
        for path in sorted(OUT.rglob("*")):
            if path.is_file():
                z.write(path, Path("supplement") / path.relative_to(OUT))
    print(f"wrote {ZIP} ({ZIP.stat().st_size / 1e6:.1f} MB); no listed identifying pattern found")
    return 0


if __name__ == "__main__":
    sys.exit(main())
