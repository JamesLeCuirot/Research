"""Exploratory analyses added for journal submission (v0.7). Not pre-registered.
1. Military and government flights removed from the airline class.  2. Regression models with operator clustering and
an operator random intercept.  3. Whether small US discrepancies match the setting of a nearby airport.
Usage: python3 journal_upgrades.py out.json airports.csv metar_clean.csv dir_sample1 dir_sample2 [sample2|pooled y|y5]"""
import sys, json, glob, numpy as np, pandas as pd, scipy.sparse as sp
sys.path.insert(0, __file__.rsplit('/', 1)[0])
import qnh_analysis as Q, rep_analysis as R, posthoc_after_review3 as P
S = ['apt', 'date']
# ICAO three-letter designators of military and government operators (judgement list) and the US military address block
MILGOV = set('RCH CNV SAM PAT EVA\x00 GAF IAM CTM FAF BAF NAF PLF HAF AME RRR ASY CFC SHF NOH DAF SVF FNY IFC CEF HRZ SUI KAF UAF RSF RSD QAF MMF NAT NOW HUF HVK TUA SQF LYX VVV SPA\x00 AIO RFR CMB DCN GRZ ITF BGA LCS'.replace('\x00', '').split()) - {'EVA', 'SPA'}

def prep(d1, d2, airports_csv):
    parts = []
    for i, d in enumerate((d1, d2)):
        x = R.prepare(sorted(glob.glob(d + '/landings_*.parquet')), airports_csv); x['sample'] = i + 1; parts.append(x)
    a = pd.concat(parts, ignore_index=True); cs = a.callsign.fillna('').str.strip()
    a['prefix'] = np.where(cs.str.match(r'^[A-Z]{3}\d'), cs.str[:3], ''); a['oper'] = np.where(a.prefix != '', a.prefix, 'AC_' + a.icao.astype(str))
    h = a.icao.astype(str).str.lower(); a['milgov'] = (a.biz == 0) & (a.prefix.isin(MILGOV) | h.between('ae0000', 'afffff'))
    return a

def informative(v, y):
    g = v.groupby(S); nb = g.biz.transform('sum'); n = g.biz.transform('size'); ny = g[y].transform('sum')
    return v[(nb > 0) & (nb < n) & (ny > 0) & (ny < n)]

def models(v, y):
    """Logistic models on landings in informative airport-date strata: airport fixed effects, business-jet indicator."""
    import statsmodels.api as sm
    from statsmodels.genmod.bayes_mixed_glm import BinomialBayesMixedGLM
    w = informative(v, y).copy(); out = dict(n=int(len(w)), events=int(w[y].sum()))
    X = pd.get_dummies(w[['apt']], drop_first=True, dtype=float); X.insert(0, 'biz', w.biz.values.astype(float)); X.insert(0, 'const', 1.0)
    keep = X.columns[(X.sum() > 0)]; X = X[keep]
    m = sm.GLM(w[y].values, X.values, family=sm.families.Binomial()).fit(cov_type='cluster', cov_kwds=dict(groups=pd.factorize(w.oper)[0]))
    i = list(X.columns).index('biz'); b, se = m.params[i], m.bse[i]
    out['logit_fe_cluster_operator'] = dict(or_=float(np.exp(b)), lo=float(np.exp(b - 1.96 * se)), hi=float(np.exp(b + 1.96 * se)), n_clusters=int(w.oper.nunique()))
    import os
    if os.environ.get('NO_MIXED'): return out
    try:
        codes, _ = pd.factorize(w.oper); Z = sp.csr_matrix((np.ones(len(w)), (np.arange(len(w)), codes)))
        Xa = pd.get_dummies(w[['apt']], drop_first=True, dtype=float); Xa.insert(0, 'biz', w.biz.values.astype(float)); Xa.insert(0, 'const', 1.0)
        mm = BinomialBayesMixedGLM(w[y].values, Xa.values, Z, ident=np.zeros(Z.shape[1], dtype=int), vcp_p=2.0, fe_p=5.0).fit_vb()
        b, se = mm.fe_mean[1], mm.fe_sd[1]
        out['mixed_operator_random_intercept'] = dict(or_=float(np.exp(b)), lo=float(np.exp(b - 1.96 * se)), hi=float(np.exp(b + 1.96 * se)), re_sd=float(np.exp(mm.vcp_mean[0])), method='variational Bayes, airport fixed effects')
    except Exception as ex: out['mixed_operator_random_intercept'] = dict(error=str(ex)[:200])
    return out

def nearby(v, airports_csv, metar_csv):
    """For US discrepancies of 2 to 5 hPa: does the broadcast value match (within 0.5 hPa) the latest setting at another
    study airport within 100 NM? Chance baseline: the mirror value (reference minus the discrepancy) tested the same way."""
    ap = pd.read_csv(airports_csv, usecols=['ident', 'latitude_deg', 'longitude_deg']).set_index('ident')
    m = pd.read_csv(metar_csv); m['apt'] = np.where(m.station.str.len() == 3, 'K' + m.station, m.station)
    m['tm'] = (pd.to_datetime(m.valid, utc=True) - pd.Timestamp('1970-01-01', tz='UTC')).dt.total_seconds(); m['h'] = m.alti * 33.8639
    mg = {k: (g.tm.values, g.h.values) for k, g in m.sort_values('tm').groupby('apt')}
    apts = [x for x in v.apt.unique() if x in ap.index and x in mg]; la = np.radians(ap.loc[apts].latitude_deg.values); lo = np.radians(ap.loc[apts].longitude_deg.values)
    dist = 3440.065 * np.arccos(np.clip(np.sin(la)[:, None] * np.sin(la)[None, :] + np.cos(la)[:, None] * np.cos(la)[None, :] * np.cos(lo[:, None] - lo[None, :]), -1, 1))
    near = {x: [apts[j] for j in np.where((dist[i] <= 100) & (dist[i] > 0))[0]] for i, x in enumerate(apts)}
    def latest(st, t):
        tm, h = mg[st]; i = np.searchsorted(tm, t) - 1
        return h[i] if i >= 0 and t - tm[i] <= 4200 else np.nan
    s = v[(v.eu == 0) & (v.dd >= 2) & (v.dd < 5) & v.apt.isin(apts)].copy(); rows = []
    for r in s.itertuples():
        ns = near.get(r.apt, []); 
        if not ns: continue
        vals = np.array([latest(n, r.t_end) for n in ns]); vals = vals[~np.isnan(vals)]
        if len(vals) == 0: continue
        mirror = 2 * r.ref - r.own
        rows.append((r.cls, bool((np.abs(vals - r.own) <= 0.5).any()), bool((np.abs(vals - mirror) <= 0.5).any()), len(vals)))
    t = pd.DataFrame(rows, columns=['cls', 'match', 'mirror', 'k'])
    return dict(us_small_total=s.groupby('cls').size().to_dict(), with_nearby_station=t.groupby('cls').size().to_dict(), match_nearby=t.groupby('cls').match.mean().round(4).to_dict(),
                match_mirror_baseline=t.groupby('cls')['mirror'].mean().round(4).to_dict(), mean_nearby_stations=float(t.k.mean()))

if __name__ == '__main__':
    out, airports_csv, metar_csv, d1, d2 = sys.argv[1:6]; a = prep(d1, d2, airports_csv); v = a[a.valid].copy(); v2 = v[v['sample'] == 2]; res = {}
    mg_ = v[v.milgov]; res['milgov'] = dict(landings=int(len(mg_)), by_prefix=mg_.prefix.value_counts().head(25).to_dict(), errors_2=int(mg_.y.sum()), errors_5=int(mg_.y5.sum()))
    for nm, d in (('pooled', v), ('sample2', v2)):
        x = d[~d.milgov]; res[f'excl_milgov_{nm}'] = dict(R1=Q.cmh(x, 'y', S), R2=Q.cmh(x, 'y5', S))
    res['nearby_station'] = dict(pooled=nearby(v, airports_csv, metar_csv), sample2=nearby(v2, airports_csv, metar_csv))
    if len(sys.argv) > 6:   # run one model per process to limit memory: journal_upgrades.py ... sample2|pooled y|y5
        nm, y = sys.argv[6:8]; old = json.load(open(out)); old[f'models_{nm}_{y}'] = models(v2 if nm == 'sample2' else v, y); json.dump(old, open(out, 'w'), indent=1, default=str); sys.exit()
    json.dump(res, open(out, 'w'), indent=1, default=str)
    print(json.dumps(res, default=str))
