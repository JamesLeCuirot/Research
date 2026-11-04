"""Step 6: build cases/cases.json, the file the run reads, and cases/review-pack.md, for James.

Case IDs are neutral, so the model never sees an ACN or a category name:
- main cases S01–S48, numbered in a seeded random order;
- pilot cases P1–P2;
- control cases K1–K6, added from cases/controls.json once James has approved them.
"""
import csv
import json
import pathlib
import random

ROOT = pathlib.Path(__file__).resolve().parents[1]
SEED = 20261003


def main():
    sel = list(csv.DictReader((ROOT / "data" / "selected-cases.csv").open(encoding="utf-8")))
    drafts = {p.stem: json.loads(p.read_text(encoding="utf-8")) for p in (ROOT / "cases" / "drafts").glob("*.json")}
    main_ = sorted([s for s in sel if s["set"] == "main"], key=lambda s: int(s["acn"]))
    random.Random(SEED).shuffle(main_)
    pilots = sorted([s for s in sel if s["set"] == "pilot"], key=lambda s: s["category"])

    cases = []
    for i, s in enumerate(main_, 1):
        cases.append(("S%02d" % i, "main", s))
    for i, s in enumerate(pilots, 1):
        cases.append((f"P{i}", "pilot", s))

    out = []
    for cid, set_, s in cases:
        d = drafts[s["acn"]]
        out.append({"case_id": cid, "set": set_, "acn": s["acn"], "category": s["category"],
                    "primary_problem": s["primary_problem"], "shared_text": d["shared_text"],
                    "safe_outcome": d["safe_outcome"], "bad_outcome": d["bad_outcome"],
                    "bad_ending_variant": d["bad_ending_variant"], "bracket_fill": d["bracket_fill"]})
    controls = ROOT / "cases" / "controls.json"
    if controls.exists():
        out += json.loads(controls.read_text(encoding="utf-8"))
    (ROOT / "cases" / "cases.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = ["# Review pack: the 48 main cases", "",
             "*For James's realism read, 1 Oct 2026. Each case shows the shared text, the safe ending, the bad-ending "
             "variant, and the condenser's notes. Mark anything that isn't faithful to the report, reads as slanted, "
             "or wouldn't ring true to a line pilot. The ACN lets you open the original in `cases/sources/<ACN>.txt`.*",
             "", "*The bad endings are the frozen wording, so only the variant and the bracket fill are shown.*", ""]
    for c in out:
        if c["set"] != "main":
            continue
        d = drafts[c["acn"]]
        lines += [f"## {c['case_id']}: category {c['category']}, ACN {c['acn']}, {c['primary_problem']}, "
                  f"{len(c['shared_text'].split())} words", "",
                  *[f"> {p}" if p.strip() else ">" for p in c["shared_text"].split("\n")], "",
                  f"**Safe ending:** {c['safe_outcome']}", "",
                  f"**Bad ending:** {c['bad_ending_variant']} ({c['bracket_fill']})", "",
                  f"<details><summary>Condenser's notes</summary>\n\n{d['notes']}\n\n</details>", "", "---", ""]
    (ROOT / "cases" / "review-pack.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"cases.json: {len(out)} cases ({sum(c['set'] == 'main' for c in out)} main, "
          f"{sum(c['set'] == 'pilot' for c in out)} pilot, {sum(c['set'] == 'control' for c in out)} control)")
    print("review-pack.md written")


if __name__ == "__main__":
    main()
