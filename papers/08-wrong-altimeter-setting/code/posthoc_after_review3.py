"""Post hoc analyses after the third independent review (v0.4). Not pre-registered.
Usage: python3 posthoc_after_review3.py out.json airports.csv us_metar.csv eu_metar.csv landings*.parquet"""
import sys, json, re, numpy as np, pandas as pd
sys.path.insert(0, __file__.rsplit('/', 1)[0])
import qnh_analysis as Q, rep_analysis as R
S = ['apt', 'date']

def or_only(df, y):
    r = Q.cmh(df, y, S); return r['or_mh']

def cluster_boot(df, y, unit, reps=1000, seed=1):
    """Percentile interval for the MH odds ratio, resampling whole clusters (unit) with replacement."""
    g = df.groupby(list(dict.fromkeys([unit] + S + ['biz'])))[y].agg(['sum', 'size']).reset_index()
    units = g[unit].unique(); idx = {u: i for i, u in enumerate(units)}; g['u'] = g[unit].map(idx)
    g['st'] = g.groupby(S).ngroup(); ns = g.st.max() + 1
    rng = np.random.default_rng(seed); out = []
    for _ in range(reps):
        w = np.bincount(rng.integers(0, len(units), len(units)), minlength=len(units))[g.u.values]
        def tot(mask, col): return np.bincount(g.st.values[mask], weights=(g[col].values * w)[mask], minlength=ns)
        b = (g.biz == 1).values
        a_ = tot(b, 'sum'); n1 = tot(b, 'size'); c_ = tot(~b, 'sum'); n0 = tot(~b, 'size'); N = n1 + n0; ok = N > 0
        num = (a_ * (n0 - c_))[ok] / N[ok]; den = (c_ * (n1 - a_))[ok] / N[ok]
        if den.sum() > 0: out.append(num.sum() / den.sum())
    return [float(np.percentile(out, 2.5)), float(np.percentile(out, 97.5))]

def clean_metar(files):
    m = pd.concat([pd.read_csv(f) for f in files], ignore_index=True)
    m = m[pd.to_numeric(m.alti, errors='coerce').notna()].copy(); m['hpa'] = m.alti.astype(float) * 33.8639
    m['t'] = pd.to_datetime(m.valid, utc=True); m = m.sort_values(['station', 't'])
    n0 = len(m); rng_bad = ~m.hpa.between(940, 1060); m = m[~rng_bad]
    g = m.groupby('station'); pv, nx = g.hpa.shift(1), g.hpa.shift(-1)
    pt = (m.t - g.t.shift(1)).dt.total_seconds() / 3600; nt = (g.t.shift(-1) - m.t).dt.total_seconds() / 3600
    spike = ((m.hpa - pv).abs() > 5) & (pt <= 3) & ((m.hpa - nx).abs() > 5) & (nt <= 3)
    edge = (((m.hpa - pv).abs() > 8) & (pt <= 1.5) & nx.isna()) | (((m.hpa - nx).abs() > 8) & (nt <= 1.5) & pv.isna())
    bad = spike | edge
    return m[~bad][['station', 'valid', 'alti']], dict(reports=int(n0), out_of_range=int(rng_bad.sum()), spikes=int(bad.sum()))

if __name__ == '__main__':
    out, airports_csv, mus, meu = sys.argv[1:5]; files = sys.argv[5:]
    a = R.prepare(files, airports_csv); res = {}
    a['ongrid'] = (((a.own - 800.0) / 0.8) - ((a.own - 800.0) / 0.8).round()).abs() < 0.02
    cs = a.callsign.fillna('').str.strip()
    a['oper'] = np.where(cs.str.match(r'^[A-Z]{3}\d'), cs.str[:3], 'AC_' + a.icao.astype(str))
    v = a[a.valid].copy()
    res['exclusions'] = dict(landings=int(len(a)), no_value=int((~a.has & ~a.unstable).sum()), unstable=int(a.unstable.sum()), implausible=int((a.has & ~a.plaus).sum()),
                             qfe_like=int(a.qfe_like.sum()), suspect_landings=int(a.suspect.sum()), suspect_aircraft=a[a.suspect].groupby('cls').icao.nunique().to_dict(), valid=int(len(v)))
    # 1. clustered intervals
    v10 = v[v.n_ac >= 10]
    res['cluster_ci'] = {k: dict(or_mh=or_only(d, y), operator=cluster_boot(d, y, 'oper'), airport=cluster_boot(d, y, 'apt'), aircraft=cluster_boot(d, y, 'icao'))
                         for k, d, y in (('R1', v, 'y'), ('R2', v, 'y5'), ('R3', v10, 'y'))}
    e = a[a.std5_elig]; res['cluster_ci']['R4'] = dict(or_mh=or_only(e, 'std5'), operator=cluster_boot(e, 'std5', 'oper'), airport=cluster_boot(e, 'std5', 'apt'))
    top = v[v.biz == 1].oper.value_counts(); res['biz_operator_share_top2'] = {k: round(float(n / (v.biz == 1).sum()), 3) for k, n in top.head(2).items()}
    # 2. source of the value (0.8 hPa grid = ADS-B broadcast; off-grid = 0.1 hPa source only)
    og = v[v.ongrid]; src = {}
    src['offgrid_landings'] = {f'{c}|{g}': [int((~x.ongrid).sum()), int(len(x))] for (c, g), x in v.groupby(['cls', 'region'])}
    src['offgrid_share_of_err5'] = {g: [int((x.y5 & ~x.ongrid).sum()), int(x.y5.sum())] for g, x in v.groupby('region')}
    src['rates_ongrid_region'] = {g: {n: [int(len(x)), int(x[n].sum()), round(1000 * float(x[n].mean()), 3)] for n in ('y', 'y5', 'y10')} for g, x in og.groupby('region')}
    src['rates_ongrid_group'] = {f'{c}|{g}': {n: [int(len(x)), int(x[n].sum()), round(1000 * float(x[n].mean()), 3)] for n in ('y', 'y5', 'y10')} for (c, g), x in og.groupby(['cls', 'region'])}
    src['rates_ongrid_all'] = {n: Q.rate_ci(og, n) for n in ('y', 'y5', 'y10')}
    src['tests_ongrid'] = dict(R1=Q.cmh(og, 'y', S), R2=Q.cmh(og, 'y5', S), R3=Q.cmh(og[og.n_ac >= 10], 'y', S), R4=Q.cmh(e[e.ongrid], 'std5', S), err10=Q.cmh(og, 'y10', S))
    src['std5_group_ongrid'] = {f'{c}|{g}': [int(len(x)), int(x.std5.sum())] for (c, g), x in e[e.ongrid].groupby(['cls', 'region'])}
    src['us_over_europe_err5_all'] = Q.region_test(v.assign(eu=1 - v.eu), 'y5', reps=5000)
    src['us_over_europe_err5_ongrid'] = Q.region_test(og.assign(eu=1 - og.eu), 'y5', reps=5000)
    src['note'] = 'region_test labels: rate_eu/ev_eu/n_eu hold the US values and vice versa because eu is flipped to make the ratio US over Europe'
    res['source'] = src
    # 3. weather reports, cleaned
    mc, minfo = clean_metar([mus, meu]); tmp = out + '.metar_clean.csv'; mc.to_csv(tmp, index=False)
    j = R.metar_join(a, [tmp]); res['metar_cleaning'] = minfo
    k = j[j.valid & j.metar.notna()].copy(); k['rm'] = (k.ref - k.metar).abs()
    res['metar_validation_clean'] = dict(n=int(len(k)), within_1=float((k.rm <= 1.0).mean()), within_1p7=float((k.rm <= 1.7).mean()),
                                         within_1_biz_heavy=float((k[k.groupby('apt').biz.transform('mean') > 0.6].rm <= 1.0).mean()),
                                         within_1_other=float((k[k.groupby('apt').biz.transform('mean') <= 0.6].rm <= 1.0).mean()))
    w = j[j.plaus & j.metar.notna() & ~j.qfe_like & ~j.suspect].copy(); w['dm'] = (w.own - w.metar).abs().round(1); mm = {}
    for nm, th in (('2.0', 2.0), ('2.4', 2.4), ('5.0', 5.0), ('10.0', 10.0)):
        w['yy'] = (w.dm >= th).astype(int); mm[nm] = Q.cmh(w, 'yy', S)
    w['yy'] = (w.dm >= 5.0).astype(int); mm['5.0_ongrid'] = Q.cmh(w[w.ongrid], 'yy', S)
    mm['n'] = w.groupby('cls').size().to_dict()
    w['hasref'] = w.valid; w['yy'] = (w.dm >= 2.4).astype(int)
    mm['rate_2.4_by_consensus_available'] = {f'{c}|{h}': [int(len(x)), int(x.yy.sum()), round(1000 * float(x.yy.mean()), 2)] for (c, h), x in w.groupby(['cls', 'hasref'])}
    res['metar_as_reference_clean'] = mm
    # 4. checks on statements in the paper
    b10 = v[(v.biz == 1) & (v.y10 == 1)]
    res['biz_err10'] = dict(n=int(len(b10)), aircraft_under_10_landings=int((b10.n_ac < 10).sum()), nonstandard_30plus=int(((b10.dd >= 30) & ((b10.own - Q.STD).abs() > 0.5)).sum()))
    a10 = v[(v.biz == 0) & (v.y10 == 1)]; res['air_err10_nonstandard_30plus'] = int(((a10.dd >= 30) & ((a10.own - Q.STD).abs() > 0.5)).sum())
    x = v[~((v.dd >= 30) & ((v.own - Q.STD).abs() > 0.5))]
    res['excluding_30plus_nonstandard'] = dict(R2=Q.cmh(x, 'y5', S), err10=Q.cmh(x, 'y10', S))
    b5 = v[(v.biz == 1) & (v.y5 == 1)]; res['biz_err5_with_1013'] = [int(((b5.own - Q.STD).abs() <= 0.5).sum()), int(len(b5))]
    res['crude_rates_y'] = {c: round(1000 * float(x.y.mean()), 2) for c, x in v.groupby('cls')}
    res['small_share'] = float(((v.dd >= 2) & (v.dd < 5)).sum() / v.y.sum())
    json.dump(res, open(out, 'w'), indent=1, default=str); print(json.dumps(res, indent=1, default=str))
