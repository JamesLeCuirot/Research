"""The Coding Desk: a browser page for hand-coding the calibration traces.

Run:
    uv run afacs-coding-tool build            # writes data/coding_tool.html (not committed: it holds trace text)
    uv run afacs-coding-tool import <folder>  # copies saved codings into annotations/human/calibration_sheet.csv

The page shows the 30 calibration traces exactly as the blind renders do (no
MAST labels, benchmark information hidden), with a coding form whose codes come
from the current codebook. It is published as a private Claude artifact; the
codings James enters are saved in the artifact's own database. Claude exports
that database to a folder of JSON files (one per trace), and `import` writes
them into the coding sheet, so the CSV in the repo stays the record of the
coding and git keeps its history.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from afacs import paths
from afacs.ingest import load_traces
from afacs.parsers import BENCHMARK_INFO
from afacs.render import HIDDEN_BENCHMARK_TEXT
from afacs.schema import CODING_FIELDS, CURRENT_CODEBOOK, load_codebook_codes, normalise_row, validate_coding

TEMPLATE = Path(__file__).parent / "templates" / "coding_tool.html"
OUTPUT = paths.DATA / "coding_tool.html"
LIST_FIELDS = ("l4_codes", "l3_codes", "l2_codes", "l1_codes")


def read_sheet() -> list[dict]:
    with open(paths.CALIBRATION_SHEET) as f:
        return list(csv.DictReader(f))


def build() -> None:
    traces = {t["uid"]: t for t in load_traces()}
    items = []
    for row in read_sheet():
        t = traces[row["uid"]]
        items.append({
            "cal_id": row["cal_id"], "uid": t["uid"], "framework": t["framework"], "model": t["model"],
            "benchmark": t["benchmark"], "n_steps": t["n_steps"], "approx_tokens": t["approx_tokens"],
            "steps": [
                {"n": s["n"], "agent": s["agent"], "kind": s["kind"],
                 "text": HIDDEN_BENCHMARK_TEXT if s["kind"] == BENCHMARK_INFO else s["text"]}
                for s in t["steps"]
            ],
        })
    data = {
        "codebook_version": CURRENT_CODEBOOK,
        "codes": [{"code": c, "text": d} for c, d in load_codebook_codes(CURRENT_CODEBOOK).items()],
        "traces": items,
    }
    # "</" inside the JSON would end the <script> tag early, so escape it.
    blob = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    html = TEMPLATE.read_text().replace("/*__DATA__*/", blob)
    OUTPUT.write_text(html)
    print(f"wrote {OUTPUT.relative_to(paths.ROOT)} ({len(items)} traces, {OUTPUT.stat().st_size / 1e6:.1f} MB)")


def load_export(folder: Path) -> dict[str, dict]:
    """Read one JSON file per saved coding (as exported from the artifact database)."""
    out = {}
    for f in sorted(folder.rglob("*.json")):
        doc = json.loads(f.read_text())
        if isinstance(doc.get("data"), dict):  # tolerate a {data: ..., version: ...} wrapper
            doc = doc["data"]
        if doc.get("cal_id"):
            out[doc["cal_id"]] = doc
    return out


def import_codings(folder: Path) -> None:
    saved = load_export(folder)
    rows = read_sheet()
    codes = load_codebook_codes(CURRENT_CODEBOOK)
    updated = 0
    for row in rows:
        doc = saved.get(row["cal_id"])
        if not doc or doc.get("uid") != row["uid"]:
            continue
        for field in CODING_FIELDS:
            value = doc.get(field, "")
            row[field] = ";".join(value) if field in LIST_FIELDS and isinstance(value, list) else ("" if value is None else str(value))
        row["minutes_spent"] = str(doc.get("minutes_spent", "") or "")
        row["status"] = doc.get("status", "")
        updated += 1
        errors, warnings = validate_coding(normalise_row(row), codes)
        for e in errors:
            print(f"  {row['cal_id']} ERROR   {e}")
        for w in warnings:
            print(f"  {row['cal_id']} warning {w}")
    fieldnames = list(rows[0].keys())
    if "status" not in fieldnames:
        fieldnames.append("status")
    with open(paths.CALIBRATION_SHEET, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for row in rows:
            w.writerow({k: row.get(k, "") for k in fieldnames})
    done = sum(1 for r in rows if r.get("status") == "done")
    print(f"Imported {updated} coding(s) into {paths.CALIBRATION_SHEET.relative_to(paths.ROOT)}; {done} marked done.")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="command", required=True)
    sub.add_parser("build")
    p = sub.add_parser("import")
    p.add_argument("folder", type=Path, help="folder of exported JSON codings (one file per trace)")
    args = ap.parse_args()
    if args.command == "build":
        build()
    else:
        import_codings(args.folder)


if __name__ == "__main__":
    main()
