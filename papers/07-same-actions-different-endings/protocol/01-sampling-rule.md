# Sampling rule — fixed before the export

*First written and committed 1 Oct 2026 (`643a50d`), before any ASRS report was exported or read. Revised later on 1 Oct, still before any export or reading, as logged at the end. Changes after the export go in `protocol/deviations.md`.*

## 1. The sampling frame (the ASRS Database Online search)

**Where:** ASRS Database Online (asrs.arc.nasa.gov → ASRS Database Online → Start Search).

**Filters.** Every filter must match. Where a filter has more than one value, any of them may match. The values are exactly as James entered them for the count check on 1 Oct 2026; only the date changes.

| Filter | Value(s) |
|---|---|
| Date of Incident was between | **January 2025 and December 2025** |
| Federal Aviation Regs (FAR) Part was | Part 121 |
| Reporter Function was | Captain, Check Pilot, First Officer, Flight Engineer / Second Officer, Instructor, Pilot Flying, Pilot Not Flying, Relief Pilot, Single Pilot. Drone-only roles are left out |
| Primary Problem was | Human Factors; Procedure |
| Event Type was | All values under: Deviation - Altitude; Deviation - Track / Heading; Ground Incursion; Inflight Event / Encounter; Airspace Violation; Deviation - Speed; Deviation / Discrepancy - Procedural |

**If the search returns fewer than 400 records**, the window widens to July 2024 – December 2025.

**Export:** CSV, all fields. The search date, the record count and the file name go in `data/raw/README.md`.

## 2. Categories, taken from NASA's own coding

Each exported record is placed in a category by its **Anomaly** field, which NASA's analysts code, not us. Where a record matches more than one category, the first in this list wins.

| # | Category | Anomaly field contains | Standard bad ending |
|---|---|---|---|
| A | Unstabilised approach | "Unstabilized Approach" | Runway excursion |
| B | Runway incursion or landing without clearance | "Ground Incursion Runway" or "Landing Without Clearance" | Runway conflict |
| C | Altitude deviation | "Deviation - Altitude" | Loss of separation |
| D | Track or heading deviation | "Deviation - Track / Heading" | Loss of separation |
| E | Airspace violation | "Airspace Violation" | Loss of separation |
| F | Other deviation from an ATC clearance or restriction | "Deviation - Speed" or "Deviation / Discrepancy - Procedural Clearance" | Loss of separation |

- Records matching none of these are dropped. That includes procedural deviations other than clearance ones, such as checklist, MEL and weight-and-balance issues, which are kept for a possible second phase.
- **Records excluded automatically** are any whose Result field contains "Aircraft Damaged" or "Physical Injury".
- The wording of each standard bad ending is fixed in the protocol, and approved by James, before any case is condensed.

## 3. The random order

- Within each category, records are sorted by ACN (NASA's report number), then shuffled with Python's `random.Random(20261001)`.
- The seed is fixed here and is not changed.

## 4. Screening, in shuffled order

Each category is screened in its shuffled order until **8 records qualify**, giving **48 cases**. The next **2 qualifying records overall** are kept for the pilot run and are never used in the main study.

**If a category runs out** before 8 qualify, its remaining places go to category C (altitude), the largest, screened in the same shuffled order. The shortfall is reported.

A record qualifies only if all of these hold:
1. The crew of the reporter's own aircraft made an action or decision that is central to the event. Events caused solely by ATC or by equipment do not qualify.
2. The narrative gives enough to state what the crew knew and what they did.
3. No injury or aircraft damage is mentioned in the narrative.
4. The category's standard bad ending is a plausible result of the same actions, without changing them.
5. It is not mainly a technical emergency, and it does not mention alcohol, drugs or medical incapacity.
6. It is not a second report of an event already selected (same date, place and aircraft). The first one drawn is kept.

**Logging.** Every screened record is logged in `data/screening-log.csv` with its ACN, category, decision and a one-line reason, including the ones that fail. Claude screens; James can audit the log; the independent checkers re-screen a sample, blind to any results.

## 5. Control cases

About six control cases are written by James, separately from ASRS:
- clear blameless errors;
- clear knowing violations with workable procedures.

They are used only as a sanity check and are never part of the main analysis.

## Revisions before the export

**Revision 1, 1 Oct 2026** (James and Claude; no report exported or read).

1. **Year changed from 2024 to 2025.**
   - *Why 2025 rather than 2024:* it is more recent, and less likely to be in the AI models' training data.
   - *Why not 2026:* James ran the same search for two windows. January–June 2026 returned 227 records; January–June 2025 returned 350. The 2026 shortfall points to NASA's processing lag, which would leave the sample short of recent months.
   - *Whole year, and the size rule replaced:* those counts showed the 10,000 export limit does not bite, so the shrink-to-fit step was dropped. The whole of 2025 is used so the small categories have enough to draw from, and the fallback for a small count is now widening to July 2024.
2. **Event types widened from four to six categories.**
   - Airspace violations and other deviations from an ATC clearance or restriction are added.
   - Every category now maps to one of three standard bad endings, so no case needs an ending of its own.
   - The design moves to 8 cases per category, 48 in total, instead of 10 × 4 = 40.
3. **The Reporter Function and Event Type values are written out exactly as entered.** The form cannot select a top-level event type on its own; it selects all of the values under it.

**Revision 2, 1 Oct 2026** (James and Claude; still no report exported or read).
- **Primary Problem widened to Human Factors and Procedure.** Reports where NASA judged the procedure to be the main problem are what test Reason's "were the procedures available, workable, intelligible and correct?" branch, and system-induced violations.
- Reports where the crew simply followed a flawed procedure, with no unsafe act of their own, fail screening criterion 1. Each case's NASA primary-problem code is recorded, so results can also be reported split by human factors and procedure, as an exploratory analysis.
- For the record: the 2025 search with Human Factors alone returned 609 records (James, 1 Oct 2026).
