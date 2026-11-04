"""Step 1: sort the exported reports into categories and make the random draw order.

This implements protocol/01-sampling-rule.md, sections 2 and 3. It reads only the
coded fields (ACN, Anomaly, Result, Primary Problem), never the narratives.

Implementation notes, fixed before any narrative was read:
- Anomaly codes are matched as whole codes. The field holds codes separated by
  semicolons, and each code is compared after trimming spaces. "Starts with" is
  used where the rule names a whole event type, such as "Deviation - Altitude".
- Each category gets its own fresh random.Random(20261001). The order therefore
  does not depend on the order in which categories are processed.

Output: data/draw-order.csv, with one row per eligible report: its category, its
position in the draw order, ACN, primary problem and anomaly codes.
"""
import csv
import pathlib
import random

ROOT = pathlib.Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "ASRS_DBOnline.csv"
OUT = ROOT / "data" / "draw-order.csv"
SEED = 20261001

COL_ACN, COL_ANOMALY, COL_RESULT, COL_PRIMARY = 0, 112, 117, 119

CATEGORIES = [  # (code, name, test); earlier wins when a report matches several
    ("A", "Unstabilised approach",
     lambda c: "Inflight Event / Encounter Unstabilized Approach" in c),
    ("B", "Runway incursion or landing without clearance",
     lambda c: "Ground Incursion Runway" in c
     or "Deviation / Discrepancy - Procedural Landing Without Clearance" in c),
    ("C", "Altitude deviation",
     lambda c: any(x.startswith("Deviation - Altitude") for x in c)),
    ("D", "Track or heading deviation",
     lambda c: any(x.startswith("Deviation - Track / Heading") for x in c)),
    ("E", "Airspace violation",
     lambda c: any(x.startswith("Airspace Violation") for x in c)),
    ("F", "Other deviation from an ATC clearance or restriction",
     lambda c: any(x.startswith("Deviation - Speed") for x in c)
     or "Deviation / Discrepancy - Procedural Clearance" in c),
]


def main():
    with RAW.open(newline="", encoding="utf-8-sig", errors="replace") as f:
        rows = list(csv.reader(f))
    data = [r for r in rows[2:] if len(r) > COL_PRIMARY and r[COL_ACN].strip()]

    pools = {code: [] for code, _, _ in CATEGORIES}
    excluded_result, uncategorised = 0, 0
    for r in data:
        result = r[COL_RESULT]
        if "Aircraft Damaged" in result or "Physical Injury" in result:
            excluded_result += 1
            continue
        codes = [x.strip() for x in r[COL_ANOMALY].split(";") if x.strip()]
        for code, _, test in CATEGORIES:
            if test(codes):
                pools[code].append(r)
                break
        else:
            uncategorised += 1

    out_rows = []
    for code, name, _ in CATEGORIES:
        pool = sorted(pools[code], key=lambda r: int(r[COL_ACN]))
        random.Random(SEED).shuffle(pool)
        for rank, r in enumerate(pool, start=1):
            out_rows.append({
                "category": code,
                "category_name": name,
                "draw_rank": rank,
                "acn": r[COL_ACN].strip(),
                "primary_problem": r[COL_PRIMARY].strip(),
                "anomaly": r[COL_ANOMALY].strip(),
            })

    with OUT.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(out_rows[0]))
        w.writeheader()
        w.writerows(out_rows)

    print(f"reports in export:            {len(data)}")
    print(f"excluded (damage or injury):  {excluded_result}")
    print(f"in none of the six categories: {uncategorised}")
    for code, name, _ in CATEGORIES:
        print(f"  {code}  {len(pools[code]):4}  {name}")
    print(f"wrote {OUT.relative_to(ROOT)} ({len(out_rows)} rows)")


if __name__ == "__main__":
    main()
