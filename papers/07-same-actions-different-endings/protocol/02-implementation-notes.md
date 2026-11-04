# Implementation notes — fixed before any narrative was read

*1 Oct 2026, Claude. These settle points the sampling rule left open. They were written after the coded fields had been tallied, and before any narrative was opened.*

1. **Matching codes.** Anomaly codes are matched as whole codes. See the header of `scripts/01_draw.py`.
2. **Random order.** Each category is shuffled with its own fresh `random.Random(20261001)`.
3. **Pool sizes after the draw:**

   | Category | Reports |
   |---|---|
   | A — unstabilised approach | 135 |
   | B — runway incursion | 23 |
   | C — altitude deviation | 90 |
   | D — track or heading deviation | 27 |
   | E — airspace violation | 49 |
   | F — other clearance or restriction deviation | 49 |

   376 reports fit none of the six categories, and 12 were excluded for damage or injury.
4. **Category B** contains runway incursions only. No report in the export carries the "Landing Without Clearance" code.
5. **The two pilot cases** are the next qualifying record in category A after its 8th, and the next qualifying record in category C after its 8th.
6. **Screening rests on the narrative.** Each report is judged on its narrative(s) and synopsis. Where an ACN combines two reporters' narratives, both are read.
