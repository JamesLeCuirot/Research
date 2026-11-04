# Cross-walk: Ezell et al. (2025) → AFACS

*Draft for James to correct. Source: Ezell, Roberts-Gaal & Chan (2025), "Incident Analysis for AI Agents", AIES 2025, arXiv:2508.14231 — their three factor categories (Section 2) and full taxonomy (Appendix A). AFACS codes are from `codebook/v1.md`.*

## How the two frameworks line up

Ezell et al. describe one causal chain: **system factors** and **contextual factors** lead to **cognitive errors**, which lead to the incident. HFACS, and so AFACS, describes four tiers: organisational influences, supervision, preconditions, unsafe acts. The broad correspondence:

| Ezell et al. category | Closest AFACS layer | Comment |
|---|---|---|
| System factors (training, feedback, learning methods, system prompt, scaffolding) | **L4 Organisational / design**, with the system prompt at **L3.4** | AFACS v0 had no code for how the model was trained; v1 adds **L4.4 Model development**, a developer-evidence code that is not applied from traces alone. |
| Contextual factors (information, tools, task definition) | **L2 Preconditions** (L2.1), with task definition at **L3.4** and budgets at **L4.2** | Close match. |
| Cognitive errors (observation, understanding, decision-making, action execution) | **L1 Unsafe acts: errors** (E1–E3), with memory and distraction at **L2.2** | Their four functions cut the same ground as HFACS's three error types differently. |
| *(no equivalent)* | **L3 Supervision / orchestration** (L3.1–L3.3) | Their framework is for single agents; there is no orchestrator, so no supervision tier. |
| *(no equivalent)* | **L2.3 Coordination** | No crew-resource-management analogue between agents. |
| *(folded into cognitive errors, not distinguished)* | **L1 Violations** (V1, V2, V?) with evidence grading | They count "performing an unintended or undesirable task" as a cognitive error and cite an agent reasoning about cheating its tests (Baker et al., 2025), but nothing distinguishes a deliberate departure from an error. |

## Item by item

### System factors (their A.1)

| Ezell et al. factor | AFACS code | Note |
|---|---|---|
| Training data: poisoning; false or misleading data; misuse-enabling data; sensitive information; content gaps | **L4.4** Model development *(developer evidence)* | Not codable from a trace; needs training records or version comparisons. A content gap can surface in a trace as an L1.E2 on a niche topic. |
| Feedback: undesirable proxy goal; wrong trade-offs; poisoned feedback | **L4.4** *(developer evidence)* | The usual latent condition behind a violation (e.g. training that rewarded looking successful); a developer can test it by checking whether the training signal would have rewarded the behaviour. |
| Learning methods: memorisation, forgetting, wrong inferences, reinforcing the wrong goal, poor generalisation | **L4.4** *(developer evidence)* | Testable by comparing model versions or checkpoints on the same scenario. |
| System prompt underspecified, or inadvertently encourages undesirable behaviour | **L3.4** Deficient specification | AFACS treats the system prompt as part of the task specification. |
| Scaffolding does not function as intended / functions ineffectively | **L4.1/L4.2** (limitation built into the design) or **L2.1** Environment (malfunction during the run) | Coded by cause (decided; codebook v1, open question 4). |

### Contextual factors (their A.2)

| Ezell et al. factor | AFACS code | Note |
|---|---|---|
| Information inaccessible, missing, or of poor quality | **L2.1** Environment | |
| Information environment open to malicious inputs (prompt injection) | **L2.1** Environment | Rare in MAST's benchmark runs. |
| Information includes sensitive data | **L2.1** Environment | Not observed in MAST. |
| Tools cannot be accessed or used; do not work as intended; vulnerable to attack | **L2.1** Environment (failure during the run) or **L4.2** Resource provisioning (wrong or missing tools by design) | |
| Inability to monitor tool errors (e.g. cannot see execution logs) | **L4.2** Resource provisioning | |
| Lack of task clarity; conflicting instructions | **L3.4** Deficient specification | |
| Task constraints (time, token or other resource limits) | **L4.2** Resource provisioning | |

### Cognitive errors (their A.3)

| Ezell et al. factor | AFACS code | Note |
|---|---|---|
| Observation: incorrect expectation; failure to notice; attention to irrelevant information | **L1.E3** Perceptual | |
| Observation: inadequate memory capacity | **L2.2** Agent state | A precondition rather than an act. |
| Understanding: misinterpretation of information | **L1.E3** Perceptual | |
| Understanding: conclusions from insufficient, misleading or wrongly assumed information | **L1.E2** Decision, with **L2.1** where the information itself was poor | |
| Decision-making: misreading user or developer intentions | **L1.E3** or **L1.E2** | E3 if a message was misread; E2 if read correctly but wrongly weighed. |
| Decision-making: wrong goal priority; non-viable plan; too few alternatives; wrong evaluation criteria | **L1.E2** Decision | |
| Decision-making: forgets or is distracted from the goal | **L2.2** Agent state, often with **L1.E2** | |
| Action execution: incorrect execution (e.g. malformed API call) | **L1.E1** Skill-based | |
| Action execution: failure to take action | **L1.E1** (a lapse) or **L1.E2** (a decision not to act) | |
| Action execution: failure of error monitoring (ignores tool feedback) | **L1.E3** (missed it), or **L3.3** where a supervising agent should have caught it | |

## What each framework adds

**AFACS adds to Ezell et al.**
1. A supervision tier for multi-agent systems: an orchestrator that fails to check output (L3.1), assigns a task beyond an agent's ability (L3.2), or leaves a visible problem uncorrected (L3.3). The human user who sets the task sits at the top of this chain (L3.4), and the people who launch the run are treated as part of the organisation (L4.5 Operation set-up).
2. Coordination between agents (L2.3), the crew-resource-management analogue.
3. Violations, coded from behaviour with graded evidence (stated, inferred, thin).
4. An empirical test on real traces (this study).

**Ezell et al. add to AFACS**
1. Model development as a latent condition (L4.4), together with the point that it needs a different kind of evidence: developer records, not traces (codebook v1, section 1.1).
2. Security-related context (malicious inputs, vulnerable tools) as named sub-cases of L2.1.
3. A finer description of cognitive functions (observation, understanding, decision, action). AFACS records the Ezell function for every L1 error alongside the HFACS error type (codebook v1, note 5.11), so the study can check the mapping above against real codings and compare which scheme coders apply more consistently.
4. A specification of what information investigators need (their Table 1), which this study audits against MAST's logs (`docs/information_audit.md`).

## A difference in scope

Ezell et al. analyse **incidents**: events that cause or could cause harm. MAST's traces are **failed benchmark tasks** with no harm. Aviation draws the same line: occurrence reporting covers events where nobody was hurt, and the same causal analysis applies to them. The paper should say this explicitly.
