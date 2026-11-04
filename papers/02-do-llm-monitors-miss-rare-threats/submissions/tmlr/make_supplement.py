"""Build the anonymised supplementary ZIP for the TMLR submission.

Copies the pre-registration, code, data, results and figures of paper 02 into
build/supplement/, removes the author line, withholds commit identifiers and
repository paths, adds a neutral README, checks that no identifying string is
left, and writes build/supplement.zip. Run from anywhere:

    python3 papers/02-do-llm-monitors-miss-rare-threats/submissions/tmlr/make_supplement.py
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

COPY = ["PREREGISTRATION.md", "code", "data", "results", "figures"]
# Strings that must not appear anywhere in the supplement.
FORBIDDEN = re.compile(r"cuirot|citadel|jameslec|github\.com|@citadelaero|/home/user|papers/02-|papers/_build|paper 02|papers 01|rare threats are missed|\.\./AUDIT\.md", re.I)

README = """# Supplementary material

Anonymised materials for "Do LLM Monitors Miss Rare Threats? A Pre-registered Test of the
Low-Prevalence Effect".

| Path | Contents |
|---|---|
| `PREREGISTRATION.md` | The pre-registered design, with its dated clarifications (Section 9). Commit identifiers are withheld for anonymity. |
| `code/` | Item generation and verification, monitor runs, the registered analysis and the post hoc analyses. `code/README.md` explains how to reproduce each step. |
| `data/` | MBPP download record and problems, generator outputs, verification records, the 419 verified item pairs (`items.jsonl`), the pools and the main-experiment design. |
| `results/` | Every raw monitor output (`monitor_raw.jsonl`, `monitor_attempts.jsonl`), the flat judgement table (`judgments.csv`), the analysis outputs (`analysis.json`, `RESULTS.md`, `RESULTS_numbers.md`), calibration and cost records. |
| `figures/` | The figures in the paper. |

**Who is who in these files.** "The research engineer" (or "the engineer") is the AI coding agent
(a Claude model) that implemented the pipeline and ran the study under the investigator's direction; "the
author" or "lead author" is the investigator. `version_history.txt` lists the version-control commits
that touched these materials during the study, with times (UTC) and files; commit identifiers are
withheld for anonymity.

Item pairs derive from MBPP (Austin et al., 2021), released under CC BY 4.0, and are released under the
same licence with attribution. Code is released under the MIT licence.

To rerun the registered analysis from the raw outputs (Python 3.11+ with numpy, scipy, pandas and
statsmodels): `python code/analyse.py`.
"""


def anonymise(text: str) -> str:
    text = re.sub(r"^\*\*Author:\*\*.*\n", "", text, flags=re.M)
    text = text.replace("Rare Threats Are Missed Threats", "Do LLM Monitors Miss Rare Threats?")
    text = re.sub(r" ?\(paper 02\)", "", text)
    text = text.replace("(`../AUDIT.md`, ", "(independent audit, not included; ")
    text = text.replace('sys.path.insert(0, "papers/_build")                 # house style (run from the repository root)\n', "")
    text = text.replace('sys.path.insert(0, str(ROOT.parent / "_build"))     # same folder, independent of the working directory',
                        'sys.path.insert(0, str(Path(__file__).resolve().parent))  # palette.py is shipped beside this script')
    text = text.replace("`papers/_build/palette.py`", "`code/palette.py`")
    text = text.replace('sys.path.insert(0, "papers/_build"); ', "")
    text = re.sub(r"`[0-9a-f]{7}`", "`[commit withheld]`", text)
    text = text.replace("from the repository root: ", "from the folder above `code/`: ")
    text = text.replace("papers/02-do-llm-monitors-miss-rare-threats/", "")
    return text


def version_history() -> str:
    """Commit times and files of the study's materials, up to the end of the study, without identifiers.

    The study folder was renamed after data collection, so both of its paths are searched."""
    root = PAPER.parents[1]
    folders = [PAPER.relative_to(root).as_posix(), "papers/02-rare-threats-are-missed-threats"]
    log = subprocess.run(
        ["git", "-C", str(root), "log", "--reverse", "--date=iso-strict", "--until=2026-11-04T06:00:00Z",
         "--format=@@%ad", "--name-only", "--", *folders],
        capture_output=True, text=True, check=True).stdout
    out = ["Version-control commits that touched the study's materials, oldest first (UTC).",
           "Commit identifiers and messages are withheld for anonymity. Paths are relative to the supplement.", ""]
    for block in log.split("@@")[1:]:
        lines = [l for l in block.strip().splitlines() if l.strip()]
        when, files = lines[0], []
        for l in lines[1:]:
            for f in folders:
                if l.startswith(f + "/"):
                    files.append(l[len(f) + 1:])
        files = [f for f in files if not f.startswith(("submissions/", "journal/", "paper.", "NOTES", "README", "AUDIT", "sources", "references"))]
        if files:
            out.append(when)
            out += ["    " + f for f in files[:40]] + (["    ... and %d more files" % (len(files) - 40)] if len(files) > 40 else [])
    return "\n".join(out) + "\n"


def main() -> int:
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    for name in COPY:
        src = PAPER / name
        if src.is_dir():
            shutil.copytree(src, OUT / name, ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store"))
        else:
            shutil.copy2(src, OUT / name)
    palette = PAPER.parent / "_build" / "palette.py"
    if palette.exists():
        shutil.copy2(palette, OUT / "code" / "palette.py")
    for path in OUT.rglob("*"):
        if path.is_file() and path.suffix in {".md", ".py", ".txt", ".json", ".jsonl", ".csv"}:
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
        print("Identifying strings remain:\n" + "\n".join(problems[:20]), file=sys.stderr)
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
