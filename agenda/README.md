# Research agenda: aviation safety science for AI alignment

Proposals that apply aviation safety science and human factors to the research areas in Anthropic's alignment agenda (scalable oversight, AI control and robustness, model organisms, interpretability, safeguards, AI welfare). Drawn up on 3 November 2026 from a literature review; five have since been written up as working papers.

Status: **written** = a working paper exists in [`papers/`](../papers/); **planned** = not started.

## Scalable oversight and honesty

| ID | Proposal | Kind | Status |
|---|---|---|---|
| SO-1 | **The Captain Says:** do models drop a correct answer on aviation regulations when someone more senior pushes back? An authority-gradient sycophancy benchmark built from verbatim FAA, EASA and UK rules, testing a CRM-style two-challenge instruction. | Empirical | Planned |
| SO-2 | **Sandwiching on the Flight Deck:** can non-experts oversee an AI on aviation law? A scalable-oversight test with expert-marked multi-rule questions and planted systematic errors. | Empirical | Planned |
| SO-3 | **Skill Fade in the Oversight Loop:** the ironies of automation applied to the people who oversee AI for safety; proposes "overseer currency" requirements. | Theory | Planned |
| SO-4 | **Just Culture for Machines:** why penalising disclosure teaches concealment. | Theory | **Written:** [paper 01](../papers/01-just-culture-for-machines/) |

## AI control and robustness

| ID | Proposal | Kind | Status |
|---|---|---|---|
| AC-1 | **Rare threats and LLM monitors:** does the airport-screening low-prevalence effect appear in AI monitors? | Empirical | **Written:** [paper 02](../papers/02-do-llm-monitors-miss-rare-threats/), "Do LLM Monitors Miss Rare Threats?" (the pre-registered prediction was reversed) |
| AC-2 | **The Human in the Audit Budget:** how much AI-control safety estimates fall once human auditor performance is realistic (vigilance, cry-wolf, automation bias), and which countermeasures recover it. | Theory and simulation | Planned |
| AC-3 | **Shift Handover for Agents:** testing aviation-style structured handovers against constraint loss and false "sanction" when agents compact their context or hand work to another agent. | Empirical | Planned |

## Model organisms

| ID | Proposal | Kind | Status |
|---|---|---|---|
| MO-1 | **Pressing On:** plan-continuation bias as a model organism of agentic "momentum"; tests stabilised-approach gates, no-fault go-around framing and briefed abandonment criteria. | Empirical | Planned |
| MO-2 | **Drift Toward the Boundary:** does skipping a safety step become normal over repeated agent episodes when it is never caught? | Empirical | Planned |
| MO-3 | **Who's Flying the Aircraft?** Diffusion of responsibility in multi-agent AI teams, and whether a designated monitoring role helps. | Empirical | Planned |

## Interpretability and auditing

| ID | Proposal | Kind | Status |
|---|---|---|---|
| IN-1 | **Situation-awareness probes for auditing agents:** SAGAT-style freezes to locate where AI auditors fail (perception, comprehension or projection). | Empirical | Planned |
| IN-2 | **Instruments, Not Just Insights:** instrument-validation and display-design requirements for interpretability tools used in safety decisions. | Theory and heuristic review | Planned |

## Safeguards, evaluation and assurance

| ID | Proposal | Kind | Status |
|---|---|---|---|
| SG-1 | **From RSP to SMS:** frontier AI safety frameworks read through ICAO's Safety Management System. | Theory | **Written:** [paper 03](../papers/03-from-rsp-to-sms/) |
| SG-2 | **Checkride or Jump Seat?** What LOSA and evidence-based training teach about evaluation awareness. | Theory and pilot | **Written:** [paper 04](../papers/04-checkride-or-jump-seat/) |
| SG-3 | **Untrusted by Design:** bringing AI control into EASA's operational oversight of Level 3 AI. | Theory | **Written:** [paper 05](../papers/05-untrusted-by-design/) |

## AI welfare

| ID | Proposal | Kind | Status |
|---|---|---|---|
| AW-1 | **Self-Reports Are Not Enough:** what workload and situation-awareness measurement (NASA-TLX, SAGAT vs SART) teach AI welfare evaluation. | Theory and small study | Planned |
| AW-2 | **Stop-Work Authority:** fitness-for-duty, pilot-in-command authority and no-fault go-around policies compared with letting models decline or end interactions. | Theory | Planned |

## Short essays (planned)

- **Überlingen and the instruction hierarchy:** when two authorities conflict, the precedence rule must be unambiguous, trained and known to everyone involved.
- **A sterile cockpit for agents:** restricting agents to safety-relevant actions in critical phases such as deployments, payments and deletions.
- **The agent flight manual:** limitations, normal and abnormal procedures, and a minimum equipment list for deployed agents.
- **Unreliable airspeed:** what AF447 teaches about monitors whose inputs can be corrupted.
- **Tool, teammate or patient?** The FAA's refusal to personify AI set against labs' work on model character and welfare.
