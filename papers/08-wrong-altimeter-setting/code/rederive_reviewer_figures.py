"""Re-derivation by the analysis author of figures that earlier drafts quoted from the AI reviewers (exploratory).
Usage: python3 rederive_reviewer_figures.py out.json airports.csv metar_clean.csv dir_sample1 dir_sample2 points_dir_sample2"""
import sys, json, glob, os, numpy as np, pandas as pd
from scipy import stats
sys.path.insert(0, __file__.rsplit('/', 1)[0])
import qnh_analysis as Q, rep_analysis as R, journal_upgrades as J
S = ['apt', 'date']; STD = Q.STD

def trace(points_dir, ev, back=1800.0):
    """Broadcast-setting history before each landing in ev (columns icao, t_end, date)."""
    rows = []
    for date, g in ev.groupby('date'):
        fs = [f for f in (os.path.join(points_dir, f'points_{d}.parquet') for d in {date, str((pd.Timestamp(date) - pd.Timedelta(days=1)).date())}) if os.path.exists(f)]
        p = pd.concat([pd.read_parquet(f, columns=['icao', 't', 'qnh'], filters=[('icao', 'in', list(g.icao.unique()))]) for f in fs]); p = p[p.qnh.notna()]
        for r in g.itertuples():
            q = p[(p.icao == r.icao) & (p.t <= r.t_end) & (p.t >= r.t_end - back)].sort_values('t')
            if len(q) == 0: rows.append(dict(i=r.Index, n=0)); continue
            vals = q.qnh.values; last2 = q[q.t >= r.t_end - 120].qnh.values; ch = np.flatnonzero(np.diff(vals) != 0)
            rows.append(dict(i=r.Index, n=int(len(q)), observed_s=float(r.t_end - q.t.iloc[0]), n_distinct=int(len(set(np.round(vals, 1)))), first=float(vals[0]), last=float(vals[-1]),
                             all_std=bool((np.abs(vals - STD) <= 0.5).all()), changed_into_std=bool(abs(vals[0] - STD) > 0.5 and abs(vals[-1] - STD) <= 0.5),
                             n_changes=int(len(ch)), last_change_s_before=float(r.t_end - q.t.iloc[ch[-1] + 1]) if len(ch) else None, n_distinct_last120=int(len(set(np.round(last2, 1))))))
    return pd.DataFrame(rows).set_index('i')

def airline_only_reference(a):
    """Odds ratio for 2 hPa or more with the reference built from airline aircraft only (same window and consensus rules)."""
    a = a.reset_index(drop=True); ref = np.full(len(a), np.nan); cons = np.full(len(a), np.nan)
    for apt, g in a[a.plaus].groupby('apt'):
        pool = g[g.biz == 0].sort_values('t_end'); pt = pool.t_end.values; pv = pool.own.values; pic = pool.icao.values
        lo = np.searchsorted(pt, g.t_end.values - Q.WIN, 'left'); hi = np.searchsorted(pt, g.t_end.values + Q.WIN, 'right')
        for k, (ix, ic) in enumerate(zip(g.index.values, g.icao.values)):
            sl = slice(lo[k], hi[k]); m = pic[sl] != ic
            if m.sum() < Q.MIN_OTHERS or len(set(pic[sl][m])) < Q.MIN_OTHERS: continue
            w = pv[sl][m]; med = np.median(w); ref[ix] = med; cons[ix] = (np.abs(w - med) <= 1.0).mean()
    ok = a.plaus & ~np.isnan(ref) & (cons >= Q.CONSENSUS) & ~a.qfe_like & ~a.suspect
    v = a[ok].copy(); v['yy'] = ((v.own - ref[ok.values]).abs().round(1) >= 2.0).astype(int)
    return Q.cmh(v, 'yy', S)

if __name__ == '__main__':
    out, airports_csv, metar_csv, d1, d2, pdir2 = sys.argv[1:7]
    a = J.prep(d1, d2, airports_csv); a['ongrid'] = (((a.own - 800.0) / 0.8) - ((a.own - 800.0) / 0.8).round()).abs() < 0.02
    v = a[a.valid].copy(); v1 = v[v['sample'] == 1]; v2 = v[v['sample'] == 2]; res = {}
    # A. which aircraft carry the off-grid (second-source) large discrepancies in Europe
    og = v[(v.eu == 1) & (v.y5 == 1) & ~v.ongrid]; allv = a[a.plaus]
    per = allv[allv.icao.isin(og.icao.unique())].groupby(['icao', 'actype']).apply(lambda x: pd.Series(dict(landings=len(x), near_1013=int(((x.own - STD).abs() <= 0.5).sum()), offgrid=int((~x.ongrid).sum())))).reset_index()
    res['A_offgrid_europe_err5'] = dict(events=int(len(og)), aircraft=int(og.icao.nunique()), by_type=og.actype.value_counts().to_dict(), events_within_0p5_of_1013=int(((og.own - STD).abs() <= 0.5).sum()),
                                        aircraft_with_1013_on_half_or_more_landings=int((per.near_1013 >= 0.5 * per.landings).sum()), aircraft_table=per.sort_values('landings', ascending=False).head(25).to_dict('records'))
    # B. traces of second-sample business-jet '1013 at landing' events
    e2 = a[(a['sample'] == 2) & a.std5_elig & (a.std5 == 1) & (a.biz == 1)]; t = trace(pdir2, e2)
    others = allv[allv.icao.isin(e2.icao)]; oth = others.groupby('icao').apply(lambda x: int(((x.own - STD).abs() > 0.5).sum()))
    res['B_biz_1013_traces_sample2'] = dict(events=int(len(e2)), types=int(e2.actype.nunique()), with_trace=int((t.n > 0).sum()), all_values_1013_in_observed_window=int(t.all_std.fillna(False).sum()), changed_into_1013=int(t.changed_into_std.fillna(False).sum()),
                                            other_pattern=int(((t.n > 0) & ~t.all_std.fillna(False) & ~t.changed_into_std.fillna(False)).sum()), observed_minutes_quartiles=[round(float(x) / 60, 1) for x in t.observed_s.quantile([.25, .5, .75])],
                                            aircraft=int(e2.icao.nunique()), aircraft_with_a_non_1013_value_on_another_landing=int((oth.reindex(e2.icao.unique()).fillna(0) > 0).sum()),
                                            aircraft_with_no_other_landing=int((others.groupby('icao').size().reindex(e2.icao.unique()).fillna(0) <= 1).sum()))
    # C. implausibly large non-standard business-jet values, second sample
    big = v2[(v2.biz == 1) & (v2.dd >= 30) & ((v2.own - STD).abs() > 0.5)]; tb = trace(pdir2, big, back=1800.0)
    lst = big[['icao', 'actype', 'apt', 'own', 'ref', 'n_distinct', 'held_s']].join(tb[['observed_s', 'n_distinct', 'first', 'last', 'n_changes', 'last_change_s_before']], rsuffix='_trace')
    lst['other_landings_same_value'] = [int((np.abs(allv[(allv.icao == r.icao)].own - r.own) < 0.05).sum()) - 1 for r in big.itertuples()]
    lst['inch_slip'] = ((lst.own - lst.ref).abs() - 33.86).abs() < 1.0
    lst['changed_in_last_3_min'] = lst.last_change_s_before.fillna(1e9) <= 180
    res['C_biz_30plus_nonstandard_sample2'] = dict(n=int(len(big)), changed_in_last_3_min=int(lst.changed_in_last_3_min.sum()), repeated_on_other_landings=int((lst.other_landings_same_value > 0).sum()), about_one_inch=int(lst.inch_slip.sum()), cases=json.loads(lst.round(1).to_json(orient='records')))
    # D. do aircraft with a discrepancy in the first sample have a higher rate in the second?
    d = {}
    for cls, x2 in v2.groupby('cls'):
        x1 = v1[v1.cls == cls]; seen = set(x1.icao); had = set(x1[x1.y == 1].icao); z = x2[x2.icao.isin(seen)]; h = z.icao.isin(had)
        d[cls] = dict(with_prior=[int(h.sum()), int(z[h].y.sum()), round(1000 * float(z[h].y.mean()), 2)], without_prior=[int((~h).sum()), int(z[~h].y.sum()), round(1000 * float(z[~h].y.mean()), 2)])
    res['D_repeat_across_samples'] = d
    # E. airline-only reference
    res['E_airline_only_reference'] = dict(sample1=airline_only_reference(a[a['sample'] == 1]), sample2=airline_only_reference(a[a['sample'] == 2]))
    # F. steadiness and one-off nature of business-jet discrepancies
    b = v[(v.biz == 1) & (v.y == 1)]; nv = allv.groupby('icao').own.agg(lambda x: len(set(np.round(x, 1))))
    res['F_biz_discrepancies'] = dict(n=int(len(b)), single_value_in_last_120s=int((b.n_distinct == 1).sum()), aircraft_showing_other_values_elsewhere=int((b.icao.map(nv) > 1).sum()),
                                      aircraft_with_two_or_more=int((b.groupby(['sample', 'icao']).size() >= 2).sum()), aircraft=int(b.groupby(['sample', 'icao']).ngroups))
    # G. broadcast coverage against discrepancy rate, by business-jet type
    g = a[a.biz == 1].groupby('actype').apply(lambda x: pd.Series(dict(landings=len(x), recorded=float((x.has | x.unstable).mean()), valid=int(x.valid.sum()), rate=float(1000 * x[x.valid].y.mean()) if x.valid.sum() else np.nan))); g = g[g.landings >= 1000].dropna()
    rho, p = stats.spearmanr(g.recorded, g.rate); res['G_coverage_vs_rate_biz_types'] = dict(types=int(len(g)), spearman_rho=float(rho), p=float(p), table=json.loads(g.round(3).reset_index().to_json(orient='records')))
    # H. figures previously computed in session
    s1 = set(a[a['sample'] == 1].icao); res['H_overlap_sample2_landings_by_aircraft_in_sample1'] = {c: round(float(x.icao.isin(s1).mean()), 4) for c, x in v2.groupby('cls')}
    sm = v[(v.dd >= 2) & (v.dd < 5)]; res['H_small_at_2p4_or_3p2'] = round(float(sm.dd.isin([2.4, 3.2]).mean()), 3); res['H_small_value_counts'] = sm.dd.value_counts().head(6).to_dict()
    m = pd.read_csv(metar_csv); m['apt'] = np.where(m.station.str.len() == 3, 'K' + m.station, m.station); m['tm'] = (pd.to_datetime(m.valid, utc=True) - pd.Timestamp('1970-01-01', tz='UTC')).dt.total_seconds(); m['h'] = m.alti * 33.8639
    mg = {k: (x.tm.values, x.h.values) for k, x in m.sort_values('tm').groupby('apt')}
    def stale(r):
        if r.apt not in mg: return np.nan
        tm, h = mg[r.apt]; i0 = np.searchsorted(tm, r.t_end - 7200); i1 = np.searchsorted(tm, r.t_end)
        return float((np.abs(h[i0:i1] - r.own) <= 1.0).any()) if i1 > i0 else np.nan
    for nm, x in (('sample2', v2), ('pooled', v)):
        z = x[(x.dd >= 2) & (x.dd < 5) & (x.eu == 0)]; z = z.assign(st=z.apply(stale, axis=1)); res[f'H_us_small_matching_destination_last_2h_{nm}'] = {c: [int(y.st.notna().sum()), round(float(y.st.mean()), 3)] for c, y in z.groupby('cls')}
    json.dump(res, open(out, 'w'), indent=1, default=str); print(json.dumps(res, default=str))
