# How to hand-code the calibration traces

*Practical instructions for human coders of the calibration traces. Since 3 November this is planned for the second study (human validation), with recruited coders who can read code; the first paper uses an AI pilot instead. The current codebook is `codebook/v1.md`; the Coding Desk now uses it, including the evidence grade for violations.*

## The short version

Open the **Coding Desk** (link below). For each of the 30 traces, C01 to C30: read it all the way through, then fill in the form on the right. Your work saves automatically. When all 30 are done, write codebook v1 from your notes, then go through the 30 once more against v1. Tell Claude "import my codings" whenever you want them copied into the repo.

## Where to do it: the Coding Desk

**https://claude.ai/artifact/HtYBLkAJJjvpzk47woaYxp** (private to you)

- **Left:** the 30 traces, with a dot showing progress (empty = not started, half = draft, green = done, red = needs fixing).
- **Middle:** the trace, step by step, exactly as in `data/calibration/Cxx.md`. MAST's labels and the benchmark answers are hidden.
- **Right:** the coding form. Each code shows its codebook definition next to it. A box at the bottom lists anything missing or inconsistent.
- **Cite:** press a step's **Cite** button to add its step number to your evidence box. If you select text in the step first, the quote goes in too (only needed for a *stated* violation).
- **Saving:** automatic. The top bar says "All changes saved". Your codings are stored in the page's private database; only you can write them. Claude can read them back and copy them into `annotations/human/calibration_sheet.csv`.
- **Time:** the page counts minutes spent on each trace while it is open (you can correct the number).
- Works on a laptop or tablet. On a phone it switches to two tabs, "Read trace" and "Code it".

## How to code one trace

This is an investigation in miniature: start at the unsafe act and work back up the layers.

1. **Read it through once without coding.** Work out what the task was, what the agents did, and whether the outcome was right. Long tool outputs (web pages, API documentation) can be skimmed; the evidence is usually in how the agents reacted to them.
2. **Is there a failure?** `yes`, `no` or `unclear`. Four of the 30 are traces MAST judged failure-free; you don't know which, so judge each trace on what you see.
3. **L1, the unsafe act.** Find the moment or moments where an agent did, or failed to do, something that made the failure happen. For each one, apply the violation rule:
   - Q1. Was the requirement in the agent's context? If not: error.
   - Q2. Does the trace show the agent registered it, or could the deviation not plausibly be accidental? If neither: error.
   - Q3. Did the agent proceed otherwise anyway? If not: no unsafe act.
   - If all three hold: V1 (recurs), V2 (one-off), or V? (evidence for Q1 or Q2 is thin).
   - If it is an error: E1 slip in carrying out a sound intention, E2 wrong decision on adequate information, or E3 misread something. Then tick which cognitive function failed (Ezell et al.): observation, understanding, decision or action (codebook v1, note 5.11).
   - An agent stuck repeating itself is an L1 act; if another agent was supervising and could have stopped it, also code L3.3 (note 5.9).
   - Something that never happened (e.g. nobody verified the result): code it by whose job it was. An agent told to do it: L1. A supervisor who should have checked: L3.1. Nobody given the job: L4.1 or L4.3 (note 5.10).
   - If nobody did anything wrong (for example a tool failed and the agents reported it sensibly), leave L1 empty and write "no unsafe act" in the notes (codebook v1, note 5.8).
4. **L2, preconditions.** What made that act possible or likely? A tool or environment problem (L2.1), the agent's state such as lost instructions or a carried-over error (L2.2), or a breakdown between agents (L2.3).
5. **L3, supervision.** Did the orchestrator or the task specification play a part? Nobody checked the output (L3.1), a task given to an agent that couldn't do it (L3.2), a visible problem left uncorrected (L3.3), an unclear or incomplete task (L3.4), whether the human user or an orchestrating agent set it (say which in the notes).
6. **L4, design.** Did the way the system was built or run set this up? Roles, verifier or termination logic (L4.1), tools or budgets (L4.2), missing procedures (L4.3), a run launched or configured wrongly, such as an empty task (L4.5). L4.4 (model development) is not coded from traces: it needs developer records, so the Coding Desk doesn't offer it.
7. **Only code a layer if the trace shows evidence for it.** Leaving a layer empty is a valid answer.
8. **Finish the form:** deepest contributing layer, confidence, the step references for each code (e.g. `L3.3: [S14], [S17]`; no quotes needed, except one quote of the agent's own words for a violation graded *stated*), and notes. The notes matter most when the codebook didn't fit: write what you wanted to say and why no code said it. Then press **Mark as done**.

If you can't decide between two codes, pick one, set confidence to `medium` or `low`, and write the alternative in your notes. Those hesitations are exactly what calibration is for.

## Two passes

1. **Pass 1:** code all 30 with the current codebook (v1), writing notes as you go, especially where it didn't fit.
2. **Revise the codebook if needed.** The notes may show a rule that needs changing; the author decides any change, and the new version gets a new number.
3. **Pass 2:** go through all 30 codings once more against the revised codebook and change whatever it changes. This is quicker than pass 1: you are checking, not re-reading everything. Do it **before** seeing any AI codings, so the AI can't influence the reference.

The reviewed set becomes the reference the AI is measured against. The paper reports how many codings the review changed, so readers can see how much the codebook moved.

## Keeping it blind

- Don't open `data/processed/calibration_key.csv` (it says which traces are controls and which are held out for testing).
- Don't look up MAST's labels for these traces.
- Benchmark answers are hidden while you code. Look at them only after pass 2 (`uv run afacs-render C07 --show-benchmark`).
- Don't ask Claude to run the AI annotator on these 30 traces until pass 2 is finished.

## Pacing

About 129,000 words in all: realistically 12–15 hours, for example 3 hours a day from 6 to 10 November. AG2 and MetaGPT traces take 5–15 minutes; AppWorld, HyperAgent, Magentic-One and OpenManus take 30–60. Code in order, C01 to C30: the order is random, so if time runs short you can stop and the set stays balanced.

## Reading the traces

- **framework log** steps are the software's bookkeeping, not an agent's words.
- Dashed steps marked **not visible to agents** are placeholders for hidden benchmark information.
- Text marked **Note added by AFACS** is not part of the log. It explains a logging artefact (for example, OpenManus logs that print only the start of the task, or one run where the task was typed in and never logged).
- "(empty message ...)" means the agent produced nothing in that turn. That is evidence.

## Without the Coding Desk

If you'd rather work offline: open `data/calibration/C01.md` … `C30.md` and fill in `annotations/human/calibration_sheet.csv` in a spreadsheet (codes separated by `;`, quotes separated by ` | `). Check it with `uv run afacs-agreement check-sheet`. Recreate the trace files on a new machine with `uv run afacs-sample calibration --renders-only`.
