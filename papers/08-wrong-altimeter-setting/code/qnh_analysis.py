"""Stage B: reference setting, error classification and confirmatory tests. Frozen with the preregistration.
Usage: python3 qnh_analysis.py out.json airports.csv landings1.parquet [landings2.parquet ...] [--permute SEED]"""
import sys, json, re, numpy as np, pandas as pd
from scipy import stats
AIRLINE_CS = re.compile(r'^[A-Z]{3}[0-9]')
LO, HI = 940.0, 1060.0            # plausible range for a broadcast setting, hPa
WIN = 1800.0                      # reference window, seconds either side
MIN_OTHERS = 5                    # other aircraft needed for a reference
CONSENSUS = 0.6                   # share of them within 1.0 hPa of their median
E2, E5, E10 = 2.0, 5.0, 10.0      # error thresholds, hPa
STD = 1013.25

def load(files, airports_csv):
    a = pd.concat([pd.read_parquet(f) for f in files], ignore_index=True)
    a['callsign'] = a.callsign.fillna('')
    a = a[(a.cls == 'biz') | a.callsign.str.match(AIRLINE_CS)].copy()
    a = a.drop_duplicates(['icao', 't_end']).reset_index(drop=True)
    a['biz'] = (a.cls == 'biz').astype(int)
    a['date'] = pd.to_datetime(a.t_end, unit='s').dt.strftime('%Y-%m-%d'); a['hour'] = pd.to_datetime(a.t_end, unit='s').dt.hour
    a['eu'] = (~a.apt.str.startswith('K')).astype(int)
    ap = pd.read_csv(airports_csv, usecols=['ident', 'elevation_ft', 'longitude_deg']).rename(columns={'ident': 'apt'})
    a = a.merge(ap, on='apt', how='left')
    a['has'] = a.own.notna(); a['plaus'] = a.own.between(LO, HI)
    return a

def reference(a):
    """Reference = median setting of OTHER aircraft landing at the same airport within 30 minutes either side."""
    ref = np.full(len(a), np.nan); nref = np.zeros(len(a), int); cons = np.full(len(a), np.nan)
    ok = a.plaus.values
    for apt, g in a[ok].groupby('apt'):
        g = g.sort_values('t_end'); t = g.t_end.values; v = g.own.values; ic = g.icao.values; idx = g.index.values
        lo = np.searchsorted(t, t - WIN, 'left'); hi = np.searchsorted(t, t + WIN, 'right')
        for k in range(len(g)):
            s = slice(lo[k], hi[k]); m = ic[s] != ic[k]
            if m.sum() < MIN_OTHERS or len(set(ic[s][m])) < MIN_OTHERS: continue
            w = v[s][m]; med = np.median(w)
            ref[idx[k]] = med; nref[idx[k]] = m.sum(); cons[idx[k]] = (np.abs(w - med) <= 1.0).mean()
    a['ref'] = ref; a['nref'] = nref; a['cons'] = cons
    return a

def classify(a):
    a['hasref'] = a.ref.notna() & (a.cons >= CONSENSUS)
    a['d'] = a.own - a.ref
    # QFE-like: setting matches station pressure at an airport at least 300 ft above sea level
    qfe = a.ref * (1 - 0.0065 * (a.elevation_ft * 0.3048) / 288.15) ** 5.2559
    a['qfe_like'] = a.hasref & (a.elevation_ft >= 300) & ((a.own - qfe).abs() <= 1.5) & (a.d.abs() >= E2)
    base = a.plaus & a.hasref & ~a.qfe_like
    # suspect avionics, judged without regard to class: an aircraft wrong on at least half of four or more landings
    b = a[base].assign(e=lambda x: x.d.abs() >= E2).groupby('icao').e.agg(['size', 'mean'])
    sus = set(b[(b['size'] >= 4) & (b['mean'] >= 0.5)].index)
    a['suspect'] = a.icao.isin(sus)
    a['valid'] = base & ~a.suspect
    for name, th in (('err2', E2), ('err5', E5), ('err10', E10)):
        a[name] = (a.d.abs() >= th).where(a.valid)
    a['std_left'] = ((a.own - STD).abs() <= 0.5) & (a.d.abs() >= E2)
    a['std_elig'] = a.valid & ((a.ref - STD).abs() >= 3.0)
    return a

def cmh(df, y, strata):
    t = df.groupby(strata + ['biz', y]).size().unstack(['biz', y], fill_value=0)
    for k in [(1, 1), (1, 0), (0, 1), (0, 0)]:
        if k not in t.columns: t[k] = 0
    A = t[(1, 1)].values.astype(float); B = t[(1, 0)].values.astype(float); C = t[(0, 1)].values.astype(float); D = t[(0, 0)].values.astype(float)
    N = A + B + C + D; inf = ((A + B) > 0) & ((C + D) > 0) & ((A + C) > 0) & ((B + D) > 0)
    A, B, C, D, N = A[inf], B[inf], C[inf], D[inf], N[inf]
    res = dict(n_strata=int(inf.sum()), n_biz=int((A + B).sum()), n_air=int((C + D).sum()), ev_biz=int(A.sum()), ev_air=int(C.sum()))
    if inf.sum() == 0 or (A * D / N).sum() == 0 or (B * C / N).sum() == 0:
        res.update(or_mh=np.nan, lo=np.nan, hi=np.nan, p=np.nan); return res
    R = A * D / N; S = B * C / N; P = (A + D) / N; Q = (B + C) / N
    orr = R.sum() / S.sum()
    var = (P * R).sum() / (2 * R.sum() ** 2) + (P * S + Q * R).sum() / (2 * R.sum() * S.sum()) + (Q * S).sum() / (2 * S.sum() ** 2)
    EA = (A + B) * (A + C) / N; VA = np.where(N > 1, (A + B) * (C + D) * (A + C) * (B + D) / (N ** 2 * np.maximum(N - 1, 1)), 0)
    chi = (A.sum() - EA.sum()) ** 2 / VA.sum(); p = stats.chi2.sf(chi, 1)
    res.update(or_mh=float(orr), lo=float(np.exp(np.log(orr) - 1.96 * np.sqrt(var))), hi=float(np.exp(np.log(orr) + 1.96 * np.sqrt(var))), p=float(p))
    return res

def boot_or(df, y, strata, reps=2000, seed=1):
    """Percentile interval for the MH odds ratio, resampling whole airports."""
    rng = np.random.default_rng(seed)
    t = df.groupby(strata + ['biz', y]).size().unstack(['biz', y], fill_value=0)
    for k in [(1, 1), (1, 0), (0, 1), (0, 0)]:
        if k not in t.columns: t[k] = 0
    A, B, C, D = [t[k].values.astype(float) for k in [(1, 1), (1, 0), (0, 1), (0, 0)]]; N = A + B + C + D
    apt = np.asarray(t.index.get_level_values('apt'))
    R = pd.Series(A * D / N).groupby(apt).sum().values; S = pd.Series(B * C / N).groupby(apt).sum().values
    o = []
    for _ in range(reps):
        ix = rng.integers(0, len(R), len(R)); s = S[ix].sum()
        if s > 0: o.append(R[ix].sum() / s)
    return [float(np.percentile(o, 2.5)), float(np.percentile(o, 97.5))] if o else [float('nan'), float('nan')]

def rate_ci(df, y, reps=2000, seed=1):
    """Rate per 1,000 landings with a percentile interval resampling airport-days."""
    g = df.assign(cl=df.apt + '|' + df.date).groupby('cl')[y].agg(['sum', 'size'])
    s = g['sum'].values.astype(float); n = g['size'].values.astype(float); rng = np.random.default_rng(seed); o = []
    for _ in range(reps):
        ix = rng.integers(0, len(s), len(s)); o.append(s[ix].sum() / n[ix].sum())
    return dict(events=int(s.sum()), n=int(n.sum()), per1000=float(1000 * s.sum() / n.sum()), lo=float(1000 * np.percentile(o, 2.5)), hi=float(1000 * np.percentile(o, 97.5)))

def region_test(df, y, reps=10000, seed=1):
    """Europe vs US rate ratio. p from permuting the region label across airports; interval from resampling airports within region."""
    g = df.groupby(['apt', 'eu'])[y].agg(['sum', 'size']).reset_index()
    s = g['sum'].values.astype(float); n = g['size'].values.astype(float); eu = g.eu.values.astype(bool)
    def rr(e): 
        a1 = s[e].sum() / n[e].sum(); a0 = s[~e].sum() / n[~e].sum(); return a1 / a0 if a0 > 0 else np.nan
    obs = rr(eu); rng = np.random.default_rng(seed)
    perm = np.array([rr(rng.permutation(eu)) for _ in range(reps)]); perm = perm[np.isfinite(perm) & (perm > 0)]
    p = float((np.abs(np.log(perm)) >= abs(np.log(obs))).mean()) if obs > 0 and np.isfinite(obs) else np.nan
    i1 = np.where(eu)[0]; i0 = np.where(~eu)[0]; o = []
    for _ in range(2000):
        b1 = rng.choice(i1, len(i1)); b0 = rng.choice(i0, len(i0)); d0 = s[b0].sum() / n[b0].sum()
        if d0 > 0: o.append((s[b1].sum() / n[b1].sum()) / d0)
    return dict(rate_eu_per1000=float(1000 * s[eu].sum() / n[eu].sum()), rate_us_per1000=float(1000 * s[~eu].sum() / n[~eu].sum()), ev_eu=int(s[eu].sum()), ev_us=int(s[~eu].sum()),
                n_eu=int(n[eu].sum()), n_us=int(n[~eu].sum()), rr=float(obs), lo=float(np.percentile(o, 2.5)) if o else float('nan'), hi=float(np.percentile(o, 97.5)) if o else float('nan'), p=p, airports_eu=int(eu.sum()), airports_us=int((~eu).sum()))

def prepare(files, airports_csv, permute=None):
    a = load(files, airports_csv)
    if permute is not None:
        rng = np.random.default_rng(permute); a['biz'] = rng.permutation(a.biz.values); a['cls'] = np.where(a.biz == 1, 'biz', 'air')
        m = a.groupby('apt').eu.first(); m[:] = rng.permutation(m.values); a['eu'] = a.apt.map(m)
    return classify(reference(a))

if __name__ == '__main__':
    args = sys.argv[1:]; permute = None
    if '--permute' in args:
        i = args.index('--permute'); permute = int(args[i + 1]); args = args[:i] + args[i + 2:]
    out, airports_csv, files = args[0], args[1], args[2:]
    a = prepare(files, airports_csv, permute)
    v = a[a.valid].copy(); v['y'] = v.err2.astype(int)
    res = {}
    h1 = cmh(v, 'y', ['apt', 'date']); h1['boot_ci_airports'] = boot_or(v, 'y', ['apt', 'date'])
    h1['crude_per1000'] = (1000 * v.groupby('cls').y.mean()).to_dict()
    res['H1_err2_biz_vs_airline'] = h1
    e = a[a.std_elig].copy(); e['y'] = e.std_left.astype(int)
    res['H2_std_left_europe_vs_us'] = region_test(e, 'y')
    ps = [res['H1_err2_biz_vs_airline']['p'], res['H2_std_left_europe_vs_us']['p']]
    order = np.argsort(ps); adj = [None, None]; prev = 0.0
    for r, i in enumerate(order):
        prev = max(prev, min(1.0, ps[i] * (2 - r))); adj[i] = prev
    res['H1_err2_biz_vs_airline']['p_holm'] = adj[0]; res['H2_std_left_europe_vs_us']['p_holm'] = adj[1]
    res['prevalence'] = {n: rate_ci(v.assign(y=v[n].astype(int)), 'y') for n in ('err2', 'err5', 'err10')}
    res['_counts'] = dict(landings=int(len(a)), broadcast=int(a.has.sum()), plausible=int(a.plaus.sum()), with_reference=int((a.plaus & a.hasref).sum()), qfe_like=int(a.qfe_like.sum()),
                          suspect_aircraft=int(a[a.suspect].icao.nunique()), suspect_landings=int(a.suspect.sum()), valid=int(a.valid.sum()), airports=int(a.apt.nunique()), permuted=permute is not None)
    json.dump(res, open(out, 'w'), indent=1)
    print(json.dumps(res, indent=1))
