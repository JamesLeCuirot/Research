"""Preregistered sensitivity and exploratory analyses (preregistration section 6). Frozen with the preregistration.
Usage: python3 qnh_secondary.py out.json airports.csv landings*.parquet [--permute SEED]"""
import sys, json, numpy as np, pandas as pd
sys.path.insert(0, __file__.rsplit('/', 1)[0])
import qnh_analysis as Q
LIGHT = set("C25A C25B C25C C25M C500 C501 C510 C525 C550 C551 C55B C560 C56X E50P E55P HDJT SF50 PC24 LJ31 LJ35 LJ40 LJ45 LJ55 LJ60 LJ70 LJ75 BE40 PRM1 EA50 H25B H25C FA10 ASTR G150".split())
S = ['apt', 'date']
def rate(df, col='y'):
    return {k: [int(len(g)), int(g[col].sum()), round(1000 * float(g[col].mean()), 3)] for k, g in df.groupby('cls')}
def hourly_change(v):
    r = v[['apt', 't_end', 'ref']].rename(columns={'t_end': 't0', 'ref': 'ref0'}).sort_values('t0')
    x = pd.merge_asof(v.sort_values('t_end').assign(tm=lambda d: d.t_end - 3600), r, left_on='tm', right_on='t0', by='apt', direction='nearest', tolerance=900)
    x['dp'] = x.ref - x.ref0; return x
if __name__ == '__main__':
    args = sys.argv[1:]; permute = None
    if '--permute' in args:
        i = args.index('--permute'); permute = int(args[i + 1]); args = args[:i] + args[i + 2:]
    out, airports_csv, files = args[0], args[1], args[2:]
    a = Q.prepare(files, airports_csv, permute); res = {'permuted': permute is not None}
    a['region'] = np.where(a.eu == 1, 'EU', 'US')
    # coverage and exclusions
    res['coverage'] = {f'{c}|{r}': dict(landings=int(len(g)), broadcast=round(float(g.has.mean()), 4), with_reference=round(float((g.plaus & g.hasref).mean()), 4), valid=round(float(g.valid.mean()), 4),
                                         qfe_like=int(g.qfe_like.sum()), suspect=int(g.suspect.sum()), implausible=int((g.has & ~g.plaus).sum())) for (c, r), g in a.groupby(['cls', 'region'])}
    v = a[a.valid].copy(); v['y'] = v.err2.astype(int)
    v['y3'] = (v.d.abs() >= 3.0).astype(int); v['y5'] = v.err5.astype(int); v['y10'] = v.err10.astype(int)
    res['crude'] = {n: rate(v, n) for n in ('y', 'y3', 'y5', 'y10')}
    res['crude_by_region'] = {r: {n: rate(g, n) for n in ('y', 'y3', 'y5', 'y10')} for r, g in v.groupby('region')}
    # sensitivity for H1
    sens = {}
    for n in ('y3', 'y5', 'y10'): sens[f'S1_threshold_{n}'] = Q.cmh(v, n, S)
    x = hourly_change(v); x['fast'] = x.dp.abs() >= 1.5
    sens['S2_excluding_fast_pressure_change'] = Q.cmh(x[~x.fast], 'y', S); sens['S2_share_fast'] = float(x.fast.mean())
    old = Q.WIN; Q.WIN = 900.0; b = Q.prepare(files, airports_csv, permute); Q.WIN = old
    vb = b[b.valid].copy(); vb['y'] = vb.err2.astype(int); sens['S3_reference_window_15min'] = Q.cmh(vb, 'y', S); sens['S3_valid'] = int(len(vb)); sens['S3_crude'] = rate(vb)
    w = a[a.plaus & a.hasref & ~a.qfe_like].copy(); w['y'] = (w.d.abs() >= Q.E2).astype(int); sens['S4_including_suspect_aircraft'] = Q.cmh(w, 'y', S)
    n_ac = v.groupby('icao').y.transform('size'); sens['S5_aircraft_with_3plus_landings'] = Q.cmh(v[n_ac >= 3], 'y', S)
    sens['S6_US'] = Q.cmh(v[v.eu == 0], 'y', S); sens['S6_Europe'] = Q.cmh(v[v.eu == 1], 'y', S)
    sens['S7_airport_date_hour'] = Q.cmh(v, 'y', S + ['hour']); sens['S8_confirmed_landings'] = Q.cmh(v[v.confirmed == True], 'y', S)
    sens['S9_airport_only'] = Q.cmh(v, 'y', ['apt'])
    loo = [Q.cmh(v[v.apt != ap], 'y', S)['or_mh'] for ap in v.apt.unique()]; sens['S10_leave_one_airport_out'] = [float(np.nanmin(loo)), float(np.nanmax(loo))]
    e = a[a.std_elig].copy(); e['y'] = e.std_left.astype(int)
    sens['H2_by_class'] = {c: Q.region_test(g, 'y', reps=2000) for c, g in e.groupby('cls')}
    e4 = a[a.valid & ((a.ref - Q.STD).abs() >= 5.0)].copy(); e4['y'] = e4.std_left.astype(int); sens['H2_ref_5hPa_from_standard'] = Q.region_test(e4, 'y', reps=2000)
    res['sensitivity'] = sens
    # exploratory
    ex = {}
    er = v[v.y == 1]
    ex['direction'] = {f'{c}|{r}': dict(set_too_high=int((g.d > 0).sum()), set_too_low=int((g.d < 0).sum())) for (c, r), g in er.groupby(['cls', 'region'])}
    bins = [-1e9, -30, -15, -9, -5.5, -3.6, -2.8, -1.99, 1.99, 2.8, 3.6, 5.5, 9, 15, 30, 1e9]
    ex['error_size_histogram'] = {r: pd.cut(g.d, bins).value_counts().sort_index().rename(str).to_dict() for r, g in v.groupby('region')}
    ex['ten_hPa_slips'] = {r: int(((g.d.abs() >= 9.2) & (g.d.abs() <= 10.8)).sum()) for r, g in v.groupby('region')}
    ex['inch_slips_33_35hPa'] = {r: int(((g.d.abs() >= 33) & (g.d.abs() <= 35)).sum()) for r, g in v.groupby('region')}
    ex['std_left'] = {f'{c}|{r}': [int(len(g)), int(g.std_left.sum())] for (c, r), g in e.groupby(['cls', 'region'])}
    ex['std_left_share_of_err2'] = {r: [int(g.y.sum()), int((g.std_left & (g.y == 1)).sum())] for r, g in v.groupby('region')}
    ex['std_left_biz_vs_air'] = Q.cmh(e, 'y', S)
    v['lst'] = (v.hour + v.longitude_deg / 15.0) % 24; v['night'] = (v.lst < 6) | (v.lst >= 21)
    ex['day'] = Q.cmh(v[~v.night], 'y', S); ex['night'] = Q.cmh(v[v.night], 'y', S); ex['rate_day_night'] = {str(k): [int(len(g)), int(g.y.sum())] for k, g in v.groupby('night')}
    v['pband'] = pd.cut((v.ref - Q.STD).abs(), [-1, 5, 15, 1e9], labels=['within 5', '5 to 15', 'over 15'])
    ex['by_pressure_band'] = {f'{c}|{p}': [int(len(g)), int(g.y.sum()), int(g.y10.sum())] for (c, p), g in v.groupby(['cls', 'pband'], observed=True)}
    ex['by_pressure_change'] = {f'{c}|{f}': [int(len(g)), int(g.y.sum())] for (c, f), g in x.groupby(['cls', 'fast'])}
    v['wrong5'] = (v.own5 - v.ref).abs() >= Q.E2
    k = v[v.own5.notna()]
    ex['five_minutes_before'] = {c: dict(n=int(len(g)), wrong_then=int(g.wrong5.sum()), corrected_by_landing=int((g.wrong5 & (g.y == 0)).sum()), wrong_both=int((g.wrong5 & (g.y == 1)).sum()), wrong_only_at_landing=int((~g.wrong5 & (g.y == 1)).sum())) for c, g in k.groupby('cls')}
    v['private_cs'] = ((v.callsign == v.reg) | v.callsign.str.match(r'^N[0-9]')) & (v.callsign != ''); v['light'] = v.actype.isin(LIGHT)
    bz = v[v.biz == 1]
    ex['within_biz'] = {f"{'registration' if p else 'company'}|{'light' if l else 'large'}": [int(len(g)), int(g.y.sum()), int(g.y5.sum())] for (p, l), g in bz.groupby(['private_cs', 'light'])}
    ex['large_company_biz_vs_air'] = Q.cmh(v[(v.biz == 0) | (~v.private_cs & ~v.light)], 'y', S)
    t = v.groupby(['cls', 'actype']).y.agg(['size', 'sum']); t = t[t['size'] >= 3000]
    ex['by_type'] = {f'{c}|{ty}': [int(r['size']), int(r['sum'])] for (c, ty), r in t.iterrows()}
    pa = v.groupby(['apt', 'cls']).y.agg(['size', 'sum']).unstack(fill_value=0)
    ex['per_airport'] = {ap: [int(r[('size', 'air')]), int(r[('sum', 'air')]), int(r[('size', 'biz')]), int(r[('sum', 'biz')])] for ap, r in pa.iterrows()}
    ex['paris'] = {ap: {n: [int(len(g)), int(g[n].sum())] for n in ('y', 'y5', 'y10')} for ap, g in v[v.apt.isin(['LFPB', 'LFPG', 'LFPO'])].groupby('apt')}
    ex['europe_over_5hPa'] = Q.rate_ci(v[v.eu == 1].assign(z=lambda d: (d.d.abs() > 5.0).astype(int)), 'z')
    ex['prevalence_by_region'] = {r: {n: Q.rate_ci(g, n) for n in ('y', 'y5', 'y10')} for r, g in v.groupby('region')}
    ex['aircraft'] = v.groupby('cls').icao.nunique().to_dict(); ex['days'] = sorted(v.date.unique().tolist())
    res['exploratory'] = ex
    json.dump(res, open(out, 'w'), indent=1, default=str); print('ok', len(a), len(v))
