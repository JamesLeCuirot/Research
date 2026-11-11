"""Post hoc analyses prompted by independent review. Not pre-registered.
Uses the modal setting in the 120 s window (posthoc_modal_extract.py) and voids landings whose broadcast value was unstable.
Usage: python3 posthoc_after_review.py out.json airports.csv modal_landings*.parquet"""
import sys, json, numpy as np, pandas as pd
sys.path.insert(0, __file__.rsplit('/', 1)[0])
import qnh_analysis as Q
out, airports_csv, files = sys.argv[1], sys.argv[2], sys.argv[3:]
a = Q.load(files, airports_csv)
a['unstable'] = a.n_distinct >= 3                      # three or more different values in the last two minutes
a.loc[a.unstable, 'own'] = np.nan; a['has'] = a.own.notna(); a['plaus'] = a.own.between(Q.LO, Q.HI)
a = Q.classify(Q.reference(a)); a['region'] = np.where(a.eu == 1, 'EU', 'US')
v = a[a.valid].copy(); S = ['apt', 'date']; res = {}
v['dd'] = v.d.abs().round(1)
for n, th in (('y', 2.0), ('y3', 3.0), ('y5', 5.0), ('y10', 10.0)): v[n] = (v.dd >= th).astype(int)
v['small'] = ((v.dd >= 2.0) & (v.dd < 5.0)).astype(int)
r = lambda x: {k: (round(z, 4) if isinstance(z, float) else z) for k, z in x.items()}
res['counts'] = dict(valid=int(len(v)), unstable_voided=a.groupby('cls').unstable.sum().astype(int).to_dict(), modal_differs_from_last=int((a.own_last.notna() & a.own.notna() & (a.own != a.own_last)).sum()))
res['rates_per1000'] = {f'{c}|{g}': {n: [int(len(x)), int(x[n].sum()), round(1000 * float(x[n].mean()), 3)] for n in ('y', 'y5', 'y10')} for (c, g), x in v.groupby(['cls', 'region'])}
res['rates_region'] = {g: {n: Q.rate_ci(x, n) for n in ('y', 'y5', 'y10')} for g, x in v.groupby('region')}
res['rates_all'] = {n: Q.rate_ci(v, n) for n in ('y', 'y5', 'y10')}
res['H1'] = {n: r(Q.cmh(v, n, S)) for n in ('y', 'small', 'y5', 'y10')}
res['H1']['boot_y'] = Q.boot_or(v, 'y', S); res['H1']['boot_y5'] = Q.boot_or(v, 'y5', S)
q = v[(v.cons > 0.95) & (v.nref >= 10)]; res['H1_strict_reference'] = {n: r(Q.cmh(q, n, S)) for n in ('y', 'y5')}
nl = v.groupby('icao').y.transform('size')
for k in (4, 10, 20): res[f'H1_aircraft_{k}plus'] = {n: r(Q.cmh(v[nl >= k], n, S)) for n in ('y', 'y5')}
res['rates_by_landings_per_aircraft'] = {f'{c}|{b}': [int(len(x)), int(x.y.sum()), round(1000 * float(x.y.mean()), 2)] for (c, b), x in v.assign(b=pd.cut(nl, [0, 1, 3, 9, 19, 1e9], labels=['1', '2-3', '4-9', '10-19', '20+'])).groupby(['cls', 'b'], observed=True)}
rng = np.random.default_rng(5); one = []
for _ in range(30):
    s = v.iloc[rng.permutation(len(v))].drop_duplicates('icao'); one.append(Q.cmh(s, 'y', ['apt'])['or_mh'])
res['H1_one_landing_per_aircraft'] = [float(np.nanmin(one)), float(np.nanmedian(one)), float(np.nanmax(one))]
ref_air = v[v.biz == 0].groupby('apt').size(); share = v.groupby('apt').biz.mean()
v['bshare'] = pd.cut(v.apt.map(share), [-1, .05, .2, .6, 1], labels=['under 5%', '5-20%', '20-60%', 'over 60%'])
res['rates_by_airport_biz_share'] = {f'{c}|{b}': [int(len(x)), int(x.y.sum()), round(1000 * float(x.y.mean()), 2)] for (c, b), x in v.groupby(['cls', 'bshare'], observed=True)}
# standard left set, strict: at least 5 hPa from reference
v['std5'] = (((v.own - Q.STD).abs() <= 0.5) & (v.dd >= 5.0)).astype(int); e = v[(v.ref - Q.STD).abs() >= 5.0]
res['std_left_5hPa'] = {f'{c}|{g}': [int(len(x)), int(x.std5.sum()), round(1000 * float(x.std5.mean()), 3)] for (c, g), x in e.groupby(['cls', 'region'])}
res['std_left_5hPa_biz_vs_air'] = r(Q.cmh(e, 'std5', S)); res['std_left_5hPa_europe_vs_us'] = r(Q.region_test(e, 'std5', reps=5000))
res['std5_share_of_errors'] = {c: dict(err2=int(x.y.sum()), err5=int(x.y5.sum()), std5=int(x.std5.sum())) for c, x in v.groupby('cls')}
e3 = a[a.std_elig].copy(); e3['y'] = e3.std_left.astype(int); res['H2_modal_stable'] = r(Q.region_test(e3, 'y'))
res['H2_modal_stable_by_class'] = {c: r(Q.region_test(x, 'y', reps=2000)) for c, x in e3.groupby('cls')}
# flat pressure, minute of hour, held time
v['minute'] = (v.t_end % 3600 // 600).astype(int)
res['small_errors_by_10min_of_hour_US'] = {c: x[x.small == 1].groupby('minute').size().to_dict() for c, x in v[v.eu == 0].groupby('cls')}
res['held_5min_share_of_errors'] = {f'{c}|{g}': round(float((x.held_s >= 300).mean()), 3) for (c, g), x in v[v.y == 1].groupby(['cls', 'region'])}
res['direction'] = {c: dict(too_high=int(((x.d > 0) & (x.y == 1)).sum()), too_low=int(((x.d < 0) & (x.y == 1)).sum()), too_high_5=int(((x.d > 0) & (x.y5 == 1)).sum()), too_low_5=int(((x.d < 0) & (x.y5 == 1)).sum())) for c, x in v.groupby('cls')}
t = v[v.biz == 1].groupby('actype').agg(n=('y', 'size'), e2=('y', 'sum'), e5=('y5', 'sum'), std5=('std5', 'sum')); t = t[t.n >= 1000]
res['biz_types'] = {k: [int(x.n), int(x.e2), int(x.e5), int(x.std5)] for k, x in t.iterrows()}
t = v[v.biz == 0].groupby('actype').agg(n=('y', 'size'), e2=('y', 'sum'), e5=('y5', 'sum')); t = t[t.n >= 5000]
res['air_types'] = {k: [int(x.n), int(x.e2), int(x.e5)] for k, x in t.iterrows()}
v['cs3'] = np.where(v.callsign.str.match(r'^[A-Z]{3}[0-9]'), v.callsign.str[:3], 'registration')
o = v.groupby(['cls', 'cs3']).y.agg(['size', 'sum']); o = o[o['size'] >= 1500]; o['r'] = 1000 * o['sum'] / o['size']
res['operator_spread_per1000'] = {c: dict(n_operators=int(len(x)), min=round(float(x.r.min()), 2), median=round(float(x.r.median()), 2), max=round(float(x.r.max()), 2)) for c, x in o.groupby(level=0)}
x10 = v[v.y10 == 1]; res['ten_hPa'] = {c: dict(events=int(len(g)), aircraft=int(g.icao.nunique()), from_aircraft_under_10_landings=int((nl[g.index] < 10).sum())) for c, g in x10.groupby('cls')}
json.dump(res, open(out, 'w'), indent=1, default=str)
for k, z in res.items(): print(k, json.dumps(z, default=str)[:650])
