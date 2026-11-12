"""Run AFTER unblinding. Part 1 is a preregistered quantity that analysis.py omitted (section 7.5, median follower
distance). Part 2 is EXPLORATORY: analyses chosen after seeing the results, reported as such.
Usage: python3 supplementary.py WORKDIR RESULTS_DIR"""
import sys, os, json
import numpy as np, pandas as pd, statsmodels.api as sm
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import analysis as A
work, res = sys.argv[1], sys.argv[2]
rng = np.random.default_rng(A.SEED + 2); NB = 2000; out = {}
t = pd.read_csv(os.path.join(res, 'airport_day.csv')); t['date'] = [A.d(z) for z in t.date]; t['pdate'] = [A.d(z) for z in t.pdate]
wx = pd.read_csv(os.path.join(HERE, '..', 'data', 'weather_airport_day.csv')); wx['date'] = [A.d(z) for z in wx.date]

# ---- Part 1 (preregistered, 7.5): median follower distance by group, year and window
import glob
fr = []
for f in sorted(glob.glob(os.path.join(work, 'data/att/*.parquet'))):   # day by day to limit memory; rule 1 is a per-day rule
    q = pd.read_parquet(f, columns=['apt', 'icao', 'cls', 'callsign', 'outcome', 'gap_s', 'fol_nm']); q['date'] = A.d(os.path.basename(f)[:10])
    q, _ = A.apply_rule1(q); fr.append(q.loc[q.fol_nm.notna(), ['date', 'apt', 'fol_nm']])
a = pd.concat(fr, ignore_index=True); del fr
a = a.merge(t[['date', 'apt', 'us', 'year', 'pdate']], on=['date', 'apt'])   # kept airport-days only
print("loaded", len(a), file=sys.stderr, flush=True)
med = {}
for w in ('baseline', 'shutdown'):
    lo, hi = A.WINDOWS[w]; x = a[(a.pdate >= lo) & (a.pdate <= hi)]
    for (u, y), g in x.groupby(['us', 'year']):
        med[f"{w}_{'us' if u else 'ctl'}{y}"] = dict(median_nm=float(g.fol_nm.median()), p10_nm=float(g.fol_nm.quantile(0.1)), pairs=int(len(g)))
out['prereg_median_follower_nm'] = med
del a

# ---- Part 2 (exploratory)
print("part1 done", file=sys.stderr, flush=True)
EX = {}
# 2a weather-adjusted September placebo
EX['weather_adjusted_placebo_september'] = A.wx_adjusted(A.in_window(t, 'baseline'), wx, rng, NB)
print("2a done", file=sys.stderr, flush=True)
# 2b weather- and baseline-adjusted: both windows, airport x window fixed effects, year x window, year x US, year x US x shutdown
x = pd.concat([A.in_window(t, 'baseline').assign(sh=0), A.in_window(t, 'shutdown').assign(sh=1)]).merge(wx[['apt', 'date'] + A.WX], on=['apt', 'date']).reset_index(drop=True)
FE = pd.get_dummies(x.apt + '_' + x.sh.astype(str), dtype=float).values; y25 = (x.year == 2025).astype(float).values
core = np.column_stack([FE, y25, y25 * x.sh, y25 * x.us, y25 * x.us * x.sh]); k = FE.shape[1] + 3
off = np.log(x.n.values); yv = x.ga.values
def fit(X, wt=None):
    """Poisson regression by Newton iterations (same model as statsmodels GLM; written out because 4,000 refits of the
    library version exhausted memory). Columns that are all zero under the weights are dropped."""
    w = np.ones(len(yv)) if wt is None else wt
    m = w > 0; Xm, ym, om, wm = X[m], yv[m], off[m], w[m]
    keep = np.abs(Xm).sum(0) > 0; Xm = Xm[:, keep]; kk = int(keep[:k].sum())
    beta = np.zeros(Xm.shape[1]); beta_prev = beta + 1
    for _ in range(60):
        mu = np.exp(np.clip(Xm @ beta + om, -30, 30)); g = Xm.T @ (wm * (ym - mu)); H = (Xm * (wm * mu)[:, None]).T @ Xm
        step = np.linalg.lstsq(H + 1e-9 * np.eye(len(beta)), g, rcond=None)[0]; beta = beta + np.clip(step, -5, 5)
        if np.max(np.abs(step)) < 1e-8: break
    return float(beta[kk])
days = sorted(x.pdate.unique()); idx = {p: i for i, p in enumerate(days)}; di = x.pdate.map(idx).values
strata = [np.array([i for i, p in enumerate(days) if A.WINDOWS[w][0] <= p <= A.WINDOWS[w][1]]) for w in ('baseline', 'shutdown')]
for name, X in (('with_weather', np.column_stack([core, x[A.WX].values.astype(float)])), ('without_weather', core)):
    est = fit(X); b = []
    for _ in range(NB):
        cnt = np.zeros(len(days))
        for s in strata: np.add.at(cnt, rng.choice(s, len(s)), 1)
        try: b.append(fit(X, cnt[di]))
        except Exception: b.append(np.nan)
    lo, hi, se = A.ci(np.array(b)); EX[f'baseline_adjusted_{name}'] = dict(rrr=float(np.exp(est)), ci_day=[float(np.exp(lo)), float(np.exp(hi))], se_log_day=se)
print("2b done", file=sys.stderr, flush=True)
# 2c TCAS RA ratio by phase (phase A is before the flight-reduction order and the general-aviation restrictions)
def ra_stat(z, w):
    g = z[z.us == 1].groupby(['w', 'year'])[['ra', 'n']].sum(); r = g.ra / g.n
    return float(np.log((r[(w, 2025)] / r[('baseline', 2025)]) / (r[(w, 2024)] / r[('baseline', 2024)])))
for w in ('phaseA', 'phaseB'):
    z = pd.concat([A.in_window(t, 'baseline').assign(w='baseline'), A.in_window(t, w).assign(w=w)])
    A.WINDOWS['_tmp'] = A.WINDOWS[w]; e = ra_stat(z, w)
    b = A.boot_days(z, lambda q: ra_stat(q, w), rng, NB, strata=['baseline', w]); lo, hi, se = A.ci(b)
    EX[f'ra_{w}'] = dict(ratio=float(np.exp(e)), ci_day=[float(np.exp(lo)), float(np.exp(hi))])
# 2d spacing: per-airport change in tight-pair share, to show what drives the pooled estimate
c = A.cells(A.in_window(t, 'shutdown'), 'tight', 'pairs'); c['rr'] = (c.k25 / c.n25) / (c.k24 / c.n24)
EX['spacing_airport_rr'] = {('us' if u else 'ctl'): dict(median=float(g.rr.median()), q25=float(g.rr.quantile(.25)), q75=float(g.rr.quantile(.75)),
                            share_above_1=float((g.rr > 1).mean()), n=int(len(g))) for u, g in c[(c.k24 > 20) & (c.k25 > 20)].groupby('us')}
# 2e approaches per day, year on year, by phase (did traffic fall?)
EX['approaches_ratio_2025_over_2024'] = {}
for w in ('baseline', 'phaseA', 'phaseB'):
    g = A.in_window(t, w).groupby(['grp', 'year']).n.sum().unstack()
    EX['approaches_ratio_2025_over_2024'][w] = (g[2025] / g[2024]).round(3).to_dict()
out['exploratory'] = EX
json.dump(out, open(os.path.join(res, 'supplementary.json'), 'w'), indent=1, default=float)
print(json.dumps(out, indent=1, default=float))
