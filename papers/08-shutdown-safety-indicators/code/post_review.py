"""EXPLORATORY checks added after the independent reviews (not preregistered). They reproduce, with this repository's
own code, the reviewers' findings that the revised paper relies on.
Usage: python3 post_review.py WORKDIR RESULTS_DIR"""
import sys, os, json, glob, gzip
import numpy as np, pandas as pd
from scipy import stats
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import analysis as A
work, res = sys.argv[1], sys.argv[2]
rng = np.random.default_rng(A.SEED + 3); NB = 2000; out = {}
t = pd.read_csv(os.path.join(res, 'airport_day.csv')); t['date'] = [A.d(z) for z in t.date]; t['pdate'] = [A.d(z) for z in t.pdate]
wx = pd.read_csv(os.path.join(HERE, '..', 'data', 'weather_airport_day.csv')); wx['date'] = [A.d(z) for z in wx.date]
sh = A.in_window(t, 'shutdown'); base = A.in_window(t, 'baseline')
def rr(x, num='ga', den='n'): return A.log_rrr(x, num, den)
def summ(est, b): lo, hi, se = A.ci(np.asarray(b)); return dict(rrr=float(np.exp(est)), ci=[float(np.exp(lo)), float(np.exp(hi))], se_log=se)

# 1. ACAS logging: messages per day and share with a position, from the raw daily files
rows = []
for f in sorted(glob.glob(os.path.join(work, 'data/acas/*.json.gz'))):
    n = pos = 0
    for line in gzip.open(f, 'rt', errors='replace'):
        if '"acas_ra"' not in line: continue
        n += 1; pos += ('"lat":' in line)
    rows.append(dict(date=os.path.basename(f)[:10], messages=n, share_with_position=round(pos / max(n, 1), 4)))
ac = pd.DataFrame(rows); ac.to_csv(os.path.join(res, 'acas_daily.csv'), index=False)
ac['d'] = [A.d(z) for z in ac.date]
def med(a, b): return float(ac[(ac.d >= A.d(a)) & (ac.d <= A.d(b))].messages.median())
out['acas_messages_per_day_median'] = {'2024-09-02..09-25': med('2024-09-02', '2024-09-25'), '2024-09-27..11-08': med('2024-09-27', '2024-11-08'),
                                       '2024-11-10..11-17': med('2024-11-10', '2024-11-17'), '2025-09-01..11-16': med('2025-09-01', '2025-11-16')}
out['acas_share_with_position_mean'] = {'2024-09-02..09-25': float(ac[ac.d <= A.d('2024-09-25')].share_with_position.mean()),
                                        '2024-09-27..11-17': float(ac[(ac.d >= A.d('2024-09-27')) & (ac.d.map(lambda z: z.year) == 2024)].share_with_position.mean()),
                                        '2025': float(ac[ac.d.map(lambda z: z.year) == 2025].share_with_position.mean())}
# RA ratio with the September baseline split at the 2024 logging change (2025-equivalent dates)
def ra_ratio(x):
    g = x[x.us == 1].groupby(['w', 'year'])[['ra', 'n']].sum(); r = g.ra / g.n
    return float(np.log((r[('s', 2025)] / r[('b', 2025)]) / (r[('s', 2024)] / r[('b', 2024)])))
for name, (b0, b1) in (('ra_baseline_1_24_Sep', ('2025-09-01', '2025-09-24')), ('ra_baseline_26_30_Sep', ('2025-09-26', '2025-09-30'))):
    A.WINDOWS['_b'] = (A.d(b0), A.d(b1)); x = pd.concat([A.in_window(t, '_b').assign(w='b'), sh.assign(w='s')])
    b = A.boot_days(x, ra_ratio, rng, NB, strata=['_b', 'shutdown']); out[name] = summ(ra_ratio(x), b)
    g = x[x.us == 1].groupby(['w', 'year'])[['ra', 'n']].sum(); out[name]['rates_per_1000'] = {f'{w}{y}': float(1000 * g.loc[(w, y), 'ra'] / g.loc[(w, y), 'n']) for (w, y) in g.index}
x = pd.concat([base.assign(w='b'), sh.assign(w='s')]); x = x[x.apt != 'KSFO']; out['ra_excl_SFO'] = summ(ra_ratio(x), A.boot_days(x, ra_ratio, rng, NB, strata=['baseline', 'shutdown']))
g = sh[sh.us == 1].groupby(['apt', 'year']).ra.sum().unstack(); out['ra_SFO_share_of_window_events'] = {str(y): float(g.loc['KSFO', y] / g[y].sum()) for y in (2024, 2025)}

# 2. Per-airport: Holm adjustment and a no-change calibration of the exact test (split one year's days at random)
c = A.cells(sh, 'ga', 'n'); p = []
for a, r in c.iterrows():
    tot = int(r.k24 + r.k25); p.append((a, int(r.us), stats.binomtest(int(r.k25), tot, r.n25 / (r.n24 + r.n25)).pvalue if tot else 1.0))
P = pd.DataFrame(p, columns=['apt', 'us', 'p']).sort_values('p').reset_index(drop=True)
def holm(q): m = len(q); adj = np.maximum.accumulate((m - np.arange(m)) * q.values); return np.minimum(adj, 1)
P['holm_all'] = holm(P.p); out['per_airport_nominal_p_below_0.05'] = int((P.p < 0.05).sum())
out['per_airport_holm_survivors_all76'] = P[P.holm_all < 0.05].apt.tolist()
U = P[P.us == 1].reset_index(drop=True); out['per_airport_holm_survivors_us50'] = U[holm(U.p) < 0.05].apt.tolist()
cal = {}
for y in (2024, 2025):
    z = sh[sh.year == y]; days = np.array(sorted(z.pdate.unique())); cnt = []
    piv = {k: z.pivot_table(index='apt', columns='pdate', values=k, aggfunc='sum', fill_value=0).reindex(columns=days, fill_value=0) for k in ('ga', 'n')}
    for _ in range(1000):
        m = np.zeros(len(days), bool); m[rng.choice(len(days), len(days) // 2, replace=False)] = True
        k1, k0 = piv['ga'].values[:, m].sum(1), piv['ga'].values[:, ~m].sum(1); n1, n0 = piv['n'].values[:, m].sum(1), piv['n'].values[:, ~m].sum(1)
        cnt.append(sum(stats.binomtest(int(a1), int(a1 + a0), b1 / (b1 + b0)).pvalue < 0.05 for a1, a0, b1, b0 in zip(k1, k0, n1, n0) if a1 + a0 > 0))
    cal[str(y)] = dict(mean=float(np.mean(cnt)), p2_5=float(np.percentile(cnt, 2.5)), p97_5=float(np.percentile(cnt, 97.5)))
out['per_airport_false_positive_calibration'] = cal

# 3. Serial correlation: circular block bootstrap of day-pairs for the primary estimate
days = sorted(sh.pdate.unique()); by = {p_: g for p_, g in sh.groupby('pdate')}
for L in (3, 7):
    b = []
    for _ in range(NB):
        idx = []
        while len(idx) < len(days):
            s = rng.integers(0, len(days)); idx += [(s + j) % len(days) for j in range(L)]
        b.append(rr(pd.concat([by[days[i]] for i in idx[:len(days)]], ignore_index=True)))
    out[f'primary_block_bootstrap_{L}day'] = summ(rr(sh), b); out[f'primary_block_bootstrap_{L}day']['mde_rel'] = float(np.exp(2.8 * out[f'primary_block_bootstrap_{L}day']['se_log']) - 1)

# 4. Where in the window: two-part split and weekly estimates
for name, (a0, a1) in (('primary_1_14_Oct', ('2025-10-01', '2025-10-14')), ('primary_15Oct_12Nov', ('2025-10-15', '2025-11-12'))):
    A.WINDOWS['_s'] = (A.d(a0), A.d(a1)); x = A.in_window(t, '_s'); out[name] = summ(rr(x), A.boot_days(x, rr, rng, NB))
wk = {}
for k in range(11):
    lo = A.d('2025-09-01') + pd.Timedelta(days=7 * k).to_pytimedelta(); A.WINDOWS['_w'] = (lo, lo + pd.Timedelta(days=6).to_pytimedelta()); wk[str(lo)] = float(np.exp(rr(A.in_window(t, '_w'))))
out['weekly_rrr'] = wk
# September placebo without the Hurricane Helene days (24-28 Sep 2025-equivalent)
x = base[~((base.pdate >= A.d('2025-09-24')) & (base.pdate <= A.d('2025-09-28')))]; out['placebo_without_24_28_Sep'] = summ(rr(x), A.boot_days(x, rr, rng, NB))
s25 = base[base.year == 2025].groupby('apt')[['ga', 'n']].sum(); s24 = base[base.year == 2024].groupby('apt')[['ga', 'n']].sum()
lower = ((s25.ga / s25.n) < (s24.ga / s24.n)); us = base.groupby('apt').us.first()
out['september_airports_with_lower_2025_rate'] = dict(us=f"{int(lower[us == 1].sum())} of {int((us == 1).sum())}", control=f"{int(lower[us == 0].sum())} of {int((us == 0).sum())}")

# 5. Weather model with weather effects allowed to differ between US and control airports
x = sh.merge(wx[['apt', 'date'] + A.WX], on=['apt', 'date']).reset_index(drop=True)
FE = pd.get_dummies(x.apt, dtype=float).values; y25 = (x.year == 2025).astype(float).values; W = x[A.WX].values.astype(float)
X = np.column_stack([FE, y25, y25 * x.us.values, W, W * x.us.values[:, None]]); k = FE.shape[1] + 1; off = np.log(x.n.values); yv = x.ga.values
def fit(wt=None):
    w = np.ones(len(yv)) if wt is None else wt; m = w > 0; Xm, ym, om, wm = X[m], yv[m], off[m], w[m]
    keep = np.abs(Xm).sum(0) > 0; Xm = Xm[:, keep]; kk = int(keep[:k].sum()); beta = np.zeros(Xm.shape[1])
    for _ in range(60):
        mu = np.exp(np.clip(Xm @ beta + om, -30, 30)); step = np.linalg.lstsq((Xm * (wm * mu)[:, None]).T @ Xm + 1e-9 * np.eye(len(beta)), Xm.T @ (wm * (ym - mu)), rcond=None)[0]
        beta = beta + np.clip(step, -5, 5)
        if np.max(np.abs(step)) < 1e-8: break
    return float(beta[kk]), beta
est, beta = fit(); dlist = sorted(x.pdate.unique()); di = x.pdate.map({p_: i for i, p_ in enumerate(dlist)}).values
b = [fit(np.bincount(rng.integers(0, len(dlist), len(dlist)), minlength=len(dlist))[di].astype(float))[0] for _ in range(NB)]
out['weather_adjusted_with_US_interactions'] = summ(est, b)
out['weather_rate_ratios_control'] = {c_: float(np.exp(beta[k + 1 + i])) for i, c_ in enumerate(A.WX)}
out['weather_rate_ratios_us'] = {c_: float(np.exp(beta[k + 1 + i] + beta[k + 4 + i])) for i, c_ in enumerate(A.WX)}

# 6. Coverage: restrict to airports whose detected approaches changed little between the years (shutdown window)
n = sh.groupby(['apt', 'year']).n.sum().unstack(); ratio = n[2025] / n[2024]
out['approach_count_ratio_outliers'] = ratio[(ratio > 1.25) | (ratio < 0.8)].round(2).to_dict()
keep = ratio[(ratio >= 0.8) & (ratio <= 1.25)].index
x = sh[sh.apt.isin(keep)]; out['primary_stable_coverage_airports'] = dict(summ(rr(x), A.boot_days(x, rr, rng, NB)), airports=int(len(keep)))
x = base[base.apt.isin(keep)]; out['placebo_stable_coverage_airports'] = summ(rr(x), A.boot_days(x, rr, rng, NB))

# 7. Spacing: airport bootstrap for the baseline-adjusted estimate (registered main spacing result; omitted from analysis.py)
both = pd.concat([sh.assign(w='shutdown'), base.assign(w='baseline')])
def adj(z): return A.log_rrr(z[z.w == 'shutdown'], 'tight', 'pairs') - A.log_rrr(z[z.w == 'baseline'], 'tight', 'pairs')
out['spacing_baseline_adjusted_airport_bootstrap'] = summ(adj(both), A.boot_airports(both, adj, rng, NB))
def adjg(z): return A.log_rrr(z[z.w == 'shutdown'], 'ga', 'n') - A.log_rrr(z[z.w == 'baseline'], 'ga', 'n')
out['goaround_baseline_adjusted_airport_bootstrap'] = summ(adjg(both), A.boot_airports(both, adjg, rng, NB))
out['approaches_in_analysis'] = int(t.n.sum())
json.dump(out, open(os.path.join(res, 'post_review.json'), 'w'), indent=1, default=float)
def r(v):
    if isinstance(v, float): return round(v, 3)
    if isinstance(v, dict): return {a: r(b_) for a, b_ in v.items()}
    if isinstance(v, list): return [r(b_) for b_ in v]
    return v
print(json.dumps(r(out)))
