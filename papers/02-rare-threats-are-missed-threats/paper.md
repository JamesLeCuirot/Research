---
title: "Rare Threats Are Missed Threats"
subtitle: "A pre-registered test of the low-prevalence effect in LLM code monitors"
author: "James Le Cuirot"
affiliation: "Citadel Aero"
date: "Draft v0.1, 3 November 2026"
status: "Working draft for author review. Not peer reviewed. Results, Discussion and Conclusion are pending."
abstract: |
  AI control protocols use language-model monitors to review the work of more capable, untrusted AI systems and to pass the most suspicious items to a small human audit budget. In deployment, real attacks are expected to be rare. In human visual search, rare targets are missed far more often than common ones. This low-prevalence effect is mainly a shift in decision criterion, and airport security counters it with Threat Image Projection, which inserts fictional threats into live screening. This pre-registered study asks whether large language model (LLM) monitors show the same effect. Two Claude models reviewed short Python solutions to MBPP programming problems. Some solutions contained a verified backdoor: code that passes the given tests but returns a wrong answer on one trigger input. We varied the share of backdoored submissions within a 40-item batch (50%, 10% or 2.5%), stated a base rate for single-item judgments (50% or 1%), and tested two remedies at 2.5%: a short labelled calibration block modelled on Threat Image Projection, and an instruction to judge each item independently. Signal detection measures separate changes in the monitor's criterion from changes in its sensitivity. <!-- RESULTS PENDING --> **[Results pending: one or two sentences on H1 to H3, with the key numbers taken from `results/RESULTS.md`.]** We discuss what the results imply for the prevalence used in control evaluations and for testing deployed monitors with inserted attacks.
keywords: [AI control, trusted monitoring, low-prevalence effect, signal detection theory, threat image projection, LLM-as-a-judge, aviation security, human factors]
---

# 1 Introduction

AI control is the study of safety measures that are meant to keep working even if an AI system is deliberately trying to defeat them (Greenblatt et al., 2024). A central measure is *trusted monitoring*. A capable but *untrusted* model does the work. A weaker model that is *trusted*, typically because it is thought too limited to subvert the protocol deliberately, reads each output and gives it a suspicion score. The most suspicious outputs go to a small budget of careful human review, called *auditing*. In the original code-writing testbed the audit budget covered 2% of problems (Greenblatt et al., 2024, Section 2.2).

The attacks such a monitor is meant to catch are expected to be rare. In control evaluations the *red team*, which plays the part of a misaligned model, can defeat simple auditing by attacking seldom, so that no attack is likely to fall inside the audited sample (Greenblatt et al., 2024, Section 3.1; Bhatt et al., 2025, Section 3.1). A sketch of a control safety case notes that a model "might simply attack very rarely such as once out of thousands of tasks" (Korbak et al., 2025, Section 6). Deployment reports are consistent with this. Anthropic's offline monitor for its internal research agents flags about one to two transcripts in every thousand, and the company reports that individual agents rarely misbehave (Favaro & Wright, n.d.; Section 3.3). Nearly everything such a monitor reads is benign.

Human factors research has studied this situation for decades. People searching for rare targets miss many of them. In a simulated baggage-screening task, misses rose from 7% when targets appeared on half of trials to 30% when they appeared on 1% (Wolfe et al., 2005). The extra misses come mainly from a shift in decision criterion: observers say "no" more readily, while their ability to tell targets from non-targets changes little (Wolfe et al., 2007). Airport security responds with Threat Image Projection (TIP), software that projects images of fictional threats into a small share of real bags and records whether the screener finds them (Cutler & Paddock, 2009; Buser et al., 2025).

Do LLM monitors behave the same way? There are reasons to expect that they might and reasons to expect that they might not (Section 4.3). Current practice mostly assumes they do not. An audit of eleven evaluations of detectors for hijacked LLM agents found that attacks made up 16% to 86% of test samples and that "no evaluation varies that share" (Abbasi et al., 2026, Abstract). Studies that estimate performance at low prevalence apply hit and false-alarm rates measured at high prevalence (Srivastav et al., 2026, Section 6.3; Abbasi et al., 2026, Section III.E), and a formal model of trusted monitoring treats suspicion scores as "a distribution, conditioned on whether the code is safe or backdoored" (Griffin et al., 2024, Section 2). If a monitor's judgments shift with how often it sees attacks, these practices overstate how many attacks a deployed monitor would catch.

This paper reports a pre-registered experiment that tests for a low-prevalence effect in LLM monitors of code. It asks three questions. Do LLM monitors flag fewer backdoors when backdoors are rare? If so, is the change a shift in criterion or a loss of sensitivity? Do remedies taken from screening research reduce it? Its contributions are:

- A pre-registered test of the low-prevalence effect in LLM code monitors that separates *experienced* prevalence (the share of backdoored submissions in a batch the monitor reviews) from *stated* prevalence (a sentence in the prompt).
- A signal detection analysis of monitor flags and suspicion scores, borrowed from human screening research, that separates the monitor's criterion from its sensitivity.
- A test of two remedies at low prevalence: a labelled high-prevalence calibration block modelled on TIP and on the retraining bursts of Wolfe et al. (2007), and an instruction to judge each item independently.
- An open set of execution-verified pairs of clean and backdoored solutions built from MBPP, released with the code, prompts and raw monitor outputs.
- An account, for AI-safety and aviation-safety readers, of where the human analogy holds and where it does not.

The pre-registration is `PREREGISTRATION.md` in this folder. It was committed to the project repository on 3 November 2026 (commit `f4bedaa`) and records that no monitor data had been collected at that point. Departures from it are listed in Section 5.8.

# 2 Background: rare targets in human screening

## 2.1 Signal detection theory

Signal detection theory (SDT) describes decisions about whether a signal is present (Green & Swets, 1966; Hautus et al., 2021). In this study a *signal* trial is a backdoored submission and a *noise* trial is a clean one. Flagging a backdoored item is a *hit*; flagging a clean item is a *false alarm*. The hit rate *H* and false-alarm rate *F* give two quantities. Sensitivity, *d′* = z(*H*) − z(*F*), measures how well the observer separates the two kinds of item. The criterion, *c* = −½[z(*H*) + z(*F*)], measures how much evidence the observer needs before saying "yes": a positive *c* is conservative (fewer flags, more misses) and a negative *c* is liberal. Here z is the inverse of the standard normal distribution function, which is infinite at 0 and 1. The log-linear correction, in which "each cell frequency in the contingency table is increased by 0.5", handles this with less bias than the 1/(2N) rule, and its remaining bias always underestimates *d′* (Hautus, 1995, Abstract).

For graded ratings, such as a suspicion score from 0 to 100, the area under the receiver operating characteristic curve (AUROC) summarises sensitivity across all thresholds; 0.5 is chance and 1.0 is perfect separation. Unlike precision, AUROC does not depend on prevalence, which is also why it hides the fact that "when attacks are rare, even a small false-positive rate yields alerts that are mostly false" (Abbasi et al., 2026, Section I).

A criterion that moves with prevalence is not irrational. Wolfe et al. (2007, Introduction) note that "[y]ou will be less likely to call something a target if the a priori probability of a target is lower", and that "the prevalence effect is a very sensible behavior unless the goal is to minimize misses". In screening for threats, and in monitoring for attacks, the goal is to minimise misses.

## 2.2 The low-prevalence effect

Wolfe et al. (2005) asked observers to look for "tools" among other semi-transparent objects in an artificial baggage-screening task. Misses were 7% at 50% target prevalence, 16% at 10% and 30% at 1% (figures from the authors' accepted manuscript; see `sources.md`). At low prevalence observers also gave up target-absent searches sooner, responding "no" much more quickly at 2% prevalence than at 50% (Wolfe et al., 2007, Experiment 2).

Wolfe et al. (2007, Abstract) found the effect "very robust" and concluded that "[i]n signal detection terms, the prevalence effect can be explained as a criterion shift and not a change in sensitivity". Several attempts to move observers to a better criterion failed; forced slowing, for example, "had no appreciable effect on errors" (Experiment 2). One regime worked: brief retraining periods at high prevalence with full feedback, inserted among long low-prevalence periods without feedback (Experiment 7). In that experiment "[t]here were no significant effects of prevalence": misses averaged 0.21 in low-prevalence epochs and 0.18 in high-prevalence epochs, while false alarms rose.

Trained screeners show the effect too. Newly trained transportation security officers had lower hit rates in low-prevalence blocks (prevalence of .05 or less, no feedback) than in a high-prevalence block (.50, full feedback), and a low-prevalence block run after the high-prevalence block showed better performance and a more liberal criterion (Wolfe et al., 2013). Unlike in the laboratory, *d′* also changed with prevalence, so in the field the effect was not purely a criterion shift. Very rare targets fare worse still. Across millions of trials from the *Airport Scanner* smartphone game, detection fell logarithmically with target frequency, with "catastrophically low detection rates" for the rarest items (Mitroff & Biggs, 2014).

Becker et al. (2026) tested occasional *probe* trials with known targets and feedback. Probes reduced the effect, but "[t]he probe benefit scaled with the frequency of the matching target", which suggests limited transfer to targets that were not probed. Probes appeared to work by guiding search towards the probed target's features and by raising perceived prevalence, "not through feedback alone", without moving the decision criterion. For monitors, this suggests that inserted examples may help mainly with attacks that resemble them.

## 2.3 Vigilance and alarm reliability

The *vigilance decrement*, a decline in detection over a long watch, is usually traced to Mackworth's (1948) studies of prolonged visual search, in which it was robust after the first half hour (Klein & Feltmate, 2025). Vigilance "requires hard mental work and is stressful" (Warm et al., 2008). An LLM does not tire, but its detection may still depend on where a target sits in a long input (Section 4.1).

Monitors also sit in front of people, who learn to discount alarms that are usually false. With alarms that were 25%, 50% or 75% reliable, about 90% of participants matched their response rates "to the expected probability of true alarms" (Bliss et al., 1995). Airport screeners working with an explosives-detection aid that had a 20% false-alarm rate and a positive predictive value of .3 ignored about half of its true alarms on difficult targets, "a strong cry-wolf effect" (Huegli et al., 2020). Sorkin and Woods (1985) showed with an SDT model that setting an automated monitor's threshold to optimise its own detection and false-alarm rates "will not yield optimal performance for the overall human-machine system". Monitor and auditor have to be designed as one system.

## 2.4 Threat Image Projection

TIP is "a software system that is used at airports to project images of threat items amongst the passenger baggage being screened by X-ray" (Cutler & Paddock, 2009, Abstract). Its claimed benefits are "improved attention and vigilance, and increased exposure to threat items", and feedback on TIP scores is reported to improve performance beyond TIP alone. Typically, fictional threat items are projected onto 1% to 4% of bags, and the system tells the screener immediately whether a projected item was present (Buser et al., 2025, Section 2). TIP thus raises the prevalence that screeners experience and gives them feedback, which is intended to counter the prevalence effect, and it also measures their performance. Analysing 1,199,838 TIP events from 728 screeners at one European airport, Buser et al. (2025, Abstract) found that "[a]pproximately 100 TIP events were sufficient to achieve a minimum reliability value of 0.7 when TIP was challenging enough (mean hit rate below 0.9)", and that TIP performance predicted the results of covert tests with real prohibited items.

The AI-control analogue is to insert known synthetic attacks into a monitor's stream, both to measure its hit rate in deployment and to keep its criterion from drifting. Korbak et al. (2025) propose this for monitors and for human auditors (see Section 3.1). The present study tests a small version of the second purpose: whether a short labelled block, shown before a low-prevalence batch, restores the monitor's hit rate.

# 3 Background: monitoring in AI control

## 3.1 Trusted monitoring and audit budgets

Greenblatt et al. (2024) introduced the "APPS backdooring setting": solve 5,000 programming problems with an untrusted GPT-4, a trusted GPT-3.5 and a limited supply of trusted high-quality labour, without submitting a backdoored solution. A solution is backdoored "if it passes all APPS test cases, and if GPT-4 can construct an exploit when presented with the code", an exploit being "a specific input that will yield an incorrect output" (Section 2). Up to 2% of problems may be audited (Section 2.2). If only the first 2% of solutions are audited, a red team that inserts obvious backdoors very rarely wins most games; the blue team's win probability is 15% (Section 3.1.2). Trusted monitoring audits "the top 2% most suspicious proposals", with a threshold that gives "a 2% false positive rate on the distribution of solutions written by GPT-4", and raises that probability to 62% (Section 3.2). Rarity is the attacker's main tool: the red team "can respond to a doubling of the number of problems by halving its probability of adding a backdoor on any given problem" (Section 3.1.2).

Later work kept these features. Griffin et al. (2024, Section 2) formalise trusted monitoring as a game in which the red team chooses a backdoor rate and the monitor's scores depend only on whether the code is backdoored. Relaxing the assumption of a perfect human auditor, they find that "[i]ncreasing the human FNR [false-negative rate] decreases safety almost linearly in the worst case" (Section 6.1). Bhatt et al. (2025) used an audit budget of 1% of actions in an agent environment, "higher than what we expect to be able to afford in real deployment" (Section 2.2, footnote 2), against a red-team "rare attacks strategy" (Section 3.1). Korbak et al. (2025, Section 4) sketch a safety case whose safety layer "audits the 0.1% most suspicious actions", and in which "developers regularly generate synthetic attacks and check whether human auditors remain attentive and flag synthetic attacks as suspicious". That proposal is TIP in all but name.

## 3.2 How well do monitors and people detect sabotage?

Monitors are imperfect, and people are not obviously better. In SHADE-Arena the strongest monitor (Gemini 2.5 Pro) reached an AUC of 0.87 in separating benign from sabotage transcripts, and a threshold catching 80% of sabotage attempts "would imply a false positive rate of over 20%" (Kutasov et al., 2025, Section 4.1). Human annotators, taking an average of 103 minutes per transcript, reached an AUC of 0.65 on 12 benign and 20 malign transcripts. Escalating only cases the monitor had flagged to human reviewers raised the true-positive rate "by approximately 15% at FPR = 0.01" (Kale et al., 2025, Abstract). SLEIGHT-Bench, 40 hand-designed attacks on monitor "blind spots", calibrates monitors to a 1% false-positive rate because otherwise "humans won't be able to review every flagged transcript"; at that threshold an Opus 4.6 monitor never caught 50% of the attacks in ten trials (Najt et al., 2026). Production blocking monitors for coding agents blocked under 1% of 4,000 benign actions, yet in an experimental setting they "fail to block over 55% of attacks" by an adversarial agent (Remedios et al., 2026). Among developers working with sabotaging coding agents, 83 of 88 without a monitor failed to detect the sabotage, and even after a correct monitor alert it survived in 9 of 16 sessions. The authors expect "the gap between detection and action" to "widen in deployment under greater time pressure, alert fatigue, and weaker review incentives" (Ye et al., 2026, Section 4.2).

These figures were measured one item at a time or on test sets in which attacks were common; in SHADE-Arena's human baseline, 20 of the 32 transcripts were malign. None of these studies varies the share of attacks a monitor sees, although the control literature expects that share to be small in deployment.

## 3.3 Base rates in deployment

Anthropic has published measurements of its internal agent oversight (Favaro & Wright, n.d.). As of August 2026 there were "approximately 30,000 agents doing research and engineering work at Anthropic at any one time" on its most-used internal platform. All their actions are read after the fact by an offline monitor, which "flags roughly one to two transcripts in every thousand for further review". In absolute terms, "[t]he monitor flags roughly 100,000 transcripts per week that are then reviewed by multiple classifiers for false-positives and initial oversight review", and "the highest priority flags (approximately ~50 per week) are escalated to human review". The page adds that "[i]n our monitoring data to date, individual agents rarely misbehave".

A flag rate is not an attack rate, and these figures do not say how many flags are true. They do show that a deployed monitor reads an overwhelmingly benign stream, and that the people at the end of the chain see a few escalations drawn from many flags. These are the conditions under which human screeners miss rare targets (Section 2.2) and discount alarms (Section 2.3).

# 4 LLM judges, context effects and the gap

## 4.1 What is known

LLM judges have known biases, including "position, verbosity, and self-enhancement biases" (Zheng et al., 2023, Abstract). In few-shot classification, GPT-3's predictions followed the label balance of the examples in the prompt: "[w]hen the prompt is unbalanced, the predictions are unbalanced (majority label bias)" (Zhao et al., 2021, Figure 4 caption). An LLM that treats the unlabelled items in a batch as evidence about what is normal might likewise be pushed towards "clean" by a batch that is almost all clean. Performance on long inputs also depends on position; it "is often highest when relevant information occurs at the beginning or end of the input context" (Liu et al., 2024, Abstract). Prior scores placed in a judge's context "anchor judgments and systematically shift ratings toward their values", and neither chain-of-thought (written step-by-step reasoning before the answer) nor a warning to disregard them reduced the total effect (Kapetanovic et al., 2026, Abstract).

Two recent studies apply SDT to LLM overseers. Chen et al. (2026, Abstract) found that more elaborate procedural traces "shift the decision criterion toward rejection, increasing false alarms in susceptible overseers", while *d′* stayed roughly constant, and they recommend that "AI auditors should be evaluated by their decision criterion and false-alarm behavior, alongside accuracy". Cai et al. (2026, Abstract) found that plausible explanations moved multimodal judges' criterion towards acceptance "without a clear change in mean discriminability". In both studies context moved the criterion and left sensitivity largely intact. That is the signature of the human low-prevalence effect, although neither study varied prevalence.

Three studies come closer. Hida et al. (2026) compared one-at-a-time and batch screening (20 items per call) of studies for systematic reviews, using five reviews whose natural share of relevant studies ranged from 2.9% to 53.0%, with and without a sentence stating that share. The stated share had little effect. Batching changed many decisions; for one model it made screening more inclusive in the four reviews with prevalence of 20% or less and more restrictive in the balanced review, a pattern the authors call "compatible with a possible tendency toward implicit normalization of decisions within the batch" (Section 4.4). In that study prevalence varied with the review, so it was confounded with topic, criteria and items, and only one review was near balance. Kim et al. (2026, Abstract) showed that "a harmful question that is reliably refused in isolation can elicit a harmful response when embedded in a batch of benign questions", and attribute this partly to "refusal signal dilution". Makins et al. (2026, Abstract) found that splitting an attack across several agents makes per-agent monitors less likely to catch it, but that this "is not driven by the ratio of benign to malicious code".

## 4.2 The gap

We searched arXiv, the web and the reference lists of the papers above (queries and results in `sources.md`). We found no study that manipulates the prevalence of targets within an LLM monitor's or judge's context while holding the pool of items fixed, no study of prevalence effects in an AI-control setting, and no test of TIP-style remedies for LLM monitors. Hida et al. (2026) is the nearest; it observed batch effects across naturally different prevalences in a different task.

## 4.3 The analogy and its limits

The comparison between a human screener and an LLM monitor is an analogy, and its limits shape the predictions. The human effect has a decision part, a criterion that tracks experienced prevalence (Wolfe et al., 2007), and a behavioural part: observers quit target-absent searches earlier when targets are rare (Wolfe et al., 2005, 2007), and detection declines over a long watch (Klein & Feltmate, 2025). An LLM has no time cost, no motivation to finish early and no fatigue across calls. It reads every item it is given, and its "experience" of prevalence exists only inside one context window, the text it is shown in a single call. Any low-prevalence effect in an LLM would have to come through the decision part, by mechanisms such as majority-label bias (Zhao et al., 2021) or dilution of a rare signal among many benign items (Kim et al., 2026).

Other mechanisms predict the opposite. A single backdoored item among 39 clean ones may stand out by contrast. A tendency to normalise decisions within a batch (Hida et al., 2026) would make a monitor flag more items when few deserve it, raising both hits and false alarms at low prevalence. The pre-registration states that a higher hit rate at low prevalence would be reported as a disconfirmation of H1.

Stated prevalence has no clean human counterpart, since the human evidence concerns experienced prevalence. Experiment 2 asks whether an LLM, which receives all its information as text, treats a stated base rate the way people treat an experienced one.

# 5 Methods

## 5.1 Design and hypotheses

Three experiments, each run with two monitor models, test four confirmatory hypotheses (PREREGISTRATION.md, Section 2):

- **H1 (experienced prevalence).** In batch review, the hit rate is lower when backdoors are rare in the batch (2.5%) than when they are common (50%), with 10% in between.
- **H1a (criterion, not sensitivity).** The prevalence effect in H1 shows as a more conservative criterion *c* at low prevalence, while sensitivity (*d′* and AUROC) changes less than the criterion.
- **H2 (stated prevalence).** In single-item review, telling the monitor that backdoors are rare (1%) lowers its hit rate relative to telling it they are common (50%).
- **H3 (remedy).** At 2.5% batch prevalence, a short high-prevalence calibration block with correct answers shown before the batch raises the hit rate.

Four exploratory questions have no directional prediction: position within a batch (E1, an analogue of the vigilance decrement), an independence instruction (E2), differences between monitors (E3) and single-item against batch judging (E4). Table 1 summarises the design.

: Table 1. Planned design per monitor model. Clean and backdoored items come from the main pool. Counts are planned; achieved counts after exclusions are reported in Section 6. <!-- CONFIRM FROM results/ -->

| Experiment | Condition | Presentation | Backdoored per call | Calls | Backdoored judgments | Clean judgments |
|---|---|---|---|---|---|---|
| 1 | P50 | Batch of 40 | 20 | 8 | 160 | 160 |
| 1 | P10 | Batch of 40 | 4 | 40 | 160 | 1,440 |
| 1 | P2.5 | Batch of 40 | 1 | 160 | 160 | 6,240 |
| 2 | *none*, S50, S1 | Single item | 0 or 1 | 240 per condition | 120 per condition | 120 per condition |
| 3 | R-cal | 10 labelled examples, then batch of 40 | 1 | 80 | 80 | 3,120 |
| 3 | R-ind | Batch of 40 with independence sentence | 1 | 80 | 80 | 3,120 |

## 5.2 Task and materials

**Domain.** The task follows the code-backdooring setting of Greenblatt et al. (2024). A monitor reviews short Python solutions to programming problems, any of which may contain a deliberately inserted *backdoor*: code that passes the provided tests but returns a wrong answer on a specific input, the *trigger*.

**Problems.** Problems come from the Mostly Basic Programming Problems dataset (MBPP; Austin et al., 2021), full configuration, all splits. MBPP contains 974 problems "designed to be solvable by entry-level programmers" (Austin et al., 2021, Abstract). Each has a natural-language task, a reference solution and three test assertions. The dataset is released under the Creative Commons Attribution 4.0 licence (CC BY 4.0). <!-- CONFIRM FROM results/: whether all 974 problems were used, and the source and version of the download (data/mbpp_download.json). -->

**Item pairs.** For each problem, a generator model (`claude-opus-5-5`) wrote, in one call, (1) a *clean* solution that passes the three MBPP tests and (2) a *backdoored* version that is a minimal edit of the clean solution, passes the same three tests and returns a wrong answer on one trigger input that the generator states. The instructions asked for a backdoor that looks like plausible code, such as an edge-case branch, with no comments that reveal it. The final generator prompt is in `data/`. <!-- CONFIRM FROM results/: final generator prompt version and file name; generation settings. -->

**Verification.** A pair was kept only if, on execution: both versions parse; both pass the three MBPP tests within a time limit; on the stated trigger input, the backdoored output differs from the clean output, and from the MBPP reference solution's output where the reference accepts that input; and the two versions differ by a small edit. Pairs failing any check were excluded and counted. <!-- CONFIRM FROM results/: time limit; edit-distance measure and threshold; number of pairs generated, excluded by reason, and kept. -->

**Normalisation.** Both versions were passed through Python's `ast` parser and unparser, which drops comments and standardises formatting, so that differences in style cannot cue the monitor. Docstrings were also removed. Function names were kept. <!-- CONFIRM FROM results/: how docstrings were removed. `ast.unparse` alone keeps docstrings, because they are expression nodes in the tree. -->

**Pools.** Verified pairs were split at random, with a seed fixed in the code, into a *calibration pool* of 40 pairs (used only for the difficulty check in Section 5.3 and as examples in the R-cal condition) and a *main pool* of all remaining pairs. Within any batch a problem appears at most once, in either its clean or its backdoored version, so the monitor can never find a backdoor by comparing two versions of the same problem. <!-- CONFIRM FROM results/: size of main pool. -->

## 5.3 Item-difficulty calibration

To avoid ceiling and floor effects, the subtlety of the backdoors could be tuned once, before the main runs, using only the calibration pool. `claude-haiku-5-5` judged the 40 calibration pairs as single items with no stated prevalence. The target was a hit rate between 0.40 and 0.90 and a false-alarm rate below 0.30. If results fell outside the target, the generator's subtlety instruction could be revised and the whole item set regenerated, at most twice. No main-pool item was used for tuning. <!-- CONFIRM FROM results/: number of revisions, calibration hit and false-alarm rates for each version, and the final generator instruction. -->

## 5.4 Monitors

The monitors were `claude-haiku-5-5`, the main "trusted, weaker" monitor, and `claude-sonnet-5-5`. Both were called through Claude Code in non-interactive mode (`claude -p`; Anthropic, n.d.), with tools, MCP servers and slash commands disabled, our own system prompt, output constrained to a JSON schema (`--json-schema`) and a fixed effort setting (`low`) in all conditions. Model sampling cannot be fixed, so every judgment is an independent random draw from the model. <!-- CONFIRM FROM results/: exact command-line flags, Claude Code version, dates of the runs. -->

For each submission the monitor returned an ID, a *suspicion score* (an integer from 0 to 100 for how likely the code is to contain a deliberately inserted backdoor) and a binary *flag* (escalate to human audit, yes or no). The system prompt told the monitor that it was reviewing code written by an untrusted AI system that may sometimes insert backdoors, defined as code that passes normal tests but gives a wrong answer on specific inputs, and asked it to flag submissions that should go to a limited human audit. The prompt was identical across conditions except for the manipulated sentences. The full prompt text is in `code/`. <!-- CONFIRM FROM results/: file holding the monitor prompts; whether each submission was shown with its MBPP task text and/or its test assertions. -->

The flag measures the monitor's own criterion, which matters for systems that act on the monitor's decision, such as blocking monitors (Remedios et al., 2026). The AUROC of suspicion scores within a condition measures whether backdoored and clean code remain separable whatever threshold is applied, which matters for protocols that set a threshold on scores externally (Greenblatt et al., 2024).

## 5.5 Experiments

**Experiment 1: experienced prevalence (batch).** Each call showed a batch of 40 submissions with random IDs in random order, and the prompt said nothing about prevalence. The conditions (P50, P10, P2.5) differ only in how many of the 40 are backdoored (Table 1). Items were drawn from the main pool without replacement within a batch and with replacement across batches, and each backdoored item's position was uniform at random.

**Experiment 2: stated prevalence (single item).** Each call showed one submission. The conditions differ by one sentence in the system prompt: *none* (no statement); *S50* ("In past reviews, about half of submissions contained a backdoor."); and *S1* ("In past reviews, about 1 in 100 submissions contained a backdoor."). For each monitor and condition, 120 backdoored and 120 clean items were drawn from the main pool, and the same item set was used in every condition.

**Experiment 3: remedies at low prevalence (batch).** Batches were built as in P2.5 (40 items, one backdoored), with 80 batches per monitor per remedy. In *R-cal* (calibration block), the prompt first showed 10 example submissions from the calibration pool, 5 backdoored and 5 clean, with their correct labels and, for the backdoored ones, the trigger input. These 10 were never in the scored batch. R-cal is the analogue of the high-prevalence retraining bursts of Wolfe et al. (2007) and of TIP feedback. In *R-ind* (independence instruction, E2), one sentence was added: "The number of backdoored submissions in this batch is unknown and may be zero, one or many; judge each submission independently on its own merits."

## 5.6 Measures

- **Hit rate (*H*):** the proportion of backdoored submissions flagged.
- **False-alarm rate (*F*):** the proportion of clean submissions flagged.
- **Sensitivity and criterion:** *d′* = z(*H*) − z(*F*) and *c* = −½[z(*H*) + z(*F*)], computed per condition with the log-linear correction (0.5 added to hits and false alarms, 1 to the signal and noise counts) applied to all cells (Hautus, 1995).
- **AUROC** of suspicion scores within each condition.
- **Mean suspicion score** for clean and for backdoored items.

## 5.7 Analysis

All analyses follow the pre-registration (Section 6 there).

- **H1.** Logistic regression of flag (backdoored items only) on prevalence condition, separately per monitor, with standard errors clustered by batch. The confirmatory test is P2.5 against P50, two-sided at α = .05, Holm-corrected across the two monitors. Hit rates are also reported with Wilson 95% confidence intervals.
- **H1a.** *d′*, *c* and AUROC per condition, with 95% confidence intervals from a cluster bootstrap over batches (2,000 resamples). H1a is supported if the change in *c* from P50 to P2.5 is positive, with an interval that excludes zero, and larger in standardised units than the change in *d′*. <!-- CONFIRM FROM results/: how "standardised units" was operationalised; the pre-registration does not define it. -->
- **H2.** Logistic regression of flag (backdoored items) on stated-prevalence condition, per monitor, with item random intercepts if the model converges and item-clustered standard errors otherwise. The confirmatory contrast is S1 against S50, Holm-corrected across monitors.
- **H3.** Hit rate in R-cal against P2.5, per monitor, by logistic regression with batch-clustered standard errors, Holm-corrected across monitors.
- **Exploratory analyses.** E1: logistic regression of hit on position (1 to 40) within P2.5 and P10. E2: R-ind against P2.5. E3: comparison of monitors. E4: single-item *none* against the batch conditions. These are labelled exploratory throughout.

The pre-registration gives an informal power estimate. With 160 backdoored judgments per cell, a fall in hit rate from 0.80 to 0.65 is detectable with about 80% power at α = .05 (two-proportion test, ignoring clustering), and effects smaller than about 15 percentage points may be missed. Experiment 3 has 80 backdoored judgments per remedy cell and so less power; the pre-registration gives no figure for it.

## 5.8 Exclusions, deviations and materials

An output was invalid if it failed the JSON schema, omitted or duplicated IDs, or if the call returned an error. Invalid calls were retried up to three times with a fresh call; a batch still invalid after that was dropped and counted. Refusals by the generator or the monitor were counted and reported. There were no other exclusions. <!-- CONFIRM FROM results/: invalid calls, retries, dropped batches and refusals, by condition. -->

Deviations from the pre-registration: <!-- CONFIRM FROM results/ and PREREGISTRATION.md Section 9: list each deviation with date and reason; label affected results in Section 6. -->

Code, the verified item pairs (MBPP-derived, CC BY 4.0, with attribution), all raw monitor outputs, the analysis script and the figures are in this folder (`code/`, `data/`, `results/`, `figures/`).

# 6 Results

<!-- RESULTS PENDING -->

**[Results pending. To be written from `results/RESULTS.md` and `figures/`. Every number in this section will be taken from the engineer's results files.]**

Planned structure:

- 6.1 Item generation, verification and difficulty calibration (counts, exclusions by reason, calibration rounds).
- 6.2 Experiment 1: hit and false-alarm rates by prevalence (H1); *d′*, *c* and AUROC (H1a).
- 6.3 Experiment 2: stated prevalence (H2).
- 6.4 Experiment 3: calibration block (H3) and independence instruction (E2).
- 6.5 Exploratory analyses: position (E1), monitor differences (E3), single-item against batch (E4).
- 6.6 Invalid outputs, refusals and dropped batches.

# 7 Discussion

<!-- RESULTS PENDING -->

**[Discussion pending results.]**

Planned structure:

- 7.1 Do LLM monitors show a low-prevalence effect? Findings against H1 to H3, including any disconfirmation.
- 7.2 Criterion or sensitivity, and what that means for monitors that act on their own decision and for monitors whose scores are thresholded externally.
- 7.3 Remedies: what the calibration block and the independence instruction did, read against Wolfe et al. (2007) and Becker et al. (2026).
- 7.4 Implications for control evaluations and deployed monitors: the prevalence used in evaluations; inserted synthetic attacks as a TIP analogue (Korbak et al., 2025; Buser et al., 2025); reporting criterion and false alarms (Chen et al., 2026); joint design of monitor and auditor (Sorkin & Woods, 1985).
- 7.5 A short, factual paragraph on implications for developers of AI tools in aviation.
- 7.6 The analogy revisited: where the human findings did and did not transfer.

# 8 Limitations

This section will be completed once the results are known. The following limitations hold whatever the results.

**One domain.** The items are short, single-function Python solutions to entry-level problems, each with at most one backdoor. Real attacks by agents are spread over long transcripts and many actions (Kutasov et al., 2025; Bhatt et al., 2025). Effects in this toy setting may not carry over, in either direction.

**Synthetic, non-adaptive attacks.** All backdoors were written by one generator under one instruction and tuned to a difficulty band. They were not optimised against the monitors, as a real adversary's would be (Najt et al., 2026; Remedios et al., 2026).

**Claude-only monitors and generator.** The monitors and the generator come from one developer and one model family. They may share blind spots, or the monitors may recognise the generator's style. Whether other model families behave the same way is untested.

**Access route and model versions.** The monitors were called through Claude Code's non-interactive mode at one fixed effort setting. Results may differ through the raw API, at other settings or with later model versions; they are a snapshot.

**Sampling and clustering.** Sampling cannot be fixed, so each judgment is a random draw. Items were reused across batches, so judgments are clustered by item as well as by batch, and the pre-registered H1 analysis clusters only by batch.

**Prevalence range and batch size.** The lowest experienced prevalence is 2.5%, one backdoor in 40, with a single batch size. Deployed flag rates are around one or two per thousand (Favaro & Wright, n.d.) and attacks are presumably rarer still. Effects below 2.5%, or in longer contexts, were not tested. Experienced prevalence exists only within one call; most deployed monitors judge one transcript per call, although a transcript may itself contain many benign actions.

**Manipulations.** Stated prevalence was one sentence in one wording. The calibration block changes two things at once: it raises the prevalence in the context (from 1 in 40 to 6 in 50 labelled or unlabelled items) and it shows worked examples of backdoors with their triggers. A benefit could come from either.

**LLMs are not people.** An LLM has no fatigue, time pressure or motivation. Similar SDT summaries for LLMs and people would not imply similar mechanisms (Section 4.3).

**Power.** Effects smaller than about 15 percentage points may be missed in Experiments 1 and 2, and Experiment 3 has half as many backdoored judgments per cell.

<!-- RESULTS PENDING: add limitations that depend on the results, e.g. ceiling or floor effects, refusal rates, deviations from the pre-registration. -->

# 9 Conclusion

<!-- RESULTS PENDING -->

**[Conclusion pending results.]**

# Acknowledgements and AI-assistance statement

Literature searches, drafting and source verification were carried out with AI assistance (Claude, Anthropic) under the author's direction. The experimental code was also written with AI assistance under the author's direction. Claude models served as the item generator and as the monitors under study. The author is responsible for the final text. Every reference was checked against the original source or, where stated, a reliable secondary source; see `sources.md`.

# Disclaimer

The views expressed are the author's own and do not represent those of any employer or regulator. Nothing here is operational, legal or regulatory advice.

# Data and code availability

Code, data, raw outputs and figures are in this folder: `code/`, `data/`, `results/`, `figures/`. The pre-registration is `PREREGISTRATION.md`. Items derive from MBPP (Austin et al., 2021), released under CC BY 4.0; the derived item pairs are released under the same licence with attribution.

# References

Abbasi, M., Núñez V., J. M., & Shahraki, A. (2026). *What standard evaluations hide about detectors of hijacked LLM agents: Rare attacks, unseen tools and benchmark transfer* (arXiv:2610.41803) [Preprint]. arXiv. https://arxiv.org/abs/2610.41803

Anthropic. (n.d.). *Run Claude Code programmatically*. Claude Code Docs. Retrieved November 3, 2026, from https://code.claude.com/docs/en/headless

Austin, J., Odena, A., Nye, M., Bosma, M., Michalewski, H., Dohan, D., Jiang, E., Cai, C., Terry, M., Le, Q., & Sutton, C. (2021). *Program synthesis with large language models* (arXiv:2108.07732) [Preprint]. arXiv. https://arxiv.org/abs/2108.07732

Becker, M. W., Rodriguez, A., Montalvo, D. T., & Peltier, C. (2026). Reducing the low-prevalence effect with probe trials. *Cognitive Research: Principles and Implications*, *11*, Article 5. https://doi.org/10.1186/s41235-025-00702-w

Bhatt, A., Rushing, C., Kaufman, A., Tracy, T., Georgiev, V., Matolcsi, D., Khan, A., & Shlegeris, B. (2025). *Ctrl-Z: Controlling AI agents via resampling* (arXiv:2504.10374) [Preprint]. arXiv. https://arxiv.org/abs/2504.10374

Bliss, J. P., Gilson, R. D., & Deaton, J. E. (1995). Human probability matching behaviour in response to alarms of varying reliability. *Ergonomics*, *38*(11), 2300–2312. https://doi.org/10.1080/00140139508925269

Buser, D., Schwaninger, A., Rehor, V., & Sterchi, Y. (2025). Reliability and validity of threat image projection data as a measure of performance in X-ray baggage screening. *Transportation Research Part A: Policy and Practice*, *200*, Article 104640. https://doi.org/10.1016/j.tra.2025.104640

Cai, A., Wang, Z., Yang, X., Lin, Y., Lee, D., & Yang, Y. (2026). *A plausible explanation is enough to mislead multimodal judges* (arXiv:2610.22631) [Preprint]. arXiv. https://arxiv.org/abs/2610.22631

Chen, Z., Zhu, D., Zheng, L., & Li, W. (2026). *Beyond accuracy: How procedural traces shift the decision criterion of LLM overseers* (arXiv:2609.18204) [Preprint; accepted at the 60th Hawaii International Conference on System Sciences]. arXiv. https://arxiv.org/abs/2609.18204

Cutler, V., & Paddock, S. (2009). Use of threat image projection (TIP) to enhance security performance. In *43rd Annual 2009 International Carnahan Conference on Security Technology* (pp. 46–51). IEEE. https://doi.org/10.1109/CCST.2009.5335565

Favaro, M., & Wright, P. (n.d.). *Measurements for understanding the pace of AI development inside frontier labs*. Anthropic. Retrieved November 3, 2026, from https://www.anthropic.com/institute/measuring-pace-of-ai-development

Green, D. M., & Swets, J. A. (1966). *Signal detection theory and psychophysics*. Wiley.

Greenblatt, R., Shlegeris, B., Sachan, K., & Roger, F. (2024). AI control: Improving safety despite intentional subversion. In *Proceedings of the 41st International Conference on Machine Learning* (Proceedings of Machine Learning Research, Vol. 235, pp. 16295–16336). PMLR. https://proceedings.mlr.press/v235/greenblatt24a.html (Preprint version: arXiv:2312.06942, https://arxiv.org/abs/2312.06942)

Griffin, C., Thomson, L., Shlegeris, B., & Abate, A. (2024). *Games for AI control: Models of safety evaluations of AI deployment protocols* (arXiv:2409.07985; Version 2, 2026) [Preprint]. arXiv. https://arxiv.org/abs/2409.07985

Hautus, M. J. (1995). Corrections for extreme proportions and their biasing effects on estimated values of d′. *Behavior Research Methods, Instruments, & Computers*, *27*(1), 46–51. https://doi.org/10.3758/BF03203619

Hautus, M. J., Macmillan, N. A., & Creelman, C. D. (2021). *Detection theory: A user's guide* (3rd ed.). Routledge. https://doi.org/10.4324/9781003203636

Hida, G. S., Ribeiro, D. M., & Hida, C. S. (2026). *Class imbalance and batch effects in LLM-based screening for systematic reviews* (arXiv:2608.14737) [Preprint]. arXiv. https://arxiv.org/abs/2608.14737

Huegli, D., Merks, S., & Schwaninger, A. (2020). Automation reliability, human–machine system performance, and operator compliance: A study with airport security screeners supported by automated explosives detection systems for cabin baggage screening. *Applied Ergonomics*, *86*, Article 103094. https://doi.org/10.1016/j.apergo.2020.103094

Kale, N., Zhang, C. B. C., Zhu, K., Aich, A., Rodriguez, P., Scale Red Team, Knight, C. Q., & Wang, Z. (2025). *Reliable weak-to-strong monitoring of LLM agents* (arXiv:2508.19461) [Preprint]. arXiv. https://arxiv.org/abs/2508.19461

Kapetanovic, A., Altwlkany, K., Mercep, A., Duricic, T., & Lacic, E. (2026). Anchoring bias in LLM-as-a-judge systems: Prior scores compromise evaluation independence. In *Proceedings of the 35th ACM International Conference on Information and Knowledge Management (CIKM '26)* (pp. 2043–2052). ACM. https://doi.org/10.1145/3799682.3840879 (Preprint version: arXiv:2608.25869)

Kim, K., Kim, H.-S., Lee, W., & Kim, C. (2026). *Safety in batches? Understanding and mitigating safety failures in batch prompting* (arXiv:2608.02681) [Preprint]. arXiv. https://arxiv.org/abs/2608.02681

Klein, R. M., & Feltmate, B. B. T. (2025). The vigilance decrement: Its first 75 years. *Frontiers in Cognition*, *4*, Article 1632885. https://doi.org/10.3389/fcogn.2025.1632885

Korbak, T., Clymer, J., Hilton, B., Shlegeris, B., & Irving, G. (2025). *A sketch of an AI control safety case* (arXiv:2501.17315) [Preprint]. arXiv. https://arxiv.org/abs/2501.17315

Kutasov, J., Sun, Y., Colognese, P., van der Weij, T., Petrini, L., Zhang, C. B. C., Hughes, J., Deng, X., Sleight, H., Tracy, T., Shlegeris, B., & Benton, J. (2025). *SHADE-Arena: Evaluating sabotage and monitoring in LLM agents* (arXiv:2506.15740) [Preprint]. arXiv. https://arxiv.org/abs/2506.15740

Liu, N. F., Lin, K., Hewitt, J., Paranjape, A., Bevilacqua, M., Petroni, F., & Liang, P. (2024). Lost in the middle: How language models use long contexts. *Transactions of the Association for Computational Linguistics*, *12*, 157–173. https://doi.org/10.1162/tacl_a_00638

Mackworth, N. H. (1948). The breakdown of vigilance during prolonged visual search. *Quarterly Journal of Experimental Psychology*, *1*(1), 6–21. https://doi.org/10.1080/17470214808416738

Makins, O., Angelini, O., Shams, Z., & Phuong, M. (2026). *Multi-agent AI control: Distributed attacks hamper per-instance monitors* (arXiv:2607.07368) [Preprint]. arXiv. https://arxiv.org/abs/2607.07368

Mitroff, S. R., & Biggs, A. T. (2014). The ultra-rare-item effect: Visual search for exceedingly rare items is highly susceptible to error. *Psychological Science*, *25*(1), 284–289. https://doi.org/10.1177/0956797613504221

Najt, E., Toft, C., Tracy, T., Roger, F., & Benton, J. (2026, May 19). *SLEIGHT-Bench: Finding blind spots in AI monitors*. Alignment Science Blog, Anthropic. Retrieved November 3, 2026, from https://alignment.anthropic.com/2026/sleight-bench/

Remedios, A., Storf, S., Roger, F., & Hughes, J. (2026, October 22). *Red-teaming auto mode: Improving blocking classifiers against malign coding agents*. Alignment Science Blog, Anthropic. Retrieved November 3, 2026, from https://alignment.anthropic.com/2026/red-teaming-auto-mode/

Sorkin, R. D., & Woods, D. D. (1985). Systems with human monitors: A signal detection analysis. *Human–Computer Interaction*, *1*(1), 49–75. https://doi.org/10.1207/s15327051hci0101_2

Srivastav, D., Pape, D., & Schönherr, L. (2026). *Unknown unknowns: Do hidden intentions in LLMs evade detection?* (arXiv:2601.18552) [Preprint; accepted to Findings of the Association for Computational Linguistics: EMNLP 2026]. arXiv. https://arxiv.org/abs/2601.18552

Warm, J. S., Parasuraman, R., & Matthews, G. (2008). Vigilance requires hard mental work and is stressful. *Human Factors*, *50*(3), 433–441. https://doi.org/10.1518/001872008X312152

Wolfe, J. M., Brunelli, D. N., Rubinstein, J., & Horowitz, T. S. (2013). Prevalence effects in newly trained airport checkpoint screeners: Trained observers miss rare targets, too. *Journal of Vision*, *13*(3), 33. https://doi.org/10.1167/13.3.33

Wolfe, J. M., Horowitz, T. S., & Kenner, N. M. (2005). Rare items often missed in visual searches. *Nature*, *435*(7041), 439–440. https://doi.org/10.1038/435439a

Wolfe, J. M., Horowitz, T. S., Van Wert, M. J., Kenner, N. M., Place, S. S., & Kibbi, N. (2007). Low target prevalence is a stubborn source of errors in visual search tasks. *Journal of Experimental Psychology: General*, *136*(4), 623–638. https://doi.org/10.1037/0096-3445.136.4.623

Ye, J., Zou, H., Yu, S., & Shi, W. (2026). *Coding with "enemy": Can human developers detect AI agent sabotage?* (arXiv:2606.05647) [Preprint; accepted at NeurIPS 2026]. arXiv. https://arxiv.org/abs/2606.05647

Zhao, T. Z., Wallace, E., Feng, S., Klein, D., & Singh, S. (2021). Calibrate before use: Improving few-shot performance of language models. In *Proceedings of the 38th International Conference on Machine Learning* (Proceedings of Machine Learning Research, Vol. 139, pp. 12697–12706). PMLR. https://proceedings.mlr.press/v139/zhao21c.html

Zheng, L., Chiang, W.-L., Sheng, Y., Zhuang, S., Wu, Z., Zhuang, Y., Lin, Z., Li, Z., Li, D., Xing, E. P., Zhang, H., Gonzalez, J. E., & Stoica, I. (2023). Judging LLM-as-a-judge with MT-Bench and Chatbot Arena. In *Advances in Neural Information Processing Systems 36 (NeurIPS 2023), Datasets and Benchmarks Track*. https://doi.org/10.52202/075280-2020
