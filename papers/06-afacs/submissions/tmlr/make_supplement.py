"""Build the anonymised supplementary ZIP for the AFACS TMLR submission.

Copies the code, codebook, prompts, encoded AI codings, results, figures and
documentation into build/supplement/, replaces the author's name with "the
investigator", drops files written only for the author (the plain-English guide
and explainer) and the full reference library, checks that no identifying string
is left, and writes build/supplement.zip. Traces are not included: they contain
benchmark questions whose maintainers ask that they not be reposted, and the
pipeline recreates them from MAST's pinned revision.

    python3 papers/06-afacs/submissions/tmlr/make_supplement.py
"""
import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
PAPER = HERE.parents[1]
OUT = HERE / "build" / "supplement"
ZIP = HERE / "build" / "supplement.zip"

COPY = ["pyproject.toml", "uv.lock", ".env.example", "src", "scripts", "tests", "codebook", "prompts",
        "docs", "results", "figures", "annotations/llm/public", "annotations/human", "data/README.md"]
DROP = ["docs/GUIDE.md", "docs/explainer.html", "docs/references.bib", "docs/CODING_GUIDE.md", "docs/related_work.md"]
FORBIDDEN = re.compile(r"cuirot|citadel|jameslec|github\.com/james|@citadelaero|/home/user|papers/06-|\bjames\b|claude\.ai/code/session|session_01|claude\.ai/artifact|\bshown to him\b|\bhe changed\b", re.I)
TEXT = {".md", ".py", ".txt", ".json", ".jsonl", ".csv", ".toml", ".html", ".example", ".sha256", ".lock"}

README = """# Supplementary material

Anonymised materials for "Extending AI-Agent Incident Analysis to Multi-Agent Systems: AFACS, an
HFACS-Based Framework, and an Audit of Public Traces".

| Path | Contents |
|---|---|
| `codebook/` | The AFACS codebook: v0, v1 (used in the pilot) and v1.1 (v1 without the stated Ezell pairing) |
| `prompts/` | The annotator prompts (v1 used in the pilot) |
| `src/afacs/`, `scripts/`, `tests/` | The pipeline: ingest and audit of MAST, rendering and blinding, sampling, annotation, quote checking, agreement and analysis. Python 3.11+, managed with uv (`pyproject.toml`, `uv.lock`) |
| `annotations/llm/public/` | Every AI coding from the three bulk runs and two checks, with benchmark text in quotes encoded (`src/afacs/protect.py` decodes them) |
| `annotations/human/` | The blank calibration coding sheet and the SHA-256 fingerprint of the hidden calibration key |
| `results/` | Analysis and agreement outputs and the pilot summary |
| `docs/` | The data audit, the information audit, the cross-walk to Ezell et al., the documentation (design) check and the coding guide |
| `figures/` | The figures |
| `data/README.md` | How the traces are recreated from MAST's pinned revision |
| `version_history.txt` | Commit times (UTC) of the calibration key fingerprint, the calibration sheet, the codebooks, the annotator prompts and the AI codings, without commit identifiers, so the order of events can be checked |

Traces are not included, because they contain benchmark questions whose maintainers ask that they not be
reposted. `uv run afacs-ingest` downloads MAST (`mcemri/MAST-Data`, revision `95118ac`, CC BY 4.0) and
recreates them. Code is released under the MIT licence.
"""


def anonymise(text: str) -> str:
    text = re.sub(r"https://claude\.ai/code/session_\w+", "[session link withheld]", text)
    text = text.replace("They were shown to him in plain English on 3 November; he changed only 5.6.",
                        "They were reviewed in plain English on 3 November; only 5.6 was changed.")
    text = text.replace("the 30 traces James hand-codes", "the 30 calibration traces for independent human coders")
    text = re.sub(r"James Le Cuirot", "the investigator", text)
    text = re.sub(r"\bJames's\b", "the investigator's", text)
    text = re.sub(r"\bJames\b", "the investigator", text)
    text = text.replace("papers/06-afacs/", "")
    return text


KEY_FILES = ["annotations/human/calibration_key.sha256", "annotations/human/calibration_sheet.csv",
             "codebook/v0.md", "codebook/v1.md", "codebook/v1.1.md",
             "prompts/annotator_v0.md", "prompts/annotator_v1.md",
             "annotations/llm/public/sonnet_bulk_r1.jsonl", "annotations/llm/public/opus_bulk_r1.jsonl",
             "annotations/llm/public/sonnet_bulk_r2.jsonl"]


def version_history() -> str:
    """Times of the commits that added or changed each file (moves excluded), across all the folders the
    project has lived in, without identifiers."""
    root = PAPER.parents[1]
    out = ["Times (UTC) of the commits that added or changed each file, oldest first, across every folder the",
           "project has lived in. Commits that only moved the project are excluded. Commit identifiers and",
           "messages are withheld for anonymity.", ""]
    for f in KEY_FILES:
        log = subprocess.run(["git", "-C", str(root), "log", "--find-renames", "--diff-filter=AM", "--date=iso-strict",
                              "--format=%ad", "--", f"*/{f}", f], capture_output=True, text=True).stdout.split()[::-1]
        if log:
            out.append(f + "\n" + "\n".join("    " + d for d in log))
    out.append("")
    out.append("The AI annotator was never run on the 30 calibration traces.")
    return "\n".join(out) + "\n"


def main() -> int:
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    for name in COPY:
        src = PAPER / name
        dst = OUT / name
        dst.parent.mkdir(parents=True, exist_ok=True)
        if src.is_dir():
            shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store", "*.egg-info"))
        elif src.exists():
            shutil.copy2(src, dst)
    for name in DROP:
        p = OUT / name
        if p.exists():
            p.unlink()
    toml = OUT / "pyproject.toml"
    toml.write_text(re.sub(r'authors = \[.*?\]', 'authors = [{ name = "Anonymous" }]', toml.read_text()), encoding="utf-8")
    for path in OUT.rglob("*"):
        if path.is_file() and (path.suffix in TEXT or path.name.startswith(".env")):
            text = path.read_text(encoding="utf-8")
            new = anonymise(text)
            if new != text:
                path.write_text(new, encoding="utf-8")
    (OUT / "README.md").write_text(README, encoding="utf-8")
    (OUT / "version_history.txt").write_text(version_history(), encoding="utf-8")

    problems = []
    for path in OUT.rglob("*"):
        if path.is_file():
            data = path.read_bytes().decode("utf-8", errors="ignore")
            for m in FORBIDDEN.finditer(data):
                problems.append(f"{path.relative_to(OUT)}: {data[max(0, m.start()-40):m.end()+40]!r}")
    if problems:
        print("Identifying strings remain:\n" + "\n".join(problems[:30]), file=sys.stderr)
        return 1

    if ZIP.exists():
        ZIP.unlink()
    with zipfile.ZipFile(ZIP, "w", zipfile.ZIP_DEFLATED) as z:
        for path in sorted(OUT.rglob("*")):
            if path.is_file():
                z.write(path, Path("supplement") / path.relative_to(OUT))
    size = ZIP.stat().st_size / 1e6
    print(f"wrote {ZIP} ({size:.1f} MB); no identifying strings found")
    return 0 if size < 100 else 2


if __name__ == "__main__":
    sys.exit(main())
