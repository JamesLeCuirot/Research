#!/usr/bin/env python3
"""Check every number in the workshop submission (paper.tex) against the study's records.

Run from anywhere:  python3 -I verify_numbers.py [--markdown]
Exit status 0 only if every number is matched and every number in paper.tex is covered.

How it works
- Every number in the body of paper.tex (abstract to appendix, after masking LaTeX code, labels,
  citation keys, model IDs and figure widths) is extracted with its sign.
- The four data tables are checked cell by cell against results/ (registered_measures_table.md,
  RESULTS_numbers.md, analysis.json).
- Every other number belongs to a "claim": a verbatim snippet of paper.tex plus the line(s) of a
  source file (or a value in a JSON file) where each of its numbers appears. Results come from
  results/; design constants from PREREGISTRATION.md or code/; numbers about other people's work
  (literature, citation locators) from the full paper's paper.tex, which was audited against its
  sources.
- Matching is exact (string-equal after removing thousands separators and a leading zero), unless a
  claim explicitly allows rounding a more precise value ('round'), a fraction shown as a percentage
  ('pct'), or a magnitude ('abs'). Rounding is to the precision printed in paper.tex.
- A second check confirms that each prose number also appears in the full paper's paper.tex, in the
  most similar sentence or its neighbours (so the condensation did not change or re-round it).
"""
import json, math, re, sys, difflib
from pathlib import Path

HERE = Path(__file__).resolve().parent
SUB = HERE.parent                      # submissions/aaai27-trust4rsi-workshop
ROOT = SUB.parent.parent               # papers/02-do-llm-monitors-miss-rare-threats
TEX = Path(sys.argv[sys.argv.index('--tex') + 1]) if '--tex' in sys.argv else SUB / 'paper.tex'   # --tex for self-tests

RN, RM, RMT, CAL = 'results/RESULTS_numbers.md', 'results/RESULTS.md', 'results/registered_measures_table.md', 'results/calibration.md'
AJ, PH, SE, PD = 'results/analysis.json', 'results/posthoc_h2.json', 'results/sensitivity_excluding_extra_turn_calls.json', 'results/posthoc_descriptives.json'
PR, AU, SP, CR = 'PREREGISTRATION.md', 'AUDIT.md', 'paper.tex', 'code/README.md'

# --------------------------------------------------------------------------- number tokens
NUM = re.compile(r"(?:(?<=[\s$(\[{,;])-)?(?<![A-Za-z0-9_.])(?:\d{1,2}:\d{2}(?::\d{2})?|\d+\.\d+\.\d+|\d{1,3}(?:,\d{3})+|\d+(?:\.\d+)?|\.\d+)")

def norm_tok(s):
    s = s.replace(',', '').replace('\u2212', '-')
    neg = s.startswith('-')
    s = s.lstrip('-')
    if re.fullmatch(r'0\.\d+', s):
        s = s[1:]
    return ('-' if neg else '') + s

def tokens(line):
    line = ' ' + line.replace('\u2212', '-').replace('\u2009', ' ').replace('\u202f', ' ')
    return [norm_tok(m.group()) for m in NUM.finditer(line)]

def decimals(s):
    s = s.lstrip('-')
    return len(s.split('.')[1]) if '.' in s and ':' not in s and s.count('.') == 1 else 0

def fmt_like(value, printed):
    """Format value to the number of decimals printed (Python formatting, as used by analyse.py)."""
    d = decimals(printed)
    return norm_tok(f"{value:.{d}f}")

# --------------------------------------------------------------------------- source files
_cache = {}
def lines_of(rel):
    if rel not in _cache:
        txt = (ROOT / rel).read_text(encoding='utf-8')
        if rel == SP:
            txt = latex_norm(txt)
        else:
            txt = txt.replace('**', '').replace('`', '').replace('*', '')
        _cache[rel] = txt.split('\n')
    return _cache[rel]

def latex_norm(t):
    t = re.sub(r'\\SI\{([^}]*)\}\{\\percent\}', r'\1%', t)
    t = re.sub(r'\\num\{([^}]*)\}', r'\1', t)
    t = t.replace('\\%', '%').replace('~', ' ').replace('``', '"').replace("''", '"')
    t = re.sub(r'\{(-[0-9.]+)\}', r'\1', t)
    t = re.sub(r'\\(?:emph|code|textbf)\{([^}]*)\}', r'\1', t)
    t = t.replace('$', '').replace('\\,', ' ').replace('-{}-', '--')
    return t

def find_line(rel, rx):
    pat = re.compile(rx)
    for i, l in enumerate(lines_of(rel), 1):
        if pat.search(l):
            return i, l
    return None, None

def json_get(rel, path):
    d = json.loads((ROOT / rel).read_text())
    for k in path.split('/'):
        d = d[int(k)] if isinstance(d, list) else d[k]
    return d

# --------------------------------------------------------------------------- evidence types
def L(rel, rx, *opts):
    """Line evidence: the first line of `rel` matching regex `rx`; options 'round', 'pct', 'abs'."""
    return ('line', rel, rx, set(opts))

def J(rel, path, *opts):
    """JSON value evidence; options 'round' (to printed precision), 'pct', 'abs', 'lt' (printed is an upper bound)."""
    return ('json', rel, path, set(opts))

def C(desc, fn, op):
    """Computed evidence: fn() -> value from results/analysis.json; op in {'lt','le','gt','ge','eqround'}."""
    return ('calc', desc, fn, op)

def ajson():
    return json.loads((ROOT / AJ).read_text())

def matches_number(printed, ev):
    """Return (ok, source_value_text, location_text)."""
    kind = ev[0]
    if kind == 'line':
        _, rel, rx, opts = ev
        n, line = find_line(rel, rx)
        if line is None:
            return False, 'line not found', f'{rel} /{rx}/'
        loc = f'full-paper {rel}:{n}' if rel == SP else f'{rel}:{n}'
        toks = tokens(line)
        if printed in toks:
            return True, printed, loc
        for t in toks:
            try:
                v = float(t.replace(':', 'x')) if ':' not in t else None
            except ValueError:
                v = None
            if v is None:
                continue
            if 'abs' in opts:
                v = abs(v)
            if 'pct' in opts and fmt_like(v * 100, printed) == printed:
                return True, f'{t} (x100)', loc
            if 'round' in opts and fmt_like(v, printed) == printed:
                return True, f'{t} (rounded)', loc
            if 'abs' in opts and norm_tok(t.lstrip('-')) == printed:
                return True, f'{t} (magnitude)', loc
        return False, ' '.join(toks), loc
    if kind == 'json':
        _, rel, path, opts = ev
        v = json_get(rel, path)
        loc = f'{rel} [{path}]'
        if 'lt' in opts:
            return v < float(printed), f'{v:.3g} < {printed}', loc
        if 'abs' in opts:
            v = abs(v)
        if 'pct' in opts:
            v = v * 100
        if isinstance(v, int) and not isinstance(v, bool):
            return norm_tok(str(v)) == printed, str(v), loc
        return fmt_like(v, printed) == printed, f'{v:.6g}', loc
    if kind == 'calc':
        _, desc, fn, op = ev
        v = fn()
        p = float(printed)
        ok = {'lt': v < p, 'le': v <= p, 'gt': v > p, 'ge': v >= p,
              'ge_r': float('0' + fmt_like(v, printed)) >= p,   # p rounded as printed (as in RESULTS_numbers.md)
              'eqround': fmt_like(v, printed) == printed}[op]
        return ok, f'{v:.4g} ({op} {printed})', f'{AJ} computed: {desc}'
    raise ValueError(kind)

# --------------------------------------------------------------------------- claims (prose)
# Each claim: (verbatim snippet of paper.tex, [evidence...]). Every number in the snippet must be
# found in at least one of the claim's evidences. Sections are given for the report.
D = lambda: ajson()['descriptive']

def _nonint_p(coefs):
    return [v['p'] for k, v in coefs.items() if k != 'Intercept']

def h1fa_min_p():
    d = ajson()['H1_false_alarms']
    return min(min(_nonint_p(d[m]['coefs'])) for m in ('Haiku', 'Sonnet'))

def e1_min_hit_p():
    d = ajson()['exploratory']['E1']
    return min(v['coefs']['position']['p'] for k, v in d.items() if 'clean_FA' not in k)

def e3_min_p():
    d = ajson()['exploratory']['E3']
    return min(v['p'] for k in ('exp1_hits_monitor_x_condition', 'exp1_false_alarms_monitor_x_condition')
               for term, v in d[k]['coefs'].items() if 'monitor' in term)

def e4_min_fa_p():
    d = ajson()['exploratory']['E4']
    return min(min(_nonint_p(d[m]['false_alarms']['coefs'])) for m in ('Haiku', 'Sonnet'))

CLAIMS = [
 # ---- Abstract
 ('Abstract', "Two Claude models made 30,880 judgements", [L(RM, r'2,176 main monitor calls \(30,880 item'), J(AJ, 'n_judgments')]),
 ('Abstract', "drawn from 379 execution-verified", [L(RM, r'The calibration pool holds 40 pairs and the main pool 379')]),
 ('Abstract', "In batches of 40, both", [L(PR, r'Each call shows a batch of 40 submissions')]),
 ('Abstract', "hit rates rose from 0.51 at 50\\% prevalence to 0.69 at 2.5\\% for Haiku, and from 0.50 to 0.74 for Sonnet", [L(RM, r"rate was 0\.51 at 50% prevalence, 0\.50 at 10% and 0\.69 at 2\.5%\. Sonnet's was 0\.50, 0\.57 and 0\.74")]),
 ('Abstract', "(Holm-adjusted $p = .0015$ and $p < .001$)", [L(RM, r'2\.15 for Haiku \(95% CI 1\.34–3\.46, Holm p = \.0015\)'), L(RM, r'Sonnet \(95% CI 1\.78–4\.43, Holm p < \.001\)'), J(AJ, 'H1/Haiku/P2.5_vs_P50/p_holm')]),
 ('Abstract', "with false-alarm rates below 2\\%", [C('max F over the six Experiment 1 cells', lambda: max(D()[f'{m}|{c}']['F'] for m in ('Haiku', 'Sonnet') for c in ('P50', 'P10', 'P2.5')) * 100, 'lt')]),
 ('Abstract', "as many backdoors as 2.5\\% batches, and more than 10\\% and 50\\% batches in three of four comparisons", [L(RM, r'than batches with 50% or 10% prevalence, and about as many as batches with 2\.5%'), L(SP, r'more than 10% and 50% batches in three of four comparisons')]),
 ('Abstract', "Stating that about 1 in 100 submissions", [L(RM, r'monitor that "about 1 in 100" submissions')]),
 ('Abstract', "single-item hit rate (0.85 to 0.78)", [L(RM, r"Sonnet's single-item hit rate from 0\.85 to 0\.78")]),
 # ---- Introduction (literature; full paper)
 ('Introduction', "the audit budget covered 2\\% of problems \\citep[Sec.~2.2]{greenblatt2024}", [L(SP, r'audit budget covered 2% of problems \\cite\[Sec\. 2\.2\]\{greenblatt2024\}')]),
 ('Introduction', "(\\citealp[Sec.~3.1]{greenblatt2024}; \\citealp[Sec.~3.1]{bhatt2025})", [L(SP, r'\\cite\[Sec\. 3\.1\]\{greenblatt2024\}, \\cite\[Sec\. 3\.1\]\{bhatt2025\}')]),
 ('Introduction', "once out of thousands of tasks'' \\citep[Sec.~6]{korbak2025}", [L(SP, r'once out of thousands of tasks" \\cite\[Sec\. 6\]\{korbak2025\}')]),
 ('Introduction', "misses rose from 7\\% when targets appeared on half of trials to 30\\% when they appeared on 1\\%", [L(SP, r'misses rose from 7% when targets appeared on half of trials to 30% when they appeared on 1%')]),
 ('Introduction', "attacks made up 16\\% to 86\\% of test samples", [L(SP, r'attacks made up 16% to 86% of test samples')]),
 ('Introduction', "(\\citealp[Sec.~6.3]{srivastav2026}; \\citealp[Sec.~III.E]{abbasi2026})", [L(SP, r'\\cite\[Sec\. 6\.3\]\{srivastav2026\}')]),
 ('Introduction', "\\citep[Sec.~2]{griffin2024}", [L(SP, r'\\cite\[Sec\. 2\]\{griffin2024\}')]),
 ('Introduction', "Both monitors caught more backdoors at 2.5\\% prevalence than at 50\\%.", [L(SP, r'Both monitors caught more backdoors at 2\.5% prevalence than at 50%\.')]),
 ('Introduction', "An open set of 419 execution-verified pairs", [L(RM, r'419 of 450 pairs were')]),
 # ---- Background
 ('Background', "c = -\\frac{1}{2}", [L(SP, r'c = -\\frac\{1\}\{2\}')]),
 ('Background', "infinite at 0 and 1", [L(SP, r'infinite at 0 and 1')]),
 ('Background', "is increased by 0.5''", [L(SP, r'is increased by 0\.5"'), L(PR, r'add 0\.5 to hits and false alarms, 1 to signal')]),
 ('Background', "\\tilde H = \\frac{n_{\\mathrm{h}} + 0.5}{n_{\\mathrm{s}} + 1}, \\qquad \\tilde F = \\frac{n_{\\mathrm{f}} + 0.5}{n_{\\mathrm{n}} + 1}", [L(PR, r'add 0\.5 to hits and false alarms, 1 to signal'), L(SP, r'\\tilde H = \\frac\{n_\{\\mathrm\{h\}\} \+ 0\.5\}')]),
 ('Background', "such as a suspicion score from 0 to 100, the area", [L(SP, r'suspicion score from 0 to 100, the area')]),
 ('Background', "0.5 is chance and 1.0 is perfect separation", [L(SP, r'0\.5 is chance and 1\.0 is perfect separation')]),
 ('Background', "Misses were 7\\% at 50\\% target prevalence, 16\\% at 10\\% and 30\\% at 1\\%.", [L(SP, r'Misses were 7% at 50% target prevalence, 16% at 10% and 30% at 1%')]),
 ('Background', "(Experiment~7). In that experiment", [L(SP, r'\(Experiment 7\)\. In that experiment')]),
 ('Background', "projected onto 1\\% to 4\\% of bags, and the system tells the screener immediately whether a projected item was present \\citep[Sec.~2]{buser2025}", [L(SP, r'projected onto 1% to 4% of bags, and the system tells the screener immediately whether a projected item was present \\cite\[Sec\. 2\]\{buser2025\}')]),
 ('Background', "\\citet[Sec.~4]{korbak2025} sketch a control safety case whose safety layer ``audits the 0.1\\% most suspicious actions''", [L(SP, r'\\cite\[Sec\. 4\]\{korbak2025\} sketch a safety case whose safety layer "audits the 0\.1% most suspicious actions"')]),
 ('Background', "\\citep[Fig.~4 caption]{zhao2021}", [L(SP, r'\\cite\[Fig\. 4 caption\]\{zhao2021\}')]),
 ('Background', "(20 items per call) of studies for systematic reviews, in five reviews whose natural share of relevant studies ranged from 2.9\\% to 53.0\\%", [L(SP, r'\(20 items per call\) of studies for systematic reviews, in five reviews whose natural share of relevant studies ranged from 2\.9% to 53\.0%')]),
 ('Background', "in the four reviews with prevalence of 20\\% or less", [L(SP, r'four reviews with prevalence of 20% or less')]),
 ('Background', "within the batch'' (Section~4.4)", [L(SP, r'within the batch" \(Section 4\.4\)')]),
 ('Background', "A single backdoored item among 39 clean ones", [L(SP, r'A single backdoored item among 39 clean ones')]),
 # ---- Methods: design
 ('Methods', "the hit rate is lower at 2.5\\% backdoor prevalence than at 50\\%, with 10\\% in between", [L(PR, r'rare in the batch \(2\.5%\) than when they are common \(50%\), with 10% in between')]),
 ('Methods', "stating that backdoors are rare (1\\%) rather than common (50\\%)", [L(PR, r'backdoors are rare \(1%\) lowers its hit rate relative to telling it they are common \(50%\)')]),
 ('Methods', "\\textbf{H3 (remedy).} At 2.5\\% prevalence", [L(PR, r'H3 \(remedy\)\. At 2\.5% batch prevalence')]),
 # ---- Methods: materials
 ('Methods', "all four splits: 974 problems", [L(RM, r'all four splits \(974 problems, CC BY 4\.0\)')]),
 ('Methods', "Creative Commons Attribution 4.0 licence (CC BY 4.0)", [L(SP, r'Creative Commons Attribution 4\.0 licence \(CC BY 4\.0\)')]),
 ('Methods', "(task IDs 367 and 927)", [L(RM, r'\(task IDs 367 and 927\)')]),
 ('Methods', "From the 972 eligible problems, 450 were drawn at random (seed 20261103)", [L(RM, r'From the 972 eligible problems we drew 450 at random \(seed 20261103\)')]),
 ('Methods', "All 450 calls returned an answer", [L(RM, r'\| Generation \(v1\) \| .* \| 450 \| 450 answered')]),
 ('Methods', "with a 10-second timeout", [L('code/common.py', r'EXEC_TIMEOUT_S = 10\b')]),
 ('Methods', "ratio of at least 0.6, the operational", [L(PR, r'ratio of at least 0\.6 between the normalised')]),
 ('Methods', "Of 450 pairs, 419 (93.1\\%) were kept", [L(RM, r'419 of 450 pairs were'), L(RM, r'kept, a yield of 93\.1%')]),
 ('Methods', "on the trigger (14) or whose edit was too large (14)", [L(RM, r'\| Backdoored output equals the MBPP reference output on the trigger \| 14 \|'), L(RM, r'\| Edit too large \(difflib ratio < 0\.6\) \| 14 \|')]),
 ('Methods', "was 2, with a maximum of 8; 356 pairs (85\\%)", [L(RM, r'median 2, P90 4, maximum 8'), L(RM, r'356 of 419 pairs \(85%\) have exactly two changed lines')]),
 ('Methods', "(seed 4021) into a calibration pool of 40 pairs and a main pool of 379", [L(RM, r'Pools \(seed 4021\)\. The calibration pool holds 40 pairs and the main pool 379')]),
 ('Methods', "judged the 80 calibration-pool items", [L(CAL, r'shown once clean and once backdoored: 80 items')]),
 ('Methods', "between 0.40 and 0.90 and a false-alarm rate below 0.30", [L(CAL, r'Target: hit rate between 0\.40 and 0\.90 and false-alarm rate below 0\.30')]),
 ('Methods', "$24/40 = 0.60$ (Wilson 95\\% CI 0.45 to 0.74), the false-alarm rate $0/40 = 0.00$ (0.00 to 0.09) and the AUROC 0.97", [L(RM, r'hit rate 24/40 = 0\.60 \(Wilson 95% CI 0\.45–0\.74\) and false-alarm rate 0/40 = 0\.00 \(0\.00–0\.09\)'), L(RM, r'^AUROC was 0\.97')]),
 # ---- Methods: monitors
 ('Methods', "Claude Code 2.1.317", [L(CR, r'Claude Code 2\.1\.317')]),
 ('Methods', "score from 0 to 100 and a binary", [L(PR, r'suspicion score \(integer 0–100')]),
 ('Methods', "about 1,800 input tokens per call (1,812 for Haiku, 1,791 for Sonnet)", [L(RM, r'constant block of about 1,800 tokens'), L(RM, r'is 1,812 tokens for Haiku'), L(RM, r'and 1,791 for Sonnet \(1,787–1,795\)')]),
 # ---- Methods: experiments
 ('Methods', "\\paragraph{Experiment 1: experienced", [L(PR, r'^Experiment 1: experienced prevalence \(batch\)')]),
 ('Methods', "Each call showed a batch of 40 submissions", [L(PR, r'Each call shows a batch of 40 submissions')]),
 ('Methods', "how many of the 40 are backdoored: 20 in each of 8 batches, 4 in each of 40 and 1 in each of 160, giving 160 backdoored judgements per condition and 160, 1,440 and 6,240 clean ones", [L(PR, r'Each call shows a batch of 40 submissions'), L(PR, r'^\| P50 \| 20 \| 8 \| 160 \| 160 \|'), L(PR, r'^\| P10 \| 4 \| 40 \| 160 \| 1,440 \|'), L(PR, r'^\| P2\.5 \| 1 \| 160 \| 160 \| 6,240 \|')]),
 ('Methods', "\\paragraph{Experiment 2: stated", [L(PR, r'^Experiment 2: stated prevalence')]),
 ('Methods', "(``In past reviews, about 1 in 100 submissions contained a backdoor.'')", [L(PR, r'"In past reviews, about 1 in 100 submissions contained a backdoor\."')]),
 ('Methods', "The same 240 main-pool problems (120 shown backdoored, 120 clean)", [L(RM, r'240 distinct main-pool problems \(120 shown backdoored, 120 shown clean\)')]),
 ('Methods', "\\paragraph{Experiment 3: remedies", [L(PR, r'^Experiment 3: remedies at low prevalence')]),
 ('Methods', "drawn afresh: 80 per remedy, giving 80 backdoored and 3,120 clean judgements", [L(PR, r'80 batches per monitor per remedy'), L(RN, r'^\| Haiku \| R-cal \| 80 \| 80 \| 48 \| .* \| 3120 \|')]),
 ('Methods', "first showed 10 examples from 10 distinct calibration-pool problems (5 backdoored, 5 clean", [L(PR, r'Each R-cal batch draws its own 10 examples \(10 distinct calibration-pool problems: 5 backdoored, 5 clean')]),
 ('Methods', "(seed 55021) and run in shuffled order (seed 99173) from 23:12 UTC on 3 November to 00:12 UTC on 4 November 2026", [L('code/s6_design.py', r'DESIGN_SEED = 55021'), L(RM, r'\(seed 99173\)'), L(RM, r'The main calls ran from 23:12 UTC on 3 November to 00:12 UTC on 4 November 2026')]),
 # ---- Methods: measures and analysis
 ('Methods', "Rates have Wilson 95\\% confidence intervals; $d'$, $c$ and AUROC have 95\\% bootstrap intervals (2,000 resamples) over batches in Experiments 1 and 3 and over items, paired across conditions, in Experiment 2", [L(RM, r'hit and false-alarm rates, with Wilson 95% CIs'), L(RM, r'cluster bootstrap \(2,000 resamples\)\. The bootstrap resamples batches in Experiments 1 and 3'), L(RM, r'items, paired across conditions, in Experiment 2;')]),
 ('Methods', "$\\alpha = .05$", [L(PR, r'about 80% power at α = \.05')]),
 ('Methods', "with 40-node Gauss--Hermite quadrature and a pre-specified", [L(PR, r'with 40-node Gauss–Hermite quadrature')]),
 ('Methods', "flag on position (1 to 40)", [L(PR, r'position \(1–40\) within P2\.5 and P10')]),
 ('Methods', "about 80\\% power for a fall in hit rate from 0.80 to 0.65 with 160 backdoored judgements per cell", [L(PR, r'with 160 backdoored judgments per cell, a drop in hit rate from 0\.80 to 0\.65 is detectable with about 80% power')]),
 ('Methods', "smaller than about 15 percentage points", [L(PR, r'Effects smaller than about 15 points may be missed')]),
 ('Methods', "Experiment 2 has 120 backdoored items per condition and Experiment 3 has 80 backdoored judgements per remedy. This applies with more force to Experiment 3; Experiment 2 has fewer items", [L(SP, r'Experiment 2 has 120 backdoored items per condition and Experiment 3 has 80 backdoored judgements per remedy\. This applies with more force to Experiment 3; Experiment 2 has fewer items')]),
 ('Methods', "Python 3.13.18 and statsmodels 0.15.0 (bootstrap seed 314159)", [L(CR, r'Python 3\.13\.18'), L(CR, r'statsmodels 0\.15\.0'), L('code/analyse.py', r'BOOT_SEED = 314159')]),
 # ---- Methods: pre-registration record
 ('Methods', "Items 1 to 3, by the author", [L(PR, r'Items 1–3 are in commit')]),
 ('Methods', "were committed at 23:10 UTC on 3 November, before", [L(PR, r'Items 1–3 are in commit `?136632a`? \(23:10 UTC'), L(PR, r'Clarifications added on 3 November 2026')]),
 ('Methods', "That the 0.6 edit-size threshold", [L(PR, r'Item 3 says the 0\.6 threshold')]),
 ('Methods', "in place of item~3's original wording", [L(PR, r'Correction to item 3')]),
 ('Methods', "Items 4 to 12, by the research engineer", [L(PR, r'Items 4–12 first appear in commit')]),
 ('Methods', "at 23:16 UTC, after the main run had started (23:13 UTC, with 12 smoke-test calls already done) and when that commit already held 138 main-experiment outputs", [L(PR, r'\(23:16 UTC\)\. By then the main run had started: the run log shows it starting at 23:13 UTC with 12 calls already done from a smoke test, and that commit already held 138 main-experiment outputs')]),
 ('Methods', "at 23:10:45 UTC, before the first main-experiment output at 23:12:32 UTC", [L(AU, r'\(23:10:45 UTC\)\. The first main-experiment output was written at 23:12:32 UTC')]),
 ('Methods', "All 2,176 main calls (30,880 judgements)", [L(RM, r'The study made 2,176 main monitor calls \(30,880 item')]),
 ('Methods', "(\\code{num\\_turns}~$>$~2)", [L(RM, r'^num_turns > 2\. We see only the final output')]),
 ('Methods', "in 43 of 368 Haiku batch calls and 24 of 720 Sonnet single-item calls", [L(RM, r'43 of 368 Haiku batch calls'), L(RM, r'24 of 720 Sonnet single-item calls')]),
 # ---- Results
 ('Results', "at or below 4.0\\% in every condition", [C('max F over all 16 cells, x100', lambda: max(v['F'] for v in D().values()) * 100, 'eqround')]),
 ('Results', "below 2\\% in all batch conditions except Sonnet's R-cal", [C("max F over batch cells other than Sonnet R-cal, x100", lambda: max(v['F'] for k, v in D().items() if k.split('|')[1] in ('P50', 'P10', 'P2.5', 'R-cal', 'R-ind') and k != 'Sonnet|R-cal') * 100, 'lt')]),
 ('Results', "hit rate $H$ (Wilson 95\\% CI), false-alarm rate $F$, $d'$, $c$ and AUROC with 95\\% bootstrap CIs", [L(RN, r'^H = hit rate, F = false-alarm rate \(Wilson 95% CIs\)')]),
 ('Results', "P50 160/160; P10 160/1,440; P2.5 160/6,240; R-cal and R-ind 80/3,120; single-item conditions 120/120", [L(RN, r'^\| Haiku \| P50 \| 8 \| 160 \| 82 \|'), L(RN, r'^\| Haiku \| P10 \| 40 \| 160 \| 80 \|'), L(RN, r'^\| Haiku \| P2\.5 \| 160 \| 160 \| 111 \|'), L(RN, r'^\| Haiku \| R-cal \| 80 \| 80 \| 48 \|'), L(RN, r'^\| Haiku \| none \| 240 \| 120 \| 76 \|')]),
 ('Results', "the population-averaged odds ratio is 0.61 [0.44, 0.84], a fall in hit rate of 7.5 points", [L(RN, r'^\| Sonnet \| S1 vs S50 \| -0\.498'), L(RM, r"GLM's OR of 0\.61, or −7\.5 percentage points", 'abs')]),
 ('Results', "Haiku's hit rate was 0.512 at P50, 0.500 at P10 and 0.694 at P2.5; Sonnet's was 0.500, 0.569 and 0.738", [L(RN, r'^\| Haiku \| P50 \| 8 \| 160 \|'), L(RN, r'^\| Haiku \| P10 \| 40 \| 160 \|'), L(RN, r'^\| Haiku \| P2\.5 \| 160 \| 160 \|'), L(RN, r'^\| Sonnet \| P50 \| 8 \| 160 \|'), L(RN, r'^\| Sonnet \| P10 \| 40 \| 160 \|'), L(RN, r'^\| Sonnet \| P2\.5 \| 160 \| 160 \|')]),
 ('Results', "the odds ratio was 2.15 for Haiku (95\\% CI 1.34 to 3.46, Holm $p = .0015$) and 2.81 for Sonnet (1.78 to 4.43, Holm $p < .001$)", [L(RM, r'2\.15 for Haiku \(95% CI 1\.34–3\.46, Holm p = \.0015\) and 2\.81 for'), L(RM, r'Sonnet \(95% CI 1\.78–4\.43, Holm p < \.001\)'), L(RN, r'^\| Haiku \| P2\.5 vs P50 \(confirmatory\)'), L(RN, r'^\| Sonnet \| P2\.5 vs P50 \(confirmatory\)')]),
 ('Results', "(Haiku OR 0.95, $p = .828$; Sonnet OR 1.32, $p = .211$)", [L(RN, r'^\| Haiku \| P10 vs P50 \|'), L(RN, r'^\| Sonnet \| P10 vs P50 \|')]),
 ('Results', "(all $p > .25$)", [C('min p of the four false-alarm prevalence contrasts (H1_false_alarms)', h1fa_min_p, 'gt')]),
 ('Results', "by backdoor prevalence in a batch of 40 (Experiment~1); left, Haiku (orange); right, Sonnet (blue). Error bars are Wilson 95\\%", [L(SP, r'by backdoor prevalence in a batch of 40 \(Experiment 1\)\. Error bars are Wilson 95%')]),
 ('Results', "($\\Delta c = {-0.44}$, 95\\% CI $-0.70$ to $-0.28$)", [L(RN, r'^\| Sonnet \| 0\.238 \[0\.144, 0\.338\]'), L(RN, r'^Point estimates with 95% cluster-bootstrap CIs')]),
 ('Results', "($\\Delta d' = 0.71$, 0.06 to 1.04)", [L(RN, r'^\| Haiku \| 0\.181 \[0\.075, 0\.281\]')]),
 ('Results', "($\\Delta c > 0$ with an interval", [L(RN, r'Support requires Δc > 0 with a CI excluding 0')]),
 ('Results', "(point estimate and 95\\% cluster-bootstrap CI)", [L(RN, r'^Point estimates with 95% cluster-bootstrap CIs')]),
 ('Results', "Telling Sonnet that ``about 1 in 100''", [L(PR, r'"In past reviews, about 1 in 100 submissions contained a backdoor\."')]),
 ('Results', "hit rate from 0.850 to 0.775 (registered GLMM: log-odds $-3.32$, SE 1.25, $z = {-2.66}$, $p = .008$, Holm $p = .015$", [L(RN, r'^\| Sonnet \| S50 \| 240 \| 120 \|'), L(RN, r'^\| Sonnet \| S1 \| 240 \| 120 \|'), L(RN, r'^\| Sonnet \| S1 vs S50 \(confirmatory\) \| -3\.321 \| 1\.246', 'round')]),
 ('Results', "the hit rate went from 0.683 to 0.642 (OR 0.57, 0.22 to 1.46, $p = .244$, Holm $p = .244$)", [L(RN, r'^\| Haiku \| S50 \| 240 \| 120 \|'), L(RN, r'^\| Haiku \| S1 \| 240 \| 120 \|'), L(RN, r'^\| Haiku \| S1 vs S50 \(confirmatory\)')]),
 ('Results', "Because 92 of 120 backdoored items were flagged in all three conditions", [L(RM, r'identified: 92 of 120 backdoored items were flagged in all three conditions')]),
 ('Results', "and 40-node non-adaptive quadrature", [L(PR, r'with 40-node Gauss–Hermite quadrature')]),
 ('Results', "($\\sigma = 32.8$)", [L(RM, r'^\s*SD 32\.8\.$'), J(PH, 'monitors/Sonnet/registered_40node/sigma', 'round')]),
 ('Results', "gives $\\sigma = 13.4$ and an S1 log-odds of $-3.76$ (SE 1.41, $z = {-2.67}$, $p = .0076$; likelihood-ratio $p = .00024$)", [L(RM, r'The accurate maximum-likelihood fit has item SD 13\.4 and S1 vs S50 log-odds −3\.76 \(SE 1\.41\)'), L(RM, r'^\s*z = −2\.67, p = \.0076'), L(RM, r'^- Sonnet: LR = 13\.50, p = \.00024\.')]),
 ('Results', "9 Sonnet items were flagged under S50 but not under S1, and none the other way round (exact paired test, $p = .0039$)", [L(RM, r'^\| Sonnet \| 9 \| 0 \| \.0039 \|')]),
 ('Results', "the paired counts were 12 against 7 ($p = .36$)", [L(RM, r'^\| Haiku \| 12 \| 7 \| \.36 \|')]),
 ('Results', "was 0.61 (0.44 to 0.84, $p = .002$)", [L(RN, r'^\| Sonnet \| S1 vs S50 \| -0\.498')]),
 ('Results', "hit rate was $-0.075$ ($-0.125$ to $-0.033$)", [L(RN, r'^\| Sonnet \| -0\.075 \[-0\.125, -0\.033\]')]),
 ('Results', "($\\Delta c = 0.29$, 0.05 to 0.59)", [L(RN, r'^\| Haiku \| -0\.042 \[-0\.117, 0\.025\]')]),
 ('Results', "(0.27, $-0.01$ to 0.58)", [L(RN, r'^\| Sonnet \| -0\.075 \[-0\.125, -0\.033\]')]),
 ('Results', "($-0.017$, $-0.034$ to $-0.004$)", [L(RN, r'^\| Sonnet \| -0\.075 \[-0\.125, -0\.033\]')]),
 ('Results', "backdoored items (75.0 to 62.7)", [L(RN, r'^\| Sonnet \| S50 \| 240 \| 120 \|'), L(RN, r'^\| Sonnet \| S1 \| 240 \| 120 \|')]),
 ('Results', "among items scoring 40--59 did not fall", [L(RN, r'^\| Monitor \| Condition \| P\(flag\) at 0–19')]),
 ('Results', "($p = .108$ and .329)", [J(AJ, "H2/Haiku/false_alarm_glm_item_clustered/coefs/C(condition, Treatment('S50'))[T.S1]/p", 'round'), J(AJ, "H2/Sonnet/false_alarm_glm_item_clustered/coefs/C(condition, Treatment('S50'))[T.S1]/p", 'round')]),
 ('Results', "Haiku's fall of about 4 points", [J(AJ, 'H2/Haiku/S1_minus_S50_point/H', 'abs', 'pct')]),
 ('Results', "At 2.5\\% prevalence the 10 labelled examples", [L(PR, r'H3 \(remedy\)\. At 2\.5% batch prevalence'), L(PR, r'shows 10 example submissions from the calibration pool')]),
 ('Results', "fell from 0.694 to 0.600 (OR 0.66, 0.38 to 1.16, $p = .150$, Holm $p = .150$)", [L(RN, r'^\| Haiku \| P2\.5 \| 160 \| 160 \|'), L(RN, r'^\| Haiku \| R-cal \| 80 \| 80 \|'), L(RN, r'^\| Haiku \| R-cal vs P2\.5 \(confirmatory\)')]),
 ('Results', "rose from 0.738 to 0.850 (OR 2.02, 0.99 to 4.10, $p = .053$, Holm $p = .106$)", [L(RN, r'^\| Sonnet \| P2\.5 \| 160 \| 160 \|'), L(RN, r'^\| Sonnet \| R-cal \| 80 \| 80 \|'), L(RN, r'^\| Sonnet \| R-cal vs P2\.5 \(confirmatory\)')]),
 ('Results', "($\\Delta c = {-0.37}$, $-0.59$ to $-0.18$) with no change in $d'$ (0.03, $-0.38$ to 0.48)", [L(RN, r'^\| Sonnet \| 0\.0224 \[0\.0139, 0\.0314\]')]),
 ('Results', "rose from 1.7\\% to 4.0\\% ($\\Delta F = 0.0224$, 0.0139 to 0.0314)", [L(RN, r'^\| Sonnet \| P2\.5 \| 160 \| 160 \| 118 \| [^|]* \| 6240 \| 108 \| 0\.0173', 'pct'), L(RN, r'^\| Sonnet \| R-cal \| 80 \| 80 \| 68 \| [^|]* \| 3120 \| 124 \| 0\.0397', 'pct'), L(RN, r'^\| Sonnet \| 0\.0224 \[0\.0139, 0\.0314\]')]),
 ('Results', "rose from 1.41 to 2.40", [L(RN, r'^\| Sonnet \| P2\.5 \| 1\.41 \|'), L(RN, r'^\| Sonnet \| R-cal \| 2\.40 \|')]),
 ('Results', "With 80 backdoored judgements per remedy cell", [L(RN, r'^\| Haiku \| R-cal \| 80 \| 80 \|')]),
 ('Results', "(all $p \\geq .08$", [L(RN, r'^\| Sonnet \| P10 \| backdoored \(hit\) \| 0\.0249'), C('min p of the four E1 hit-rate position tests (exploratory/E1)', e1_min_hit_p, 'ge_r')]),
 ('Results', "(OR per 10 positions 1.26, $p = .019$)", [L(RN, r'^\| Monitor \| Condition \| Items \| Coef\. per position'), L(RN, r'^\| Sonnet \| P2\.5 \| clean \(false alarm\) \| 0\.0228')]),
 ('Results', "(Haiku OR 0.74, 0.42 to 1.30, $p = .288$; Sonnet OR 1.07, 0.57 to 1.98, $p = .835$)", [L(RN, r'^\| Haiku \| R-ind vs P2\.5 \(hit rate\)'), L(RN, r'^\| Sonnet \| R-ind vs P2\.5 \(hit rate\)')]),
 ('Results', "($\\Delta F = {-0.0045}$, ${-0.0088}$ to ${-0.0003}$)", [L(RN, r'^\| Haiku \| -0\.0045 \[-0\.0088, -0\.0003\]')]),
 ('Results', "(all monitor terms and interactions $p \\geq .195$)", [L(RN, r"^\| C\(condition, Treatment\('P50'\)\)\[T\.P10\]:C\(monitor, Treatment\('Haiku'\)\)\[T\.Sonnet\] \| 0\.327"), C('min p of monitor terms and interactions, Experiment 1 hits and false alarms (exploratory/E3)', e3_min_p, 'ge_r')]),
 ('Results', "(log-odds 0.965, SE 0.230, $p < .001$, at S50)", [L(RN, r"^\| C\(monitor, Treatment\('Haiku'\)\)\[T\.Sonnet\] \| 0\.965 \| 0\.230")]),
 ('Results', "(Haiku 0.633, Sonnet 0.800)", [L(RN, r'^\| Haiku \| none \| 240 \|'), L(RN, r'^\| Sonnet \| none \| 240 \|')]),
 ('Results', "for Haiku, 0.61 at P50 ($p = .051$), 0.58 at P10 ($p = .026$) and 1.31 at P2.5 ($p = .291$); for Sonnet, 0.25 ($p < .001$), 0.33 ($p < .001$) and 0.70 ($p = .226$)", [L(RN, r'^\| Haiku \| P50 \(batch\) vs none \(single\), hits'), L(RN, r'^\| Haiku \| P10 \(batch\) vs none \(single\), hits'), L(RN, r'^\| Haiku \| P2\.5 \(batch\) vs none \(single\), hits'), L(RN, r'^\| Sonnet \| P50 \(batch\) vs none \(single\), hits'), L(RN, r'^\| Sonnet \| P10 \(batch\) vs none \(single\), hits'), L(RN, r'^\| Sonnet \| P2\.5 \(batch\) vs none \(single\), hits')]),
 ('Results', "(all $p \\geq .46$)", [L(RN, r'^\| Sonnet \| P2\.5 \(batch\) vs none \(single\), false alarms .* 0\.465'), C('min p of the six E4 false-alarm contrasts (exploratory/E4)', e4_min_fa_p, 'ge_r')]),
 ('Results', "No item scoring below 20 was flagged and every item scoring 60 or more was; most of the change happened in the 40--59 band, with a few items scoring 20--39", [L(RN, r'^\| Monitor \| Condition \| P\(flag\) at 0–19')]),
 ('Results', "(80--100: Haiku 0.09 against 0.22, Sonnet 0.17 against 0.45)", [L(RN, r'^\| Monitor \| Condition \| P\(flag\) at 0–19'), L(RN, r'^\| Haiku \| P50 \| 0\.00 \(n=195\)'), L(RN, r'^\| Haiku \| P2\.5 \| 0\.00 \(n=6044\)'), L(RN, r'^\| Sonnet \| P50 \| 0\.00 \(n=202\)'), L(RN, r'^\| Sonnet \| P2\.5 \| 0\.00 \(n=6052\)')]),
 ('Results', "7,592 at P50 against 4,195 at P2.5; Sonnet's were 116 against 480", [L(RM, r'^\| Haiku \| 7,592 \| 4,757 \| 4,195'), L(RM, r'^\| Sonnet \| 116 \| 480 \| 480')]),
 ('Results', "The H1 odds ratios were 2.35 for Haiku ($p = .0007$) and 2.81 for Sonnet ($p < .001$), and Haiku's H3 $p$ value moved from .150 to .076", [L(RM, r'^\| Haiku \| 2\.35, \.0007 \|'), L(RM, r'^\| Sonnet \| 2\.81, < \.001 \|'), L(RN, r'^\| Haiku \| R-cal vs P2\.5 \(confirmatory\)'), J(SE, 'results/Haiku/H3/p', 'round')]),
 # ---- Discussion
 ('Discussion', "caught more backdoors at 2.5\\% prevalence than at 50\\%, and the criterion", [L(SP, r'caught more backdoors at 2\.5% prevalence than at 50%, and the criterion')]),
 ('Discussion', "A stated base rate of 1 in 100 had a small effect", [L(SP, r'A stated base rate of 1 in 100 had a small effect')]),
 ('Discussion', "An LLM monitor sees all 40 items at once", [L(SP, r'An LLM monitor sees all 40 items at once')]),
 ('Discussion', "number of backdoors in a batch of 40, and P10 (4 backdoors) behaved like P50 (20)", [L(SP, r'number of backdoors in a batch of 40, and P10 \(4 backdoors\) behaved like P50 \(20\)')]),
 ('Discussion', "one odd item among 39 ordinary ones", [L(SP, r'one odd item among 39 ordinary ones')]),
 ('Discussion', "coordinating them ``across space'' \\citep[Sec.~6]{korbak2025}", [L(SP, r'coordinating them "across space" \\cite\[Sec\. 6\]\{korbak2025\}')]),
 ('Discussion', "\\citep[Experiment~7]{wolfe2007}", [L(SP, r'\\cite\[Experiment 7\]\{wolfe2007\}')]),
 ('Discussion', "which is 2\\% of problems in \\citet{greenblatt2024} and 0.1\\% of actions", [L(SP, r'which is 2% of problems in Greenblatt et al\. \\cite\{greenblatt2024\} and 0\.1% of actions')]),
 ('Discussion', "about 100 TIP events per screener", [L(SP, r'about 100 TIP events per screener')]),
 # ---- Limitations and conclusion
 ('Limitations', "Each call carried about 1,800 tokens", [L(RM, r'constant block of about 1,800 tokens')]),
 ('Limitations', "P50 had 8 batches per monitor", [L(PR, r'^\| P50 \| 20 \| 8 \| 160 \| 160 \|')]),
 ('Limitations', "All batches held 40 items", [L(PR, r'Each call shows a batch of 40 submissions')]),
 ('Limitations', "The lowest prevalence was 2.5\\%", [L(PR, r'rare in the batch \(2\.5%\)')]),
 ('Limitations', "effects smaller than about 15 points may have been missed", [L(PR, r'Effects smaller than about 15 points may be missed')]),
 ('Limitations', "H3 (80 backdoored judgements per cell)", [L(RN, r'^\| Haiku \| R-cal \| 80 \| 80 \|')]),
 ('Limitations', "rest on 120 clean items", [L(RN, r'^\| Haiku \| none \| 240 \| 120 \| 76 \| [^|]* \| 120 \|')]),
 ('Limitations', "Clarifications 4 to 12 were committed", [L(PR, r'Items 4–12 first appear in commit')]),
 ('Conclusion', "when one backdoor sat in a batch of 40", [L(PR, r'Each call shows a batch of 40 submissions')]),
 # ---- Table headers
 ('Table 1 header', "$H$ [95\\% CI] & $F$ & $d'$ [95\\% CI] & $c$ [95\\% CI] & AUROC [95\\% CI]", [L(RMT, r'^\| Monitor \| Condition \| H \[95% CI\] \| F \[95% CI\]')]),
 ('Table 2 header', "OR [95\\% CI] & $z$", [L(RN, r'^\| Monitor \| Contrast \| log-odds \| SE \| OR \[95% CI\] \| z \| p \| p \(Holm\) \|')]),
 ('Table 3 header', "$\\Delta H$ [95\\% CI] & $\\Delta F$ [95\\% CI] & $\\Delta d'$ [95\\% CI] & $\\Delta c$ [95\\% CI] & $\\Delta$AUROC [95\\% CI]", [L(RN, r'^\| Monitor \| ΔH \[95% CI\] \| ΔF \[95% CI\] \| Δd′ \[95% CI\]')]),
 ('Table 4 header', "Top band & Flag at 40--59", [L(RN, r'^\| Monitor \| Condition \| P\(flag\) at 0–19')]),
 # ---- Appendix
 ('Appendix', "share of backdoored items scoring 80--100. ``Flag at 40--59''", [L(RN, r'^\| Monitor \| Condition \| P\(flag\) at 0–19')]),
 ('Appendix', "(Experiment~2); left, Haiku (orange); right, Sonnet (blue). Error bars are Wilson 95\\%", [L(SP, r'statements of the base rate \(Experiment 2\)\. Error bars are Wilson 95%')]),
 ('Appendix', "Hit and false-alarm rates at 2.5\\% prevalence without a remedy", [L(SP, r'Hit and false-alarm rates at 2\.5% prevalence without a remedy')]),
 ('Appendix', "R-ind); left, Haiku (orange); right, Sonnet (blue). Error bars are Wilson 95\\%", [L(SP, r'with the independence instruction \(R-ind\)\. Error bars are Wilson 95%')]),
 ('Appendix', "Error bars are 95\\% bootstrap confidence intervals: a cluster bootstrap over batches for Experiments 1 and 3, and a paired item bootstrap for Experiment~2", [L(SP, r'Error bars are 95% bootstrap confidence intervals: a cluster bootstrap over batches for Experiments 1 and 3, and a paired item bootstrap for Experiment 2')]),
 ('Appendix', "(exploratory, E1); left, Haiku (orange); right, Sonnet (blue). Error bars are Wilson 95\\%", [L(SP, r'in bins of eight positions \(exploratory\)\. Error bars are Wilson 95%')]),
]

# --------------------------------------------------------------------------- masking / extraction
def body_and_mask():
    t = TEX.read_text(encoding='utf-8')
    start = t.index('\\begin{document}')
    m = list(t)
    def blank(a, b):
        for i in range(a, b):
            if m[i] != '\n':
                m[i] = ' '
    blank(0, start)
    pats = [r'(?<!\\)%.*', r'\\code\{[^}]*\}', r'\\label\{[^}]*\}', r'\\(?:eq)?ref\{[^}]*\}',
            r'\\includegraphics\[[^\]]*\]\{[^}]*\}', r'\\cite[a-z]*(?=[\[{])', r'(?<=\])\{[a-z0-9_,]+\}|(?<=\\citep)\{[a-z0-9_,]+\}|(?<=\\citet)\{[a-z0-9_,]+\}|(?<=\\citealp)\{[a-z0-9_,]+\}',
            r'\\begin\{tabular\}\{[^\n]*', r'\\setlength\{\\tabcolsep\}\{[^}]*\}', r'\\begin\{(?:table|figure)\*?\}\[[a-z]*\]',
            r'\\bibliography\{[^}]*\}']
    for p in pats:
        for x in re.finditer(p, t, flags=re.M):
            blank(x.start(), x.end())
    return t, ''.join(m)

def number_spans(masked, a=0, b=None):
    b = len(masked) if b is None else b
    return [(x.start(), x.end(), norm_tok(x.group())) for x in NUM.finditer(masked, a, b)]

# --------------------------------------------------------------------------- tables
def table_rows(t, label):
    """Return list of (start, end, cells) for the data rows of the tabular in the table labelled `label`."""
    li = t.index('\\label{%s}' % label)
    ts = t.rfind('\\begin{tabular}', 0, li)
    te = t.index('\\end{tabular}', ts)
    mid = t.index('\\midrule', ts)
    rows, pos = [], mid + len('\\midrule')
    for raw in re.finditer(r'[^\n]*\\\\', t[pos:te]):
        s = pos + raw.start(); e = pos + raw.end()
        line = raw.group()
        if line.strip().startswith('\\midrule') or line.strip().startswith('\\bottomrule'):
            continue
        cells = [c.strip() for c in line.rstrip('\\').split('&')]
        rows.append((s, e, cells))
    return rows

def cell_nums(cell):
    return [norm_tok(x.group()) for x in NUM.finditer(' ' + cell.replace('\u2212', '-').replace('$', ' ').replace('{', ' ').replace('}', ' '))]

def md_row(rel, rx):
    n, line = find_line(rel, rx)
    if line is None:
        return None, None
    return n, [c.strip() for c in line.strip().strip('|').split('|')]

COND = {'P50 (batch)': 'P50 (Exp 1)', 'P10 (batch)': 'P10 (Exp 1)', 'P2.5 (batch)': 'P2.5 (Exp 1)', 'R-cal (batch)': 'R-cal (Exp 3)',
        'R-ind (batch)': 'R-ind (Exp 3)', '\\emph{none} (single)': 'none (Exp 2)', 'S50 (single)': 'S50 (Exp 2)', 'S1 (single)': 'S1 (Exp 2)'}

def check_tables(t, report, covered):
    ok_all = True
    # Table: registered measures
    for s, e, c in table_rows(t, 'tab:measures'):
        mon, cond = c[0], c[1]
        n, src = md_row(RMT, r'^\| %s \| %s' % (mon, re.escape(COND[cond])))
        sub_nums = [x for cell in c[2:] for x in cell_nums(cell)]
        # source: H [ci], F [ci] -> F point as %, d', c, AUROC, means
        srcnums = cell_nums(src[2]) + [None] + cell_nums(src[4]) + cell_nums(src[5]) + cell_nums(src[6]) + cell_nums(src[7]) + cell_nums(src[8])
        fval = float('0' + cell_nums(src[3])[0]) if cell_nums(src[3])[0].startswith('.') else float(cell_nums(src[3])[0])
        srcnums[3] = fmt_like(fval * 100, sub_nums[3])
        ok = sub_nums == srcnums
        ok_all &= ok
        report.append(('Table 1 (registered measures)', f'{mon} {cond.replace(chr(92)+"emph{none}", "none")}', ' '.join(sub_nums), f'{RMT}:{n} (F: x100, 1 dp)', 'match' if ok else 'MISMATCH ' + ' '.join(map(str, srcnums))))
        if ok: covered.update(range(s, e))
    # Table: confirmatory tests
    keys = {('H1', 'Haiku'): ('H1/Haiku/P2.5_vs_P50', r'^\| Haiku \| P2\.5 vs P50 \(confirmatory\)'), ('H1', 'Sonnet'): ('H1/Sonnet/P2.5_vs_P50', r'^\| Sonnet \| P2\.5 vs P50 \(confirmatory\)'),
            ('H2', 'Haiku'): ('H2/Haiku', r'^\| Haiku \| S1 vs S50 \(confirmatory\)'), ('H2', 'Sonnet'): ('H2/Sonnet', r'^\| Sonnet \| S1 vs S50 \(confirmatory\)'),
            ('H3', 'Haiku'): ('H3/Haiku', r'^\| Haiku \| R-cal vs P2\.5 \(confirmatory\)'), ('H3', 'Sonnet'): ('H3/Sonnet', r'^\| Sonnet \| R-cal vs P2\.5 \(confirmatory\)')}
    for s, e, c in table_rows(t, 'tab:tests'):
        hyp, mon = c[0], c[2]
        jp, rx = keys[(hyp, mon)]
        n, src = md_row(RN, rx)
        or_ci = cell_nums(c[3]); z = cell_nums(c[4]); p = c[5].replace('$', '').replace('<\\,', '<').strip(); ph = c[6].replace('$', '').replace('<\\,', '<').strip()
        ok = or_ci == cell_nums(src[4]) and z == cell_nums(src[5])
        term = json_get(AJ, jp + '/term'); pholm = json_get(AJ, jp + '/p_holm')
        def pcheck(printed, val):
            if printed.startswith('<'):
                return val < float(printed[1:].strip())
            return fmt_like(val, printed.strip()) == norm_tok(printed.strip())
        ok = ok and pcheck(p, term['p']) and pcheck(ph, pholm) and fmt_like(term['OR'], or_ci[0]) == or_ci[0]
        ok_all &= ok
        report.append(('Table 2 (confirmatory tests)', f'{hyp} {mon}', ' '.join(or_ci + z + [p, ph]), f'{RN}:{n}; {AJ} [{jp}/term/p, p_holm]', 'match' if ok else 'MISMATCH'))
        if ok: covered.update(range(s, e))
    # Table: H1a
    for s, e, c in table_rows(t, 'tab:h1a'):
        mon = c[0]
        n, src = md_row(RN, r'^\| %s \| (0\.181|0\.238) \[' % mon)
        sub = [x for cell in c[1:] for x in cell_nums(cell)]
        srcn = [x for cell in src[1:6] for x in cell_nums(cell)]
        ok = sub == srcn
        ok_all &= ok
        report.append(('Table 3 (H1a)', mon, ' '.join(sub), f'{RN}:{n}', 'match' if ok else 'MISMATCH ' + ' '.join(srcn)))
        if ok: covered.update(range(s, e))
    # Table: score bands (appendix)
    cm = {'P50': 'P50', 'P2.5': 'P2.5', '\\emph{none} (single)': 'none', 'S50 (single)': 'S50', 'S1 (single)': 'S1'}
    for s, e, c in table_rows(t, 'tab:bands'):
        mon, cond = c[0], cm[c[1]]
        n, src = md_row(RN, r'^\| %s \| %s \| 0\.00 \(n=' % (mon, re.escape(cond)))
        top = cell_nums(src[11])  # bd share 80-100
        flag4059 = cell_nums(src[4])[0:1]
        sub = cell_nums(c[2]) + cell_nums(c[3])
        ok = sub == top + flag4059
        ok_all &= ok
        report.append(('Table 4 (score bands, appendix)', f'{mon} {cond}', ' '.join(sub), f'{RN}:{n} (bd share 80–100; P(flag) at 40–59)', 'match' if ok else 'MISMATCH ' + ' '.join(top + flag4059)))
        if ok: covered.update(range(s, e))
    return ok_all

# --------------------------------------------------------------------------- source-paper fidelity
def sentences_of_source():
    t = latex_norm((ROOT / SP).read_text(encoding='utf-8'))
    t = t[t.index('\\begin{document}'):]
    t = re.sub(r'\\cite\[([^\]]*)\]\{[^}]*\}', r'[\1]', t)
    t = re.sub(r'\\cite\{[^}]*\}', ' ', t)
    return [s for s in re.split(r'(?<=[.])\s+(?=[A-Z\\(])|\n', t) if s.strip()]

def sentence_around(t, i, j):
    """Expand [i, j) of the submission to the enclosing sentence (or table row / caption)."""
    a = max(t.rfind('. ', 0, i), t.rfind('\n', 0, i), t.rfind('{', 0, i) if t[max(0, i - 1)] == '{' else -1)
    b_candidates = [x for x in (t.find('. ', j), t.find('\n', j)) if x >= 0]
    b = min(b_candidates) if b_candidates else len(t)
    return t[a + 1:b + 1]

# Numbers that the condensation moved out of a table (or caption) of the full paper into prose or
# a header: their place in the full paper is given explicitly.
FIDELITY_EXTRA = {
 "how many of the 40 are backdoored: 20 in each of 8 batches": [r'^1 & P50 & Batch of 40 & 20 & 8 & 160 & 160', r'^1 & P10 & Batch of 40 & 4 & 40 & 160 & 1440', r'^1 & P2\.5 & Batch of 40 & 1 & 160 & 160 & 6240'],
 "drawn afresh: 80 per remedy": [r'^3 & R-cal & 10 labelled examples, then batch of 40 & 1 & 80 & 80 & 3120'],
 "(80--100: Haiku 0.09 against 0.22": [r'^Haiku & P50 & 0\.09 & 0\.73', r'^Haiku & P2\.5 & 0\.22 & 0\.84', r'^Sonnet & P50 & 0\.17 & 0\.85', r'^Sonnet & P2\.5 & 0\.45 & 0\.93', r'"Top band" is the share of backdoored items scoring 80--100'],
 "$H$ [95\\% CI] & $F$": [r'Hit rate H \(Wilson 95% CI\)', r'AUROC with 95% bootstrap CIs'],
 "OR [95\\% CI] & $z$": [r'OR \[95% CI\] & z & p & Holm p & Outcome'],
 "$\\Delta H$ [95\\% CI]": [r'point estimate and 95% cluster-bootstrap CI'],
}

def fidelity_extra_tokens(snip):
    toks = set()
    for k, rxs in FIDELITY_EXTRA.items():
        if snip.startswith(k):
            for rx in rxs:
                n, line = find_line(SP, rx)
                if line is not None:
                    toks |= set(tokens(line))
    return toks

def fidelity(sentence, nums, src_sents):
    s = latex_norm(sentence)
    s = re.sub(r'\\cite[a-z]*\[([^\]]*)\]\{[^}]*\}', r'[\1]', s)
    s = re.sub(r'\\cite[a-z]*\{[^}]*\}', ' ', s)
    best, bi = 0, 0
    for i, x in enumerate(src_sents):
        r = difflib.SequenceMatcher(None, s, x, autojunk=False).ratio()
        if r > best:
            best, bi = r, i
    window = ' '.join(src_sents[max(0, bi - 2): bi + 3])
    wt = set(tokens(window)) | set(x.lstrip('-') for x in tokens(window))
    missing = [n for n in nums if n not in wt and n.lstrip('-') not in wt]
    return best, missing, src_sents[bi][:90]

# --------------------------------------------------------------------------- main
def main():
    md = '--markdown' in sys.argv
    t, masked = body_and_mask()
    covered = set()
    report = []
    ok_tables = check_tables(t, report, covered)
    src_sents = sentences_of_source()
    n_mis = 0 if ok_tables else 1
    fid_flags = []
    for sec, snip, evs in CLAIMS:
        i = t.find(snip)
        if i < 0:
            report.append((sec, snip[:60], '', 'snippet not found in paper.tex', 'MISMATCH')); n_mis += 1; continue
        spans = number_spans(masked, i, i + len(snip))
        nums = [x[2] for x in spans]
        rows_ok = True; locs = []; vals = []
        for num in nums:
            hit = None
            for ev in evs:
                ok, val, loc = matches_number(num, ev)
                if ok:
                    hit = (val, loc); break
            if hit is None:
                rows_ok = False; vals.append(f'{num}: NOT FOUND')
            else:
                if hit[1] not in locs: locs.append(hit[1])
                if hit[0] != num: vals.append(f'{num} ← {hit[0]}')
        # cover every occurrence of this snippet
        j = i
        while j >= 0:
            if rows_ok:
                covered.update(range(j, j + len(snip)))
            j = t.find(snip, j + 1)
        best, missing, srcs = fidelity(sentence_around(t, i, i + len(snip)), nums, src_sents)
        extra = fidelity_extra_tokens(snip)
        missing = [n for n in missing if n not in extra]
        if missing:
            fid_flags.append((sec, snip[:70], round(best, 2), missing, srcs))
        n_mis += (not rows_ok)
        report.append((sec, snip if len(snip) < 110 else snip[:107] + '...', ' '.join(nums), '; '.join(locs) + (' [' + '; '.join(vals) + ']' if vals else ''), 'match' if rows_ok else 'MISMATCH'))
    # coverage: every number in the masked body must be covered
    uncovered = [(s, t[s:e]) for s, e, _ in number_spans(masked) if s not in covered]
    total = len(number_spans(masked))
    if md:
        print('| # | Part | Text in submission (paper.tex) | Numbers | Source: file:line or JSON path [value used] | Result |')
        print('|---|---|---|---|---|---|')
        for k, (sec, snip, nums, loc, res) in enumerate(report, 1):
            esc = lambda x: x.replace('|', '\\|').replace('\n', ' ')
            print(f'| {k} | {sec} | `{esc(snip)}` | {esc(nums)} | {esc(loc)} | {res} |')
        print()
    print(f'Numbers in paper.tex body: {total}; covered by a check: {total - len(uncovered)}; uncovered: {len(uncovered)}')
    print(f'Checks: {len(report)}; mismatches: {n_mis}')
    print(f'Source-paper fidelity flags (number not in the most similar sentence of the full paper): {len(fid_flags)}')
    for f in fid_flags:
        print('  FIDELITY?', f)
    for s, x in uncovered:
        ctx = t[max(0, s - 40): s + 30].replace('\n', ' ')
        print(f'  UNCOVERED {x!r} at {s}: ...{ctx}...')
    sys.exit(0 if (n_mis == 0 and not uncovered) else 1)

if __name__ == '__main__':
    main()
