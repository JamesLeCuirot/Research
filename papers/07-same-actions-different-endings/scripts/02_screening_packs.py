"""Step 2: write one screening pack per category, listing its reports in draw order.

Each pack holds the fields needed to apply the screening criteria: the narratives,
the synopsis, the callback, the flight phase, the aircraft and the reporter's
function and experience. The screener reads the pack from the top and stops once
the quota is met.
"""
import csv
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "ASRS_DBOnline.csv"
ORDER = ROOT / "data" / "draw-order.csv"
OUTDIR = ROOT / "data" / "screening"

FIELDS = {  # label: column index in the ASRS export
    "Date": 1, "Local time": 2, "Locale": 3, "Flight conditions": 10, "Light": 13,
    "Aircraft 1": 18, "Mission": 23, "Flight phase": 25, "Airspace": 27,
    "Reporter function": 93, "Reporter qualification": 94, "Reporter experience": 95,
    "Human factors": 97, "Anomaly": 112, "Detector": 115, "Result": 117,
    "Contributing factors": 118, "Primary problem": 119,
}


def main():
    with RAW.open(newline="", encoding="utf-8-sig", errors="replace") as f:
        rows = list(csv.reader(f))
    by_acn = {r[0].strip(): r for r in rows[2:] if len(r) > 120 and r[0].strip()}
    with ORDER.open(newline="", encoding="utf-8") as f:
        order = list(csv.DictReader(f))

    OUTDIR.mkdir(parents=True, exist_ok=True)
    for cat in sorted({o["category"] for o in order}):
        items = [o for o in order if o["category"] == cat]
        lines = [f"# Screening pack, category {cat}: {items[0]['category_name']}",
                 f"# {len(items)} reports, in draw order. Read from the top; stop when the quota is met.", ""]
        for o in items:
            r = by_acn[o["acn"]]
            lines.append(f"=== DRAW RANK {o['draw_rank']} | ACN {o['acn']} ===")
            for label, col in FIELDS.items():
                if r[col].strip():
                    lines.append(f"{label}: {r[col].strip()}")
            for label, col in (("Narrative 1", 120), ("Callback 1", 121),
                               ("Narrative 2", 122), ("Callback 2", 123), ("Synopsis", 124)):
                if len(r) > col and r[col].strip():
                    lines.append(f"{label}: {r[col].strip()}")
            lines.append("")
        (OUTDIR / f"pack_{cat}.txt").write_text("\n".join(lines), encoding="utf-8")
        print(f"pack_{cat}.txt: {len(items)} reports")


if __name__ == "__main__":
    main()
