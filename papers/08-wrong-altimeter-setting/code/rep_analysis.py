"""Replication analysis on a fresh sample, using the corrected measure. Frozen with PREREGISTRATION_REPLICATION.md.
Input landings come from qnh_extract.py followed by posthoc_modal_extract.py (setting = modal value in the last 120 s).
Usage: python3 rep_analysis.py out.json airports.csv [--metar us.csv eu.csv] [--permute SEED] landings*.parquet"""
import sys, json, numpy as np, pandas as pd
sys.path.insert(0, __file__.rsplit('/', 1)[0])
import qnh_analysis as Q
S = ['apt', 'date']

def prepare(files, airports_csv, permute=None):
    a = Q.load(files, airports_csv)
    if permute is not None:
        rng = np.random.default_rng(permute); a['biz'] = rng.permutation(a.biz.values); a['cls'] = np.where(a.biz == 1, 'biz', 'air')
        m = a.groupby('apt').eu.first(); m[:] = rng.permutation(m.values); a['eu'] = a.apt.map(m)
    a['unstable'] = a.n_distinct >= 3
    a.loc[a.unstable, 'own'] = np.nan; a['has'] = a.own.notna(); a['plaus'] = a.own.between(Q.LO, Q.HI)
    a = Q.classify(Q.reference(a)); a['region'] = np.where(a.eu == 1, 'EU', 'US')
    a['dd'] = a.d.abs().round(1)
    for n, th in (('y', 2.0), ('y5', 5.0), ('y10', 10.0)): a[n] = (a.dd >= th).astype(int)
    a['std5'] = (((a.own - Q.STD).abs() <= 0.5) & (a.dd >= 5.0)).astype(int)
    a['std5_elig'] = a.valid & ((a.ref - Q.STD).abs() >= 5.0)
    a['n_ac'] = a[a.valid].groupby('icao').y.transform('size').reindex(a.index)
    return a

def holm(ps):
    order = np.argsort(ps); adj = [None] * len(ps); prev = 0.0
    for r, i in enumerate(order):
        prev = max(prev, min(1.0, ps[i] * (len(ps) - r))); adj[i] = prev
    return adj

def metar_join(a, files):
    m = pd.concat([pd.read_csv(f) for f in files], ignore_index=True)
    m = m[pd.to_numeric(m.alti, errors='coerce').notna()].copy(); m['alti'] = m.alti.astype(float)
    m['apt'] = np.where(m.station.str.len() == 3, 'K' + m.station, m.station)
    m['tm'] = (pd.to_datetime(m.valid, utc=True) - pd.Timestamp('1970-01-01', tz='UTC')).dt.total_seconds(); m['metar'] = m.alti * 33.8639
    m = m[['apt', 'tm', 'metar']].sort_values('tm')
    j = pd.merge_asof(a.sort_values('t_end'), m, left_on='t_end', right_on='tm', by='apt', direction='backward', tolerance=4200.0)
    return j

if __name__ == '__main__':
    args = sys.argv[1:]; permute = None; metar = None
    if '--permute' in args:
        i = args.index('--permute'); permute = int(args[i + 1]); args = args[:i] + args[i + 2:]
    if '--metar' in args:
        i = args.index('--metar'); metar = args[i + 1:i + 3]; args = args[:i] + args[i + 3:]
    out, airports_csv, files = args[0], args[1], args[2:]
    a = prepare(files, airports_csv, permute); v = a[a.valid].copy(); res = {}
    res['coverage'] = {f'{c}|{g}': dict(landings=int(len(x)), recorded=round(float(x.has.mean() + x.unstable.mean()), 4), unstable=int(x.unstable.sum()), analysed=round(float(x.valid.mean()), 4),
                                         qfe_like=int(x.qfe_like.sum()), suspect=int(x.suspect.sum())) for (c, g), x in a.groupby(['cls', 'region'])}
    tests = {}
    tests['R1_err2'] = Q.cmh(v, 'y', S); tests['R1_err2']['boot_ci_airports'] = Q.boot_or(v, 'y', S)
    tests['R2_err5'] = Q.cmh(v, 'y5', S); tests['R2_err5']['boot_ci_airports'] = Q.boot_or(v, 'y5', S)
    tests['R3_err2_aircraft_10plus'] = Q.cmh(v[v.n_ac >= 10], 'y', S)
    tests['R4_std_at_landing_5hPa'] = Q.cmh(a[a.std5_elig], 'std5', S)
    adj = holm([tests[k]['p'] if tests[k]['p'] == tests[k]['p'] else 1.0 for k in tests])
    for k, p in zip(tests, adj): tests[k]['p_holm'] = p
    res['tests'] = tests
    res['rates_all'] = {n: Q.rate_ci(v, n) for n in ('y', 'y5', 'y10')}
    res['rates_region'] = {g: {n: Q.rate_ci(x, n) for n in ('y', 'y5', 'y10')} for g, x in v.groupby('region')}
    res['rates_group'] = {f'{c}|{g}': {n: [int(len(x)), int(x[n].sum()), round(1000 * float(x[n].mean()), 3)] for n in ('y', 'y5', 'y10')} for (c, g), x in v.groupby(['cls', 'region'])}
    res['std5_group'] = {f'{c}|{g}': [int(len(x)), int(x.std5.sum())] for (c, g), x in a[a.std5_elig].groupby(['cls', 'region'])}
    res['us_vs_europe_err5'] = Q.region_test(v.assign(eu=1 - v.eu), 'y5', reps=5000)   # ratio is US over Europe
    v['small'] = ((v.dd >= 2.0) & (v.dd < 5.0)).astype(int)
    sens = dict(small_2_to_5=Q.cmh(v, 'small', S), err10=Q.cmh(v, 'y10', S), aircraft_4plus=Q.cmh(v[v.n_ac >= 4], 'y', S), aircraft_20plus=Q.cmh(v[v.n_ac >= 20], 'y', S),
                strict_reference=Q.cmh(v[(v.cons > 0.95) & (v.nref >= 10)], 'y', S), US=Q.cmh(v[v.eu == 0], 'y', S), Europe=Q.cmh(v[v.eu == 1], 'y', S), airport_date_hour=Q.cmh(v, 'y', S + ['hour']))
    res['sensitivity'] = sens
    res['rates_by_landings_per_aircraft'] = {f'{c}|{b}': [int(len(x)), int(x.y.sum())] for (c, b), x in v.assign(b=pd.cut(v.n_ac, [0, 1, 3, 9, 19, 1e9], labels=['1', '2-3', '4-9', '10-19', '20+'])).groupby(['cls', 'b'], observed=True)}
    res['counts'] = dict(landings=int(len(a)), valid=int(len(v)), aircraft=v.groupby('cls').icao.nunique().to_dict(), days=sorted(v.date.unique().tolist()), permuted=permute is not None)
    if metar:
        j = metar_join(a, metar); k = j[j.valid & j.metar.notna()].copy(); k['rm'] = k.ref - k.metar
        res['metar_validation'] = dict(valid_landings=int(j.valid.sum()), with_metar=int(len(k)), share_ref_within_1hPa=float((k.rm.abs() <= 1.0).mean()), share_ref_within_1p7hPa=float((k.rm.abs() <= 1.7).mean()),
                                       median_diff=float(k.rm.median()), p01_p99=[float(k.rm.quantile(.01)), float(k.rm.quantile(.99))],
                                       by_region={g: float((x.rm.abs() <= 1.0).mean()) for g, x in k.groupby('region')})
        w = j[j.plaus & j.metar.notna() & ~j.qfe_like & ~j.suspect].copy(); w['dm'] = (w.own - w.metar).abs().round(1)
        w['y'] = (w.dm >= 2.0).astype(int); w['y5'] = (w.dm >= 5.0).astype(int)
        res['metar_as_reference'] = dict(n=w.groupby('cls').size().to_dict(), err2=Q.cmh(w, 'y', S), err5=Q.cmh(w, 'y5', S),
                                         rates={f'{c}|{g}': [int(len(x)), int(x.y.sum()), int(x.y5.sum())] for (c, g), x in w.groupby(['cls', 'region'])})
    json.dump(res, open(out, 'w'), indent=1, default=str)
    print(json.dumps(res['tests'], indent=1, default=str)); print({k: res[k] for k in ('counts',) }['counts']['valid'], list(res.keys()))
