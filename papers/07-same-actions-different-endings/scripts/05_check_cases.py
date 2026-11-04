"""Step 5: check every drafted case against the frozen rules.

For each case it checks:
- the JSON shape;
- 150–250 words of shared text (main cases);
- the bad ending matches the frozen wording, with only the brackets filled;
- the safe ending closes with one of the two allowed sentences;
- no he/she, no NASA placeholders, no runway numbers, no likely airport codes;
- no banned judgement words.

It prints one line per problem. It exits non-zero if any hard rule fails.
"""
import csv
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
DRAFTS = ROOT / "cases" / "drafts"

BAD = {
    "A-excursion": r"The aircraft could not be stopped on the remaining runway\. It left the (end|side) of the runway "
                   r"at about 30 knots and came to rest on the grass\. The passengers were evacuated, and two received "
                   r"minor injuries during the evacuation\. The aircraft was slightly damaged\.",
    "B-departing": r"At the same time, another aircraft was beginning its take-off roll on the runway\. Its crew saw "
                   r"(our aircraft|the conflict|this aircraft), rejected the take-off at high speed and stopped about "
                   r"300 feet short of it\. That aircraft's passengers were evacuated because of hot brakes, and two "
                   r"received minor injuries\.",
    "B-landing": r"The landing aircraft's crew saw the conflict late and went around from about 50 feet, passing low "
                 r"over (this aircraft|the runway)\. A flight attendant on the landing aircraft was thrown off balance "
                 r"by the abrupt go-around and received a minor injury\.",
    "LOS": r"Another aircraft was (climbing|descending|crossing) nearby\. Both crews received TCAS resolution "
           r"advisories and followed them, and the aircraft passed about 300 feet vertically and half a mile apart\. "
           r"A flight attendant on this aircraft was thrown against a galley cart during the manoeuvre and received a "
           r"minor injury\.",
}
VARIANT_OK = {"A": {"A-excursion"}, "B": {"B-departing", "B-landing"},
              "C": {"LOS"}, "D": {"LOS"}, "F": {"LOS"}}
SAFE_ENDS = ("There was no conflict with other traffic. No one was hurt and the aircraft was not damaged.",
             "No one was hurt and no aircraft was damaged.")
KEYS = ["acn", "category", "shared_text", "safe_outcome", "bad_outcome", "bad_ending_variant",
        "bracket_fill", "word_count_shared", "notes"]
BANNED = [r"\bhe\b", r"\bshe\b", r"\bhis\b", r"\bher\b", r"\bhim\b", r"\bhers\b", r"\bhimself\b", r"\bherself\b",
          r"ZZZ", r"\bfailed to\b", r"\bmistaken(ly)?\b", r"\bshould have\b", r"\berror\b", r"\bmistakes?\b",
          r"\bcomplacen", r"\bfixat", r"\bfroze\b"]
RUNWAY_NO = r"\b(runway|rwy|taxiway)\s+\d{1,2}[LRC]?\b"
ACRONYMS_OK = {"ATC", "TCAS", "ILS", "FMS", "VNAV", "LNAV", "PAPI", "GPWS", "EGPWS", "MSA", "SID", "STAR", "FAF",
               "RNAV", "RNP", "VOR", "DME", "MCP", "FMA", "MFD", "PFD", "ND", "AP", "ATIS", "VMC", "IMC", "TOGA",
               "RA", "TA", "MDA", "DA", "AGL", "MSL", "QNH", "QNE", "FL", "LOC", "GS", "APU", "CDU", "FCU", "ALT",
               "VS", "FPA", "IAS", "MEL", "NOTAM", "CRM", "SOP", "FOM", "TOD", "TOC", "FPM", "HUD", "ECAM", "EICAS",
               "LVP", "RVR", "PM", "PF", "FO", "CA", "IFR", "VFR", "GA", "DH", "OK", "UTC", "ETA", "FAA",
               "PVOR", "FGC", "TRACON", "ARTCC", "IAF", "IF", "CRJ", "KIAS", "VREF", "VAPP"}


def check(d, is_main):
    hard, soft = [], []
    if list(d) != KEYS:
        hard.append(f"keys {list(d)}")
    st, safe, bad = d.get("shared_text", ""), d.get("safe_outcome", ""), d.get("bad_outcome", "")
    wc = len(st.split())
    if wc != d.get("word_count_shared"):
        soft.append(f"word_count_shared {d.get('word_count_shared')} but counted {wc}")
    if is_main and wc > 250:
        hard.append(f"shared text {wc} words (over 250)")
    elif is_main and wc < 150:
        soft.append(f"shared text {wc} words, under the 150 guide (allowed under D5 if the report is short)")
    for label in ("The flight.", "The crew.", "What happened."):
        if label not in st:
            hard.append(f"missing paragraph label '{label}'")
    v = d.get("bad_ending_variant")
    if v not in VARIANT_OK.get(d.get("category"), set()):
        hard.append(f"variant {v} not allowed for category {d.get('category')}")
    elif not re.fullmatch(BAD[v], bad.strip()):
        hard.append("bad ending is not the frozen wording")
    if not safe.strip().endswith(SAFE_ENDS):
        hard.append("safe ending does not close with an allowed sentence")
    text = " ".join((st, safe))
    for pat in BANNED:
        if re.search(pat, text, re.I if pat != "ZZZ" else 0):
            hard.append(f"banned word or placeholder: {pat}")
    if re.search(RUNWAY_NO, text, re.I):
        hard.append("runway or taxiway number present")
    caps = {w for w in re.findall(r"\b[A-Z]{3,4}\b", text) if w not in ACRONYMS_OK}
    if caps:
        soft.append(f"possible codes, check by hand: {sorted(caps)}")
    return hard, soft


def main():
    sel = {r["acn"]: r for r in csv.DictReader((ROOT / "data" / "selected-cases.csv").open(encoding="utf-8"))}
    files = sorted(DRAFTS.glob("*.json"))
    n_hard = 0
    seen = set()
    for f in files:
        d = json.loads(f.read_text(encoding="utf-8"))
        acn = d.get("acn")
        seen.add(acn)
        is_main = sel.get(acn, {}).get("set") == "main"
        hard, soft = check(d, is_main)
        n_hard += len(hard)
        for p in hard:
            print(f"HARD  {f.stem}: {p}")
        for p in soft:
            print(f"soft  {f.stem}: {p}")
    missing = [a for a in sel if a not in seen]
    print(f"\nchecked {len(files)} drafts; hard problems {n_hard}; still to write: {len(missing)} {missing}")
    sys.exit(1 if n_hard else 0)


if __name__ == "__main__":
    main()
