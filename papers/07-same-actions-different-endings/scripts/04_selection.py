"""Step 4: merge the screening logs into one, and list the selected cases.

Checks: the quotas after deviations D1 and D2, exactly one pilot in each of A and C, the
draw ranks run in order with no gaps, and no possible duplicate event across categories
(same date, place and aircraft type among the selected reports).
"""
import csv
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
SCREEN = ROOT / "data" / "screening"
RAW = ROOT / "data" / "raw" / "ASRS_DBOnline.csv"
QUOTA = {"A": 8, "B": 6, "C": 20, "D": 8, "E": 0, "F": 6}  # main cases, after D1, D2 and D7 (exclusions)
EXCLUDED = {r["acn"] for r in csv.DictReader((pathlib.Path(__file__).resolve().parents[1] / "data" / "exclusions.csv")
                                             .open(encoding="utf-8"))}


def main():
    rows = []
    for cat in "ABCDEF":
        with (SCREEN / f"log_{cat}.csv").open(newline="", encoding="utf-8") as f:
            log = list(csv.DictReader(f))
        ranks = [int(r["draw_rank"]) for r in log]
        assert ranks == list(range(1, len(ranks) + 1)), f"{cat}: draw ranks not consecutive from 1"
        rows += log

    with (ROOT / "data" / "screening-log.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

    with RAW.open(newline="", encoding="utf-8-sig", errors="replace") as f:
        raw = {r[0].strip(): r for r in list(csv.reader(f))[2:] if len(r) > 120 and r[0].strip()}

    selected, problems = [], []
    for cat in "ABCDEF":
        q = [r for r in rows if r["category"] == cat and r["decision"] == "qualifies" and r["acn"] not in EXCLUDED]
        main_ = [r for r in q if r["pilot"] != "yes"]
        pilot = [r for r in q if r["pilot"] == "yes"]
        if len(main_) != QUOTA[cat]:
            problems.append(f"{cat}: {len(main_)} main cases, expected {QUOTA[cat]}")
        if len(pilot) != (1 if cat in "AC" else 0):
            problems.append(f"{cat}: {len(pilot)} pilot cases")
        for r in q:
            x = raw[r["acn"]]
            selected.append({"set": "pilot" if r["pilot"] == "yes" else "main", "category": cat,
                             "draw_rank": r["draw_rank"], "acn": r["acn"],
                             "date": x[1], "locale": x[3], "aircraft": x[18],
                             "primary_problem": x[119], "screening_reason": r["reason"]})

    keys = {}
    for s in selected:
        k = (s["date"], s["locale"], s["aircraft"])
        keys.setdefault(k, []).append(s["acn"])
    dups = {k: v for k, v in keys.items() if len(v) > 1}

    with (ROOT / "data" / "selected-cases.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(selected[0]))
        w.writeheader()
        w.writerows(selected)

    n_main = sum(s["set"] == "main" for s in selected)
    print(f"screened in total: {len(rows)}; selected: {n_main} main + "
          f"{sum(s['set'] == 'pilot' for s in selected)} pilot")
    for cat in "ABCDEF":
        print(f"  {cat}: {sum(s['category'] == cat and s['set'] == 'main' for s in selected)} main")
    pp = {}
    for s in selected:
        if s["set"] == "main":
            pp[s["primary_problem"]] = pp.get(s["primary_problem"], 0) + 1
    print("primary problem among main cases:", pp)
    print("possible duplicates (same date, place and aircraft):", dups or "none")
    if problems:
        print("PROBLEMS:", *problems, sep="\n  ")
        sys.exit(1)


if __name__ == "__main__":
    main()
