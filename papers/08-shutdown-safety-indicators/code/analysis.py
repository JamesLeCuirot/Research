"""Pre-registered analysis (PREREGISTRATION.md section 7). Committed before first use on study data.
Usage: python3 analysis.py WORKDIR OUTDIR [--selftest]
Reads WORKDIR/data/att/*.parquet and WORKDIR/data/acas/*.json.gz; writes airport_day.csv, results.json, RESULTS.md."""
import sys, os, glob, gzip, json, datetime as dt
import numpy as np, pandas as pd
import statsmodels.api as sm
from scipy import stats
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from actypes import BIZJET, AIRLINE
NBOOT = 2000; SEED = 20261111
G = pd.read_csv(os.path.join(HERE, 'airports_study.csv'))
G['us'] = G.grp.isin(['US40', 'USOTHER']).astype(int)

# ---------------------------------------------------------------- windows (2025-equivalent dates)
def d(s): return dt.date.fromisoformat(s)
WINDOWS = {'baseline': (d('2025-09-01'), d('2025-09-30')), 'shutdown': (d('2025-10-01'), d('2025-11-12')),
           'phaseA': (d('2025-10-01'), d('2025-11-06')), 'phaseB': (d('2025-11-07'), d('2025-11-16')),
           'peak': (d('2025-10-31'), d('2025-11-09'))}
def pair_date(date):   # map an archive day to its 2025-equivalent (weekday-aligned) date
    return date if date.year == 2025 else date + dt.timedelta(364)

# ---------------------------------------------------------------- build airport-day table
def load_attempts(work):
    fr = []
    for f in sorted(glob.glob(os.path.join(work, 'data/att/*.parquet'))):
        a = pd.read_parquet(f, columns=['apt', 'icao', 'cls', 'callsign', 'outcome', 'gap_s', 'fol_nm'])
        a['date'] = d(os.path.basename(f)[:10]); fr.append(a)
    return pd.concat(fr, ignore_index=True)

def apply_rule1(a):
    """Remove training/test/flight-inspection activity: aircraft with >=3 go-arounds at one airport on one UTC day
    (all their attempts there that day), and FLC callsigns."""
    ga = a[a.outcome == 'ga'].groupby(['date', 'apt', 'icao']).size()
    rep = ga[ga >= 3].index
    key = pd.MultiIndex.from_frame(a[['date', 'apt', 'icao']])
    m_rep = key.isin(rep)
    m_flc = a.callsign.fillna('').astype(str).str.startswith('FLC').values
    info = dict(removed_attempts_repeat=int(m_rep.sum()), removed_ga_repeat=int((m_rep & (a.outcome == 'ga').values).sum()),
                removed_attempts_flc=int((m_flc & ~m_rep).sum()))
    return a[~(m_rep | m_flc)], info

def ra_events(work):
    """RA events near US study airports: first RA message per aircraft after >=120 s without one; study types;
    within 15 NM and below 7,000 ft above the nearest study airport."""
    ap = pd.read_csv(os.path.join(work, 'ref/airports.csv'), usecols=['ident', 'latitude_deg', 'longitude_deg', 'elevation_ft'])
    ap = ap.merge(G, left_on='ident', right_on='icao')
    AL = np.radians(ap.latitude_deg.values)[None, :]; AO = np.radians(ap.longitude_deg.values)[None, :]
    rows = []
    for f in sorted(glob.glob(os.path.join(work, 'data/acas/*.json.gz'))):
        date = d(os.path.basename(f)[:10]); last = {}; ev = []
        try:
            for line in gzip.open(f, 'rt', errors='replace'):
                line = line.strip().rstrip(',')
                if not line.startswith('{'): continue
                try: x = json.loads(line)
                except Exception: continue
                r = x.get('acas_ra') or {}; t = r.get('unix_timestamp'); h = x.get('hex')
                if t is None or h is None: continue
                if h not in last or t - last[h] > 120:
                    ev.append((x.get('lat'), x.get('lon'), x.get('alt_baro'), x.get('t'), r.get('advisory')))
                last[h] = t
        except Exception as e:
            print('ACAS read problem', f, repr(e), file=sys.stderr)
        e = pd.DataFrame(ev, columns=['lat', 'lon', 'alt', 'typ', 'adv']).dropna(subset=['lat', 'lon'])
        if not len(e): continue
        e['alt'] = pd.to_numeric(e.alt, errors='coerce')
        la = np.radians(e.lat.values)[:, None]; lo = np.radians(e.lon.values)[:, None]
        dd = np.hypot((lo - AO) * np.cos((la + AL) / 2), la - AL) * 3440.065
        j = dd.argmin(1); e['dmin'] = dd[np.arange(len(e)), j]; e['apt'] = ap.icao.values[j]
        e['agl'] = e.alt - ap.elevation_ft.fillna(0).values[j]
        e = e[(e.dmin < 15) & (e.agl < 7000) & e.typ.isin(BIZJET | AIRLINE)]
        e['date'] = date; e['coc'] = e.adv.fillna('').str.contains('Clear of Conflict')
        rows.append(e[['date', 'apt', 'coc']])
    return pd.concat(rows, ignore_index=True) if rows else pd.DataFrame(columns=['date', 'apt', 'coc'])

def airport_day(a, ra=None, air_only=False):
    if air_only: a = a[a.cls == 'air']
    a = a.assign(ga=(a.outcome == 'ga').astype(int), pair=a.fol_nm.notna().astype(int), tight=(a.fol_nm < 2.5).astype(int))
    t = a.groupby(['date', 'apt']).agg(n=('ga', 'size'), ga=('ga', 'sum'), pairs=('pair', 'sum'), tight=('tight', 'sum')).reset_index()
    if ra is not None and len(ra):
        r = ra.groupby(['date', 'apt']).agg(ra=('coc', 'size'), ra_nococ=('coc', lambda s: int((~s).sum()))).reset_index()
        t = t.merge(r, on=['date', 'apt'], how='left')
    for c in ('ra', 'ra_nococ'):
        if c not in t: t[c] = 0
        t[c] = t[c].fillna(0).astype(int)
    t['year'] = [x.year for x in t.date]; t['pdate'] = [pair_date(x) for x in t.date]
    return t.merge(G, left_on='apt', right_on='icao').drop(columns='icao')

def apply_rules23(t, ndays=77):
    t = t[t.n >= 30]
    ok = t.groupby(['apt', 'year']).size().unstack(fill_value=0)
    for y in (2024, 2025):
        if y not in ok: ok[y] = 0
    keep = ok[(ok[2024] >= 60) & (ok[2025] >= 60)].index
    excluded = sorted(set(G.icao) - set(keep))
    return t[t.apt.isin(keep)], excluded, ok

def in_window(t, w):
    a, b = WINDOWS[w]; return t[(t.pdate >= a) & (t.pdate <= b)]

# ---------------------------------------------------------------- estimators
def cells(t, num, den):
    """Airport x year sums."""
    c = t.groupby(['apt', 'us', 'year'])[[num, den]].sum().unstack('year', fill_value=0)
    out = pd.DataFrame({'us': c.index.get_level_values('us'), 'k24': c[(num, 2024)].values, 'k25': c[(num, 2025)].values,
                        'n24': c[(den, 2024)].values, 'n25': c[(den, 2025)].values}, index=c.index.get_level_values('apt'))
    return out

def fe_poisson(c, treat='us'):
    """Poisson with airport fixed effects, year and year x treated, offset log(den). With two periods per airport this is
    exactly the conditional (binomial) likelihood: k25 | k24+k25 ~ Bin(p), logit p = log(n25/n24) + b + d*treated.
    Returns (log RRR, log year ratio in untreated)."""
    c = c[(c.k24 + c.k25 > 0) & (c.n24 > 0) & (c.n25 > 0)]
    if c[treat].nunique() < 2: return np.nan, np.nan
    X = np.column_stack([np.ones(len(c)), c[treat].values.astype(float)])
    y = np.column_stack([c.k25.values, c.k24.values])
    try:
        r = sm.GLM(y, X, family=sm.families.Binomial(), offset=np.log(c.n25.values / c.n24.values)).fit()
        return float(r.params[1]), float(r.params[0])
    except Exception:
        return np.nan, np.nan

def pooled(t, num, den):
    g = t.groupby(['us', 'year'])[[num, den]].sum()
    return {f"{'us' if u else 'ctl'}{y}": (int(g.loc[(u, y), num]), int(g.loc[(u, y), den])) for (u, y) in g.index}

def did_summary(t, num, den, per=1000.0):
    p = pooled(t, num, den); r = {k: per * v[0] / v[1] if v[1] else np.nan for k, v in p.items()}
    out = dict(counts=p, rates=r)
    if all(k in r for k in ('us2024', 'us2025', 'ctl2024', 'ctl2025')):
        out['rd_us'] = r['us2025'] - r['us2024']; out['rd_ctl'] = r['ctl2025'] - r['ctl2024']; out['did_rd'] = out['rd_us'] - out['rd_ctl']
        out['rr_us'] = r['us2025'] / r['us2024']; out['rr_ctl'] = r['ctl2025'] / r['ctl2024']; out['rrr_pooled'] = out['rr_us'] / out['rr_ctl']
    return out

def log_rrr(t, num, den, treat='us'):
    return fe_poisson(cells(t, num, den).rename(columns={'us': treat}) if treat == 'us' else cells_t(t, num, den, treat), treat)[0]

def cells_t(t, num, den, treat):
    c = t.groupby(['apt', treat, 'year'])[[num, den]].sum().unstack('year', fill_value=0)
    return pd.DataFrame({treat: c.index.get_level_values(treat), 'k24': c[(num, 2024)].values, 'k25': c[(num, 2025)].values,
                         'n24': c[(den, 2024)].values, 'n25': c[(den, 2025)].values}, index=c.index.get_level_values('apt'))

def boot_days(t, stat, rng, nboot=NBOOT, strata=None):
    """Resample weekday-aligned day-pairs (both years, all airports together). strata: list of windows resampled separately."""
    by = {p: g for p, g in t.groupby('pdate')}
    if strata is None: groups = [sorted(by)]
    else: groups = [[p for p in sorted(by) if WINDOWS[w][0] <= p <= WINDOWS[w][1]] for w in strata]
    res = []
    for _ in range(nboot):
        parts = []
        for days in groups:
            if not days: continue
            pick = rng.integers(0, len(days), len(days))
            u, cnt = np.unique(pick, return_counts=True)
            for i, k in zip(u, cnt):
                g = by[days[i]]
                parts.append(g if k == 1 else pd.concat([g] * k))
        res.append(stat(pd.concat(parts, ignore_index=True)))
    return np.array(res, dtype=float)

def boot_airports(t, stat, rng, nboot=NBOOT, treat='us'):
    by = {a: g for a, g in t.groupby('apt')}
    grp = t.groupby('apt')[treat].first()
    lists = [list(grp[grp == v].index) for v in sorted(grp.unique())]
    res = []
    for _ in range(nboot):
        parts = []; n = 0
        for L in lists:
            for i in rng.integers(0, len(L), len(L)):
                g = by[L[i]].copy(); g['apt'] = f'b{n}'; n += 1; parts.append(g)
        res.append(stat(pd.concat(parts, ignore_index=True)))
    return np.array(res, dtype=float)

def ci(b):
    b = b[np.isfinite(b)]
    if len(b) < 100: return [np.nan, np.nan, np.nan]
    return [float(np.percentile(b, 2.5)), float(np.percentile(b, 97.5)), float(np.std(b, ddof=1))]

def rrr_block(t, num, den, rng, treat='us', nboot=NBOOT, airports=True):
    est = log_rrr(t, num, den, treat)
    bd = boot_days(t, lambda x: log_rrr(x, num, den, treat), rng, nboot)
    lo, hi, se = ci(bd)
    out = dict(rrr=float(np.exp(est)), ci_day=[float(np.exp(lo)), float(np.exp(hi))], se_log_day=se,
               mde_rel=float(np.exp(2.8 * se) - 1) if np.isfinite(se) else np.nan)
    if airports:
        ba = boot_airports(t, lambda x: log_rrr(x, num, den, treat), rng, nboot, treat)
        lo2, hi2, se2 = ci(ba); out.update(ci_airport=[float(np.exp(lo2)), float(np.exp(hi2))], se_log_airport=se2)
    return out

def verdict(lo, hi):
    if not (np.isfinite(lo) and np.isfinite(hi)): return 'not estimable'
    if lo > 1 or hi < 1: return 'change detected'
    if lo >= 0.80 and hi <= 1.25: return 'no meaningful change'
    return 'inconclusive'

def exact_rr(k25, n25, k24, n24):
    """Rate ratio with exact conditional (Clopper-Pearson) interval."""
    if min(n24, n25) == 0 or k24 + k25 == 0: return (np.nan, np.nan, np.nan)
    tot = k24 + k25
    lo = stats.beta.ppf(0.025, k25, tot - k25 + 1) if k25 > 0 else 0.0
    hi = stats.beta.ppf(0.975, k25 + 1, tot - k25) if k25 < tot else 1.0
    f = lambda p: (p / (1 - p)) * (n24 / n25) if p < 1 else np.inf
    return ((k25 / n25) / (k24 / n24) if k24 > 0 else np.inf, f(lo), f(hi))

def dl_tau2(c):
    """DerSimonian-Laird heterogeneity of per-airport log rate ratios (airports with events in both years)."""
    c = c[(c.k24 > 0) & (c.k25 > 0)]
    y = np.log((c.k25 / c.n25) / (c.k24 / c.n24)); v = 1 / c.k24 + 1 / c.k25; w = 1 / v
    mu = (w * y).sum() / w.sum(); Q = (w * (y - mu) ** 2).sum(); k = len(c)
    tau2 = max(0.0, (Q - (k - 1)) / (w.sum() - (w ** 2).sum() / w.sum()))
    return dict(k=int(k), Q=float(Q), tau2=float(tau2), tau=float(np.sqrt(tau2)), I2=float(max(0, (Q - (k - 1)) / Q)) if Q > 0 else 0.0)

# ---------------------------------------------------------------- main analysis
def run(t, t_air, t_norule1, rng, nboot=NBOOT):
    R = {}
    sh = in_window(t, 'shutdown'); base = in_window(t, 'baseline')
    # 7.1 primary
    P = did_summary(sh, 'ga', 'n'); P.update(rrr_block(sh, 'ga', 'n', rng, nboot=nboot))
    dv = verdict(*P['ci_day']); av = verdict(*P['ci_airport'])
    wider = P['ci_day'] if (np.log(P['ci_day'][1]) - np.log(P['ci_day'][0])) >= (np.log(P['ci_airport'][1]) - np.log(P['ci_airport'][0])) else P['ci_airport']
    P['verdict'] = dv if (dv == 'change detected') == (av == 'change detected') else verdict(*wider)
    P['ci_for_conclusion'] = P['ci_day'] if (dv == 'change detected') == (av == 'change detected') else wider
    R['primary'] = P
    # 7.2 placebo, baseline-adjusted, phases, groups
    B = did_summary(base, 'ga', 'n'); B.update(rrr_block(base, 'ga', 'n', rng, nboot=nboot)); R['placebo_september'] = B
    both = pd.concat([sh.assign(w='shutdown'), base.assign(w='baseline')])
    def adj(x, num='ga', den='n'):
        return log_rrr(x[x.w == 'shutdown'], num, den) - log_rrr(x[x.w == 'baseline'], num, den)
    e = adj(both); bd = boot_days(both, adj, rng, nboot, strata=['baseline', 'shutdown']); lo_, hi_, se_ = ci(bd)
    R['baseline_adjusted'] = dict(rrr=float(np.exp(e)), ci_day=[float(np.exp(lo_)), float(np.exp(hi_))], se_log_day=se_)
    for w in ('phaseA', 'phaseB', 'peak'):
        x = in_window(t, w); S = did_summary(x, 'ga', 'n'); S.update(rrr_block(x, 'ga', 'n', rng, nboot=nboot, airports=False)); R[w] = S
    ctl = sh[sh.us == 0]
    for gname in ('US40', 'USOTHER'):
        x = pd.concat([sh[sh.grp == gname], ctl]); S = did_summary(x, 'ga', 'n'); S.update(rrr_block(x, 'ga', 'n', rng, nboot=nboot, airports=False)); R[f'group_{gname}'] = S
    xb = in_window(t, 'phaseB'); xb = xb[xb.us == 1].assign(t40=lambda z: (z.grp == 'US40').astype(int))
    eb = log_rrr(xb, 'ga', 'n', 't40'); bb = boot_days(xb, lambda z: log_rrr(z, 'ga', 'n', 't40'), rng, nboot); lo_, hi_, se_ = ci(bb)
    g_ = xb.groupby(['t40', 'year'])[['ga', 'n']].sum()
    R['phaseB_US40_vs_USOTHER'] = dict(rrr=float(np.exp(eb)), ci_day=[float(np.exp(lo_)), float(np.exp(hi_))],
                                       rates={f"{'US40' if a else 'USOTHER'}{y}": 1000 * g_.loc[(a, y), 'ga'] / g_.loc[(a, y), 'n'] for (a, y) in g_.index})
    for name, sel in (('control_europe_only', ['EU']), ('control_canada_only', ['CA'])):
        x = sh[(sh.us == 1) | sh.grp.isin(sel)]; S = did_summary(x, 'ga', 'n'); S.update(rrr_block(x, 'ga', 'n', rng, nboot=nboot, airports=False)); R[name] = S
    xa = in_window(t_air, 'shutdown'); S = did_summary(xa, 'ga', 'n'); S.update(rrr_block(xa, 'ga', 'n', rng, nboot=nboot, airports=False)); R['airline_jets_only'] = S
    xn = in_window(t_norule1, 'shutdown'); S = did_summary(xn, 'ga', 'n'); S.update(rrr_block(xn, 'ga', 'n', rng, nboot=nboot, airports=False)); R['without_rule1'] = S
    loo = {a: float(np.exp(log_rrr(sh[sh.apt != a], 'ga', 'n'))) for a in sorted(sh.apt.unique())}
    R['leave_one_out'] = dict(min=min(loo.values()), max=max(loo.values()), argmin=min(loo, key=loo.get), argmax=max(loo, key=loo.get))
    # 7.3 per airport
    c = cells(sh, 'ga', 'n'); pa = []
    for a, r in c.iterrows():
        rr, lo_, hi_ = exact_rr(r.k25, r.n25, r.k24, r.n24)
        pa.append(dict(apt=a, us=int(r.us), ga24=int(r.k24), n24=int(r.n24), ga25=int(r.k25), n25=int(r.n25), rate24=1000 * r.k24 / r.n24, rate25=1000 * r.k25 / r.n25,
                       rd=1000 * (r.k25 / r.n25 - r.k24 / r.n24), rr=rr, rr_lo=lo_, rr_hi=hi_))
    R['per_airport'] = pa; R['heterogeneity_us'] = dl_tau2(c[c.us == 1]); R['heterogeneity_ctl'] = dl_tau2(c[c.us == 0])
    # 7.5 spacing
    S = did_summary(sh, 'tight', 'pairs', per=100.0); S.update(rrr_block(sh, 'tight', 'pairs', rng, nboot=nboot)); R['spacing_shutdown'] = S
    S = did_summary(base, 'tight', 'pairs', per=100.0); S.update(rrr_block(base, 'tight', 'pairs', rng, nboot=nboot, airports=False)); R['spacing_placebo'] = S
    e = adj(both, 'tight', 'pairs'); bd = boot_days(both, lambda x: adj(x, 'tight', 'pairs'), rng, nboot, strata=['baseline', 'shutdown']); lo_, hi_, se_ = ci(bd)
    R['spacing_baseline_adjusted'] = dict(rrr=float(np.exp(e)), ci_day=[float(np.exp(lo_)), float(np.exp(hi_))], se_log_day=se_)
    # 7.6 TCAS RA (US only): (shutdown/baseline in 2025) / (shutdown/baseline in 2024)
    def ra_stat(x, col='ra'):
        g = x[x.us == 1].groupby(['w', 'year'])[[col, 'n']].sum(); r = g[col] / g['n']
        try: return float(np.log((r[('shutdown', 2025)] / r[('baseline', 2025)]) / (r[('shutdown', 2024)] / r[('baseline', 2024)])))
        except Exception: return np.nan
    for name, x, col in (('ra_main', both, 'ra'), ('ra_excl_DCA_BUR', both[~both.apt.isin(['KDCA', 'KBUR'])], 'ra'), ('ra_excl_clear_of_conflict', both, 'ra_nococ')):
        e = ra_stat(x, col); bd = boot_days(x, lambda z: ra_stat(z, col), rng, nboot, strata=['baseline', 'shutdown']); lo_, hi_, se_ = ci(bd)
        g = x[x.us == 1].groupby(['w', 'year'])[[col, 'n']].sum()
        R[name] = dict(ratio=float(np.exp(e)), ci_day=[float(np.exp(lo_)), float(np.exp(hi_))], se_log_day=se_,
                       counts={f'{w}{y}': (int(g.loc[(w, y), col]), int(g.loc[(w, y), 'n'])) for (w, y) in g.index},
                       rates_per_1000={f'{w}{y}': 1000 * g.loc[(w, y), col] / g.loc[(w, y), 'n'] for (w, y) in g.index})
    # 7.7 Holm across H2 (baseline-adjusted spacing) and H3 (RA main), using bootstrap two-sided p-values
    def bp(est, se): return float(2 * (1 - stats.norm.cdf(abs(est) / se))) if se and np.isfinite(se) and se > 0 else np.nan
    p2 = bp(np.log(R['spacing_baseline_adjusted']['rrr']), R['spacing_baseline_adjusted']['se_log_day']); p3 = bp(np.log(R['ra_main']['ratio']), R['ra_main']['se_log_day'])
    ps = sorted([('H2_spacing', p2), ('H3_tcas', p3)], key=lambda z: z[1]); R['holm'] = {ps[0][0]: min(1, 2 * ps[0][1]), ps[1][0]: min(1, max(2 * ps[0][1], ps[1][1]))}
    R['holm_raw_p'] = dict(H2_spacing=p2, H3_tcas=p3)
    return R

# ---------------------------------------------------------------- 7.4 weather-adjusted secondary model
WX = ['lowvis_share', 'gust25', 'ts']
def wx_adjusted(sh, wx, rng, nboot=NBOOT):
    """Airport-day Poisson on the shutdown window: airport fixed effects, year, year x US, the three preregistered weather
    covariates, offset log(approaches). Day-pair bootstrap by reweighting. Also returns the same model without covariates
    on the same airport-days, so the effect of adjustment is visible."""
    x = sh.merge(wx[['apt', 'date'] + WX], on=['apt', 'date'], how='left')
    miss = int(x[WX].isna().any(axis=1).sum()); x = x.dropna(subset=WX).reset_index(drop=True)
    A = pd.get_dummies(x.apt, dtype=float).values; y25 = (x.year == 2025).astype(float).values
    core = np.column_stack([A, y25, y25 * x.us.values]); k = A.shape[1] + 1
    Xa = np.column_stack([core, x[WX].values.astype(float)]); off = np.log(x.n.values); yv = x.ga.values
    def fit(X, wt=None):
        m = slice(None) if wt is None else wt > 0
        return sm.GLM(yv[m], X[m], family=sm.families.Poisson(), offset=off[m], freq_weights=None if wt is None else wt[m]).fit()
    ra, ru = fit(Xa), fit(core)
    days = sorted(x.pdate.unique()); idx = {p: i for i, p in enumerate(days)}; di = x.pdate.map(idx).values
    ba, bu = [], []
    for _ in range(nboot):
        wt = np.bincount(rng.integers(0, len(days), len(days)), minlength=len(days))[di].astype(float)
        try: ba.append(fit(Xa, wt).params[k]); bu.append(fit(core, wt).params[k])
        except Exception: ba.append(np.nan); bu.append(np.nan)
    la, ha, sa = ci(np.array(ba)); lu, hu, su = ci(np.array(bu))
    return dict(airport_days=int(len(x)), airport_days_without_weather=miss,
                adjusted=dict(rrr=float(np.exp(ra.params[k])), ci_day=[float(np.exp(la)), float(np.exp(ha))], se_log_day=sa),
                unadjusted_same_days=dict(rrr=float(np.exp(ru.params[k])), ci_day=[float(np.exp(lu)), float(np.exp(hu))], se_log_day=su),
                covariate_rate_ratios={c: float(np.exp(ra.params[k + 1 + i])) for i, c in enumerate(WX)},
                covariate_means={f"{'us' if u else 'ctl'}{y}": g[WX].mean().round(4).to_dict() for (u, y), g in x.groupby(['us', 'year'])})

def weekly(t):
    x = t.copy(); x['week'] = [(p - d('2025-09-01')).days // 7 for p in x.pdate]
    g = x.groupby(['us', 'year', 'week'])[['ga', 'n', 'tight', 'pairs', 'ra']].sum().reset_index()
    g['ga_per_1000'] = 1000 * g.ga / g.n; g['tight_pct'] = 100 * g.tight / g.pairs; g['ra_per_1000'] = 1000 * g.ra / g.n
    return g

def selftest():
    """Synthetic check: planted RRR of 1.30 must be recovered and the placebo must be near 1."""
    rng = np.random.default_rng(1); rows = []
    days25 = [d('2025-09-01') + dt.timedelta(i) for i in range(77)]
    for _, a in G.iterrows():
        base = rng.uniform(0.002, 0.006); vol = rng.integers(60, 600)
        for p in days25:
            for y in (2024, 2025):
                date = p if y == 2025 else p - dt.timedelta(364)
                lv = float(rng.random() < 0.2) * rng.random(); wx = np.exp(rng.normal(0, 0.4) + 1.5 * lv)
                eff = 1.30 if (a.us and y == 2025 and p >= d('2025-10-01')) else 1.0
                n = rng.poisson(vol * (1.1 if y == 2025 else 1.0)); ga = rng.binomial(n, min(0.5, base * wx * eff * (1.15 if y == 2025 else 1)))
                pairs = int(0.7 * n); rows.append(dict(date=date, apt=a.icao, n=n, ga=ga, pairs=pairs, tight=rng.binomial(pairs, 0.08), ra=rng.poisson(0.002 * n), ra_nococ=0, lowvis_share=lv, gust25=0.0, ts=0.0,
                                                       year=y, pdate=p, grp=a.grp, us=a.us))
    t = pd.DataFrame(rows); wx = t[['apt', 'date'] + WX]; t = t.drop(columns=WX); t, exc, _ = apply_rules23(t)
    W = wx_adjusted(in_window(t, 'shutdown'), wx, np.random.default_rng(3), nboot=200)
    print('selftest weather-adjusted RRR (planted 1.30):', round(W['adjusted']['rrr'], 3), W['adjusted']['ci_day'], 'low-vis rate ratio (planted 4.48):', round(W['covariate_rate_ratios']['lowvis_share'], 2))
    assert 1.15 < W['adjusted']['rrr'] < 1.45
    R = run(t, t, t, np.random.default_rng(2), nboot=200)
    print('selftest primary RRR (planted 1.30):', round(R['primary']['rrr'], 3), R['primary']['ci_day'], R['primary']['verdict'])
    print('selftest placebo RRR (planted 1.00):', round(R['placebo_september']['rrr'], 3), R['placebo_september']['ci_day'])
    print('selftest spacing RRR (planted 1.00):', round(R['spacing_shutdown']['rrr'], 3), ' RA ratio (planted 1.00):', round(R['ra_main']['ratio'], 3))
    assert 1.15 < R['primary']['rrr'] < 1.45 and 0.85 < R['placebo_september']['rrr'] < 1.18

if __name__ == '__main__':
    if '--selftest' in sys.argv: selftest(); sys.exit(0)
    work, out = sys.argv[1], sys.argv[2]; os.makedirs(out, exist_ok=True)
    rng = np.random.default_rng(SEED)
    a = load_attempts(work); ra = ra_events(work)
    a1, info = apply_rule1(a)
    t, excluded, cov = apply_rules23(airport_day(a1, ra))
    t_air = airport_day(a1, ra, air_only=True); t_air = t_air[t_air.apt.isin(t.apt.unique()) & (t_air.n >= 30)]
    t_no1 = airport_day(a, ra); t_no1 = t_no1[t_no1.apt.isin(t.apt.unique()) & (t_no1.n >= 30)]
    t.to_csv(os.path.join(out, 'airport_day.csv'), index=False); weekly(t).to_csv(os.path.join(out, 'weekly.csv'), index=False)
    R = run(t, t_air, t_no1, rng)
    wxf = os.path.join(HERE, '..', 'data', 'weather_airport_day.csv')
    if os.path.exists(wxf):
        wx = pd.read_csv(wxf); wx['date'] = [d(z) for z in wx.date]
        R['weather_adjusted'] = wx_adjusted(in_window(t, 'shutdown'), wx, np.random.default_rng(SEED + 1))
    R['meta'] = dict(days_2024=int(a[[x.year == 2024 for x in a.date]].date.nunique()), days_2025=int(a[[x.year == 2025 for x in a.date]].date.nunique()),
                     attempts_total=int(len(a)), rule1=info, excluded_airports=excluded, airports_kept=int(t.apt.nunique()),
                     airports_kept_by_group=t.groupby('grp').apt.nunique().to_dict(), nboot=NBOOT, seed=SEED)
    json.dump(R, open(os.path.join(out, 'results.json'), 'w'), indent=1, default=float)
    print(json.dumps({k: R[k] for k in ('meta',)}, indent=1, default=float)); print('primary', R['primary']['rrr'], R['primary']['ci_day'], R['primary']['ci_airport'], R['primary']['verdict'])
