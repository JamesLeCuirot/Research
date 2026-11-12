"""Pooled descriptive analysis of both samples (exploratory). Each sample is prepared separately with the frozen
functions (so exclusions and landings-per-aircraft are per sample, as in each sample's own analysis), then stacked.
Usage: python3 pooled_analysis.py out.json airports.csv us_metar.csv eu_metar.csv dir_sample1 dir_sample2"""
import sys, json, glob, numpy as np, pandas as pd
sys.path.insert(0, __file__.rsplit('/', 1)[0])
import qnh_analysis as Q, rep_analysis as R, posthoc_after_review3 as P
S = ['apt', 'date']
def rt(x, n): return [int(len(x)), int(x[n].sum()), round(1000 * float(x[n].mean()), 3)]
def test(d, y): r = Q.cmh(d, y, S); r['operator_ci'] = P.cluster_boot(d, y, 'oper'); return r

if __name__ == '__main__':
    out, airports_csv, mus, meu, d1, d2 = sys.argv[1:7]; parts = []
    for i, d in enumerate((d1, d2)):
        x = R.prepare(sorted(glob.glob(d + '/landings_*.parquet')), airports_csv); x['sample'] = i + 1; parts.append(x)
    a = pd.concat(parts, ignore_index=True)
    a['ongrid'] = (((a.own - 800.0) / 0.8) - ((a.own - 800.0) / 0.8).round()).abs() < 0.02
    cs = a.callsign.fillna('').str.strip(); a['oper'] = np.where(cs.str.match(r'^[A-Z]{3}\d'), cs.str[:3], 'AC_' + a.icao.astype(str))
    v = a[a.valid].copy(); og = v[v.ongrid]; e = a[a.std5_elig]; res = {}
    res['counts'] = dict(landings=int(len(a)), valid=int(len(v)), by_class=v.groupby('cls').size().to_dict(), aircraft=v.groupby('cls').icao.nunique().to_dict(), dates=int(v.date.nunique()),
                         no_value=int((~a.has & ~a.unstable).sum()), unstable=int(a.unstable.sum()), implausible=int((a.has & ~a.plaus).sum()), qfe_like=int(a.qfe_like.sum()), suspect_landings=int(a.suspect.sum()))
    res['coverage'] = {f'{c}|{g}': dict(landings=int(len(x)), recorded=round(float(x.has.mean() + x.unstable.mean()), 4), analysed=round(float(x.valid.mean()), 4)) for (c, g), x in a.groupby(['cls', 'region'])}
    res['rates_all'] = {n: Q.rate_ci(v, n) for n in ('y', 'y5', 'y10')}; res['rates_all_grid'] = {n: Q.rate_ci(og, n) for n in ('y', 'y5', 'y10')}
    res['rates_group'] = {f'{c}|{g}': {n: rt(x, n) for n in ('y', 'y5', 'y10')} for (c, g), x in v.groupby(['cls', 'region'])}
    res['rates_group_grid'] = {f'{c}|{g}': {n: rt(x, n) for n in ('y', 'y5', 'y10')} for (c, g), x in og.groupby(['cls', 'region'])}
    res['rates_class'] = {c: {n: rt(x, n) for n in ('y', 'y5', 'y10')} for c, x in v.groupby('cls')}
    res['rates_region_grid'] = {g: {n: rt(x, n) for n in ('y', 'y5', 'y10')} for g, x in og.groupby('region')}
    res['offgrid'] = {g: dict(landings=[int((~x.ongrid).sum()), int(len(x))], err5=[int((x.y5 & ~x.ongrid).sum()), int(x.y5.sum())]) for g, x in v.groupby('region')}
    v['small'] = ((v.dd >= 2.0) & (v.dd < 5.0)).astype(int); res['small_share'] = float(v.small.sum() / v.y.sum())
    res['small_rate_region_grid'] = {g: round(1000 * float(x.small.mean()), 3) for g, x in v[v.ongrid].groupby('region')}
    res['tests'] = dict(R1=test(v, 'y'), R2=test(v, 'y5'), R3=test(v[v.n_ac >= 10], 'y'), R4=test(e, 'std5'), small=test(v, 'small'), err10=test(v, 'y10'), aircraft_20plus=test(v[v.n_ac >= 20], 'y'),
                        R1_grid=Q.cmh(og, 'y', S), R2_grid=Q.cmh(og, 'y5', S), R4_grid=Q.cmh(e[e.ongrid], 'std5', S), R1_US=Q.cmh(v[v.eu == 0], 'y', S), R1_Europe=Q.cmh(v[v.eu == 1], 'y', S))
    res['by_landings_per_aircraft'] = {f'{c}|{b}': rt(x, 'y') for (c, b), x in v.assign(b=pd.cut(v.n_ac, [0, 1, 3, 9, 19, 1e9], labels=['1', '2-3', '4-9', '10-19', '20+'])).groupby(['cls', 'b'], observed=True)}
    res['std5_group'] = {f'{c}|{g}': [int(x.std5.sum()), int(len(x)), int(x[x.ongrid].std5.sum()), int(x.ongrid.sum())] for (c, g), x in e.groupby(['cls', 'region'])}
    b5 = v[(v.biz == 1) & (v.y5 == 1)]; res['biz_err5_with_1013'] = [int(((b5.own - Q.STD).abs() <= 0.5).sum()), int(len(b5))]
    b10 = v[(v.biz == 1) & (v.y10 == 1)]; res['biz_err10'] = dict(n=int(len(b10)), under_10_landings=int((b10.n_ac < 10).sum()), nonstandard_30plus=int(((b10.dd >= 30) & ((b10.own - Q.STD).abs() > 0.5)).sum()))
    res['us_over_europe_err5_grid'] = Q.region_test(og.assign(eu=1 - og.eu), 'y5', reps=5000); res['us_over_europe_err5_all'] = Q.region_test(v.assign(eu=1 - v.eu), 'y5', reps=5000)
    res['region_label_note'] = 'in us_over_europe_* the keys rate_eu/ev_eu/n_eu hold US values and vice versa; rr is US over Europe'
    top = v[v.biz == 1].oper.value_counts(); res['biz_top2_operator_share'] = round(float(top.head(2).sum() / (v.biz == 1).sum()), 3)
    mc, _ = P.clean_metar([mus, meu]); tmp = out + '.metar_clean.csv'; mc.to_csv(tmp, index=False); j = R.metar_join(a, [tmp])
    k = j[j.valid & j.metar.notna()].copy(); k['rm'] = (k.ref - k.metar).abs()
    res['metar'] = dict(n=int(len(k)), within_1=float((k.rm <= 1.0).mean()), within_1p7=float((k.rm <= 1.7).mean()), within_1_by_region={g: float((x.rm <= 1.0).mean()) for g, x in k.groupby('region')},
                        within_1_biz_heavy=float((k[k.groupby('apt').biz.transform('mean') > 0.6].rm <= 1.0).mean()))
    w = j[j.plaus & j.metar.notna() & ~j.qfe_like & ~j.suspect].copy(); w['dm'] = (w.own - w.metar).abs().round(1)
    for nm, th in (('or_2p4', 2.4), ('or_5', 5.0), ('or_2p0_nominal', 2.0)):
        w['yy'] = (w.dm >= th).astype(int); res['metar'][nm] = Q.cmh(w, 'yy', S)
    w['yy'] = (w.dm >= 2.4).astype(int); res['metar']['n_by_class'] = w.groupby('cls').size().to_dict()
    res['metar']['rate_2p4_by_consensus_available'] = {f'{c}|{h}': rt(x, 'yy') for (c, h), x in w.groupby(['cls', 'valid'])}
    json.dump(res, open(out, 'w'), indent=1, default=str); print(json.dumps(res, indent=None, default=str))
