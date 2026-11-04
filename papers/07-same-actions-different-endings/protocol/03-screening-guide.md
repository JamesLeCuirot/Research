# Screening guide

*Fixed 1 Oct 2026, before screening began. Amended once during screening: the criterion 4 clarification under deviation D3 (TCAS below about 1,000 ft above ground). It applies only to the loss-of-separation categories C, D and F, and was applied retrospectively to all of their qualifiers. Categories A, B and E are unaffected: A and B have different bad endings, and E had no qualifiers.*

## The task

Read your category's pack (`data/screening/pack_<X>.txt`) **from the top, in draw order**. Decide for each report whether it qualifies, and log every report you read, whether it passes or fails. Stop as soon as the quota is met:
- **8 qualifying reports** for categories B, D, E and F;
- **9** for categories A and C. The 9th is flagged as a pilot case and is never used in the main study.

If the pack runs out first, stop, and report the shortfall.

## The six criteria

A report qualifies only if **all six** hold. Where it fails, give the **first** criterion it fails.

1. **The crew's own action is central.** The crew of the reporter's own aircraft made an action or decision that is central to the event.
   - Fails if the event was caused solely by ATC, another aircraft or equipment, and the crew did nothing that contributed.
   - Readback, hearing, setting, monitoring and decision errors by the crew all count as crew actions.
2. **There is enough detail.** The narrative gives enough to state what the crew knew and what they did.
3. **There is no harm.** No injury and no aircraft damage are mentioned anywhere in the report.
4. **The category's bad ending is plausible.** It must follow plausibly from the *same* crew actions, with only luck changing. For example, other traffic happened to be there, or the runway was shorter or wetter than it might have been.
   - **A — runway excursion.** The aircraft leaves the end or the side of the runway at low speed, and some people are slightly injured.
   - **B — runway conflict.** Another aircraft or vehicle has to take abrupt avoiding action, such as a high-speed rejected take-off or a go-around at low height, and comes very close.
   - **C, D, E, F — loss of separation.** Another aircraft comes very close, both crews follow TCAS resolution advisories, and a cabin crew member is injured in the manoeuvre.
     - Fails if the deviation could not plausibly bring another aircraft close. A purely ground event in C–F counts as implausible for this ending.
     - **Clarification, 1 Oct 2026, deviation D3.** Also fails if the crew's deviation happened entirely below about **1,000 ft above ground**, such as low on final approach. TCAS does not issue resolution advisories there, so "both crews follow TCAS RAs" cannot happen. A deviation that began above 1,000 ft above ground can still qualify.
   - **Addition, 1 Oct 2026, deviation D7, for replacement screening.** Category C, D and F cases (the loss-of-separation ending) must be passenger flights, because the ending injures a flight attendant aboard. A report fails criterion 4 if its Mission field says "Cargo / Freight / Delivery", or if the narrative shows it was a cargo, ferry or positioning flight.
5. **Not a technical emergency, and no substance or medical issue.** It is not mainly a technical emergency, and it does not mention alcohol, drugs or medical incapacity of the crew. Fatigue is allowed.
6. **Not a duplicate.** It is not a second report of an event you have already accepted, judged by the same date, place and aircraft. Keep the first one drawn.

## What you must not do

- **Don't judge interest.** Do not prefer cases that seem interesting, borderline or likely to show any effect. Apply only the six criteria. Do not think about how the crew might be judged.
- **Don't change files.** Do not change any file except your own log, and do not read other categories' packs.
- **Use the pack only.** No web or other sources.

## The log format

Write `data/screening/log_<X>.csv`. It is UTF-8 with a header row and these columns:

`category,draw_rank,acn,decision,failed_criterion,pilot,reason`

| Column | What goes in it |
|---|---|
| `decision` | `qualifies` or `fails` |
| `failed_criterion` | The criterion number, 1–6. Blank if it qualifies |
| `pilot` | `yes` only for the 9th qualifier in A and C; otherwise blank |
| `reason` | One plain sentence, without quoting the narrative at length. For qualifiers, say in a few words what the crew did |
