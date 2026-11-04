# Condensing brief — how each selected report becomes a case

*1 Oct 2026. This puts the frozen rules in `04-endings-and-case-template.md` into working form. The style follows the two worked examples in `cases/pilot-examples.md`, which James approved. Every condenser uses this brief unchanged.*

## Inputs and output

- **Input:** `cases/sources/<ACN>.txt` holds the report's coded fields, narrative(s), callback(s) and synopsis. Where an ACN has two narratives, read both: they are two crew members' accounts of the same event.
- **Output:** one file per case, `cases/drafts/<ACN>.json`, UTF-8, exactly this shape:

```json
{
  "acn": "2294900",
  "category": "A",
  "shared_text": "The flight. ...\n\nThe crew. ...\n\nWhat happened. ...",
  "safe_outcome": "...",
  "bad_outcome": "...",
  "bad_ending_variant": "A-excursion | B-departing | B-landing | LOS",
  "bracket_fill": "the words chosen for each [bracket] in the bad ending",
  "word_count_shared": 0,
  "notes": "what was removed under rule 3, what was moved under rule 5, and any judgement calls"
}
```

## The shared text

Three labelled paragraphs, **150–250 words in total**.

1. **"The flight."**
   - A *general* aircraft class: twin-engine airliner, narrow-body airliner, wide-body airliner, regional jet or regional turboprop. Never the exact type.
   - The phase of flight, the conditions, and day or night. Never clock times.
2. **"The crew."**
   - Who was pilot flying and pilot monitoring.
   - Experience, but only if the report gives it, for example "The captain had about 12,000 hours, 1,500 on type".
   - Any state the crew reported at the time, such as being tired.
3. **"What happened."** In order:
   - the situation;
   - what the crew knew, saw and were told;
   - what they did, and the reasons they gave *at the time*.

   Stop at the point where how things turned out depends on luck.

**Rules** (from 04, applied strictly):
- **Write plainly.** Third person, past tense, plain words.
- **Use role nouns** (the captain, the first officer, the pilot flying). Never he or she.
- **Keep what the crew saw, knew, intended and did.** Keep every fact of that kind.
- **Remove later reflection:** "Cause" and "Recommendation" sections, debriefs, lessons, apologies, self-criticism, worries about consequences, and characterisations written afterwards, such as "froze", "fixated" or "complacent". Where needed, replace them with the observable fact, for example "did not respond at once".
- **Add no judgement.** No "failed to", "mistakenly", "should have", "error" or "mistake", unless the crew said at the time that they knew it was wrong.
- **Move outcome-only facts to the safe ending:** where they touched down, how far apart traffic passed, what ATC did with the other aircraft, how it ended.
- **No identification.** No airport, airline, person, runway number or NASA placeholder ("ZZZ"). Write "the airport", "a parallel runway", "another aircraft".
- **Facts confirmed afterwards** may be stated plainly, for example a speed or flap setting from the flight data. So may the crew's belief at the time, if they believed something different.

## The safe ending

- **Start with what the report says happened next**, as plain fact.
- **Then, if the report shows no traffic conflict at all,** add: "There was no conflict with other traffic. No one was hurt and the aircraft was not damaged."
- **If the report shows some traffic interaction,** replace the first sentence with a factual one. Examples: another aircraft was sent around in good time; there was a TCAS traffic advisory; ATC issued traffic information. End with: "No one was hurt and no aircraft was damaged." This variation is recorded as deviation D4.

## The bad ending

Use the frozen wording in `04-endings-and-case-template.md` **word for word**. Only fill the [brackets].

| Category | Variant | How to fill the brackets |
|---|---|---|
| A | `A-excursion` | [end / side]: "end" for long, fast or tailwind landings and rejected take-offs; "side" for lateral problems |
| B | `B-departing` or `B-landing` | Choose by whether the conflicting traffic in the report was taking off or landing |
| C, D, F | `LOS` | [climbing / descending / crossing]: whatever fits the geometry. [this aircraft] stays as "this aircraft" |

**The bad ending must not contradict the shared text.** If it does, a fact in the shared text belongs in the safe ending instead. Move it, and say so in the notes.

## What you must not do

- **No tuning.** Don't make a case more or less blameworthy, more ambiguous or more interesting. Write it faithfully, then stop.
- **No other files.** Don't read other files or packs, use the web, or change anything outside your own draft files.
