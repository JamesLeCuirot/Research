"""Figures from the analysis outputs. Usage: python3 figures.py RESULTS_DIR FIG_DIR"""
import sys, os, json
import numpy as np, pandas as pd
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, '..', '..', '_build'))
from palette import apply_style, NEUTRAL
apply_style()
BLUE, ORANGE = '#0072B2', '#E69F00'
res, fig = sys.argv[1], sys.argv[2]; os.makedirs(fig, exist_ok=True)
R = json.load(open(os.path.join(res, 'results.json'))); W = pd.read_csv(os.path.join(res, 'weekly.csv'))
W = W[W.week <= 10]            # weeks 0-10 are complete 7-day weeks (1 Sep - 16 Nov)
wk_lab = pd.to_datetime('2025-09-01') + pd.to_timedelta(W.week * 7, unit='D')
W['start'] = wk_lab
SH0, SH1, ORD = pd.Timestamp('2025-10-01'), pd.Timestamp('2025-11-12'), pd.Timestamp('2025-11-07')

def weekly_panel(ax, col, us, title, ylabel):
    for y, c, ls in ((2024, NEUTRAL, '--'), (2025, BLUE if us else ORANGE, '-')):
        g = W[(W.us == us) & (W.year == y)].sort_values('week')
        ax.plot(g.start + pd.Timedelta(days=3), g[col], ls, color=c, marker='o', ms=3, lw=1.3,
                label=f'{y}' + (' (same weekdays)' if y == 2024 else ''))
    ax.axvspan(SH0, SH1, color='#999999', alpha=0.15, lw=0); ax.axvline(ORD, color='#D55E00', lw=0.8, ls=':')
    ax.set_title(title, loc='left'); ax.set_ylabel(ylabel); ax.set_ylim(bottom=0)
    ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%d %b')); ax.tick_params(axis='x', rotation=30)

def weekly_fig(col, ylabel, name, groups=(1, 0)):
    f, axs = plt.subplots(1, len(groups), figsize=(6.3 if len(groups) == 2 else 3.6, 2.8), sharey=True, squeeze=False)
    for ax, us in zip(axs[0], groups):
        weekly_panel(ax, col, us, 'US study airports' if us else 'Control airports (Canada, Europe)', ylabel if ax is axs[0][0] else '')
        ax.legend(frameon=False, loc='lower left', fontsize=7)
    f.tight_layout(); f.savefig(os.path.join(fig, name)); plt.close(f)

weekly_fig('ga_per_1000', 'Go-arounds per 1,000 approaches', 'fig_weekly_goaround.pdf')
weekly_fig('tight_pct', 'Pairs under 2.5 NM (%)', 'fig_weekly_spacing.pdf')
weekly_fig('ra_per_1000', 'RA events per 1,000 approaches', 'fig_weekly_ra.pdf', groups=(1,))

# per-airport forest
P = pd.DataFrame(R['per_airport']); P = P[(P.ga24 > 0) & (P.ga25 > 0)]
f, axs = plt.subplots(1, 2, figsize=(6.3, 7.2), gridspec_kw=dict(width_ratios=[1, 1]))
for ax, us, c in ((axs[0], 1, BLUE), (axs[1], 0, ORANGE)):
    g = P[P.us == us].sort_values('rr').reset_index(drop=True); yy = np.arange(len(g))
    ax.hlines(yy, g.rr_lo.clip(lower=0.1), g.rr_hi.clip(upper=10), color=c, lw=1); ax.plot(g.rr, yy, 'o', color=c, ms=3)
    ax.axvline(1, color=NEUTRAL, lw=0.8); ax.set_xscale('log'); ax.set_xlim(0.2, 5)
    ax.set_xticks([0.25, 0.5, 1, 2, 4]); ax.set_xticklabels(['0.25', '0.5', '1', '2', '4']); ax.minorticks_off()
    ax.set_yticks(yy); ax.set_yticklabels([a[1:] if (us and a.startswith('K')) else a for a in g.apt], fontsize=6.5)
    ax.set_ylim(-1, max(len(g), 1)); ax.grid(axis='y', visible=False)
    ax.set_title('US airports' if us else 'Control airports', loc='left'); ax.set_xlabel('Go-around rate, 2025 ÷ 2024')
f.tight_layout(); f.savefig(os.path.join(fig, 'fig_airport_forest.pdf')); plt.close(f)

# estimates summary
rows = [('Primary: shutdown, all airports', 'primary'), ('September placebo (before shutdown)', 'placebo_september'),
        ('Shutdown, adjusted for September', 'baseline_adjusted'), ('Weather-adjusted', ('weather_adjusted', 'adjusted')),
        ('Phase A: 1 Oct–6 Nov', 'phaseA'), ('Phase B: 7–16 Nov (flight cuts)', 'phaseB'), ('Peak staffing strain: 31 Oct–9 Nov', 'peak'),
        ('FAA-order airports only', 'group_US40'), ('Other US airports only', 'group_USOTHER'),
        ('Europe as only control', 'control_europe_only'), ('Canada as only control', 'control_canada_only'),
        ('Airline jets only', 'airline_jets_only'), ('Without training-flight exclusion', 'without_rule1')]
f, ax = plt.subplots(figsize=(6.3, 3.6)); labs = []
ax.axvspan(0.80, 1.25, color='#999999', alpha=0.15, lw=0); ax.axvline(1, color=NEUTRAL, lw=0.8)
for i, (lab, k) in enumerate(rows):
    e = R.get(k[0], {}).get(k[1]) if isinstance(k, tuple) else R.get(k)
    if not e: continue
    y = -len(labs); labs.append(lab); lo, hi = e['ci_day']
    ax.hlines(y, lo, hi, color=BLUE, lw=1.4 if k == 'primary' else 1); ax.plot(e['rrr'], y, 'o', color=BLUE, ms=5 if k == 'primary' else 3.5)
ax.set_yticks(-np.arange(len(labs))); ax.set_yticklabels(labs); ax.set_xscale('log')
xt = [0.6, 0.8, 1, 1.25, 1.6, 2]; ax.set_xticks(xt); ax.set_xticklabels([str(v) for v in xt]); ax.minorticks_off(); ax.grid(axis='y', visible=False)
ax.set_xlabel('Ratio of rate ratios (US change ÷ control change), 95% interval'); f.tight_layout()
f.savefig(os.path.join(fig, 'fig_estimates.pdf')); plt.close(f)
print('figures written to', fig)
