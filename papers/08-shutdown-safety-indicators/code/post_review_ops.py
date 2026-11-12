"""EXPLORATORY checks added after the flight-operations review (not preregistered). They reproduce, with this
repository's own code, the reviewer's findings that the revised paper relies on. Reads the per-day attempt files.
Usage: python3 post_review_ops.py WORKDIR RESULTS_DIR"""
import sys, os, json, glob, gzip
import numpy as np, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import analysis as A
work, res = sys.argv[1], sys.argv[2]
rng = np.random.default_rng(A.SEED + 4); NB = 2000; out = {}
t = pd.read_csv(os.path.join(res, 'airport_day.csv')); t['date'] = [A.d(z) for z in t.date]; t['pdate'] = [A.d(z) for z in t.pdate]
key = t[['date', 'apt', 'us', 'grp', 'year', 'pdate']]

# RA event times per aircraft (first message after >=120 s without one), all aircraft, for matching to go-arounds
def ra_times(f):
    last = {}; ev = []
    for line in gzip.open(f, 'rt', errors='replace'):
        line = line.strip().rstrip(',')
        if not line.startswith('{'): continue
        try: x = json.loads(line)
        except Exception: continue
        ts = (x.get('acas_ra') or {}).get('unix_timestamp'); h = x.get('hex')
        if ts is None or h is None: continue
        if h not in last or ts - last[h] > 120: ev.append((h, ts))
        last[h] = ts
    return pd.DataFrame(ev, columns=['icao', 'tra'])

fr = []
for f in sorted(glob.glob(os.path.join(work, 'data/att/*.parquet'))):
    day = os.path.basename(f)[:10]
    q = pd.read_parquet(f, columns=['apt', 'icao', 'cls', 'callsign', 'outcome', 'gap_s', 'fol_nm', 'rwy', 'hmin', 'h_last', 'confirmed', 't_end'])
    q['date'] = A.d(day); q, _ = A.apply_rule1(q)
    q['ga'] = (q.outcome == 'ga').astype('int8'); q['ralink'] = np.int8(0)
    rf = os.path.join(work, 'data/acas', day + '.json.gz')
    if os.path.exists(rf) and q.ga.sum():
        r = ra_times(rf); g = q[q.ga == 1][['icao', 't_end']].reset_index().merge(r, on='icao')
        q.loc[g[(g.tra - g.t_end).abs() <= 180]['index'].unique(), 'ralink'] = 1
    fr.append(q[['date', 'apt', 'rwy', 'ga', 'ralink', 'hmin', 'h_last', 'confirmed', 'fol_nm']])
a = pd.concat(fr, ignore_index=True); del fr
a = a.merge(key, on=['date', 'apt'])                      # kept airport-days only
a['ga_hi'] = ((a.ga == 1) & (a.hmin >= 200)).astype(int); a['ga_lo'] = ((a.ga == 1) & (a.hmin < 200)).astype(int)
a['ga_nora'] = ((a.ga == 1) & (a.ralink == 0)).astype(int); a['ga_hi_nora'] = ((a.ga_hi == 1) & (a.ralink == 0)).astype(int)
a['one'] = 1; a['pair'] = a.fol_nm.notna().astype(int); a['tight'] = (a.fol_nm < 2.5).astype(int)
low = a.h_last < 30
a['pair_low'] = (a.pair == 1) & low; a['tight_low'] = (a.tight == 1) & low
cols = ['one', 'ga', 'ga_hi', 'ga_lo', 'ga_nora', 'ga_hi_nora', 'ralink', 'pair', 'tight', 'pair_low', 'tight_low']
T = a.groupby(['date', 'apt', 'us', 'grp', 'year', 'pdate'])[cols].sum().reset_index().rename(columns={'one': 'n'})
for c in ('pair_low', 'tight_low'): T[c] = T[c].astype(int)
sh = A.in_window(T, 'shutdown'); base = A.in_window(T, 'baseline')
def summ(x, num, den='n', nb=NB):
    est = A.log_rrr(x, num, den); lo, hi, se = A.ci(A.boot_days(x, lambda z: A.log_rrr(z, num, den), rng, nb))
    return dict(rrr=float(np.exp(est)), ci=[float(np.exp(lo)), float(np.exp(hi))])
def rates(x, num, den='n', per=1000):
    g = x.groupby(['us', 'year'])[[num, den]].sum()
    return {f"{'us' if u else 'ctl'}{y}": dict(count=int(g.loc[(u, y), num]), rate=float(per * g.loc[(u, y), num] / g.loc[(u, y), den])) for (u, y) in g.index}

# 1. Go-arounds by lowest height reached (below 200 ft is the class most dependent on low-level coverage)
out['ga_below_200ft_shutdown'] = rates(sh, 'ga_lo'); out['ga_200ft_or_above_shutdown'] = rates(sh, 'ga_hi')
out['rrr_ga_200ft_or_above_shutdown'] = summ(sh, 'ga_hi'); out['rrr_ga_200ft_or_above_september'] = summ(base, 'ga_hi')
g = sh.groupby(['apt', 'year']).ga_lo.sum().unstack(); g['diff'] = g[2025] - g[2024]
out['ga_below_200ft_largest_changes'] = {k: [int(v[2024]), int(v[2025])] for k, v in g.sort_values('diff', ascending=False).head(8).iterrows()}
# 2. Go-arounds linked to a resolution advisory by the same aircraft within 180 s
out['ra_linked_goarounds'] = {w: rates(x, 'ralink') for w, x in (('september', base), ('shutdown', sh))}
out['ga_rate_excluding_ra_linked_shutdown'] = rates(sh, 'ga_nora'); out['rrr_ga_excluding_ra_linked_shutdown'] = summ(sh, 'ga_nora')
out['rrr_ga_excluding_ra_linked_september'] = summ(base, 'ga_nora')
out['rrr_ga_200ft_and_not_ra_linked_shutdown'] = summ(sh, 'ga_hi_nora'); out['rrr_ga_200ft_and_not_ra_linked_september'] = summ(base, 'ga_hi_nora')
s = T[T.apt == 'KSFO'].groupby('year')[['ga', 'ralink']].sum(); out['SFO_goarounds_77_days'] = {str(y): dict(all=int(s.loc[y, 'ga']), ra_linked=int(s.loc[y, 'ralink'])) for y in s.index}
# 3. Coverage indicators
lz = a[a.ga == 0]
out['landings_ground_confirmed_share'] = {f"{'us' if u else 'ctl'}{y}": float(v) for (u, y), v in lz.groupby(['us', 'year']).confirmed.mean().items()}
out['pairs_leader_seen_below_30ft_share'] = {f"{'us' if u else 'ctl'}{y}": float(v) for (u, y), v in (T.groupby(['us', 'year']).pair_low.sum() / T.groupby(['us', 'year']).pair.sum()).items()}
# 4. Spacing restricted to pairs whose leader was tracked to below 30 ft
p = a[(a.pair == 1)]; p = p.assign(band=pd.cut(p.h_last, [-1e9, 30, 100, 300, 1e9], labels=['<30', '30-100', '100-300', '>300']))
out['tight_share_by_leader_last_height_us'] = {f'{b}_{y}': float(v) for (b, y), v in p[p.us == 1].groupby(['band', 'year'], observed=True).tight.mean().items()}
out['spacing_leader_below_30ft'] = dict(september=summ(base, 'tight_low', 'pair_low'), shutdown=summ(sh, 'tight_low', 'pair_low'))
both = pd.concat([sh.assign(w='shutdown'), base.assign(w='baseline')])
def adj(z): return A.log_rrr(z[z.w == 'shutdown'], 'tight_low', 'pair_low') - A.log_rrr(z[z.w == 'baseline'], 'tight_low', 'pair_low')
lo, hi, se = A.ci(A.boot_days(both, adj, rng, NB, strata=['baseline', 'shutdown'])); out['spacing_leader_below_30ft']['baseline_adjusted'] = dict(rrr=float(np.exp(adj(both))), ci=[float(np.exp(lo)), float(np.exp(hi))])
# 5. Runway ends present in one year and almost absent in the other (closure or detection gap), all 77 days
L = lz.groupby(['apt', 'rwy', 'year']).size().unstack(fill_value=0); tot = L.groupby('apt').transform('sum'); S = L / tot
flag = S[((S[2024] >= 0.04) & (S[2025] < 0.004)) | ((S[2025] >= 0.04) & (S[2024] < 0.004))]
out['runway_ends_in_one_year_only'] = {f'{ap} {rw}': [int(L.loc[(ap, rw), 2024]), int(L.loc[(ap, rw), 2025])] for (ap, rw) in flag.index}
bad = sorted(set(flag.index.get_level_values('apt'))); out['airports_with_runway_change'] = bad
x = sh[~sh.apt.isin(bad)]; out['rrr_excluding_runway_change_airports_shutdown'] = dict(summ(x, 'ga'), airports=int(x.apt.nunique()))
x = base[~base.apt.isin(bad)]; out['rrr_excluding_runway_change_airports_september'] = summ(x, 'ga')
# 5b. Runway use and go-arounds at two airports discussed in the paper (all 77 days)
rw = a[a.apt.isin(['KBOS', 'KSAN'])].groupby(['apt', 'rwy', 'year']).agg(approaches=('one', 'sum'), go_arounds=('ga', 'sum')).reset_index()
out['runway_use_BOS_SAN'] = {f'{r_.apt} {r_.rwy} {r_.year}': [int(r_.approaches), int(r_.go_arounds)] for r_ in rw.itertuples()}
# 6. RA events by airport: SFO and BUR
r = pd.concat([A.in_window(t, 'baseline').assign(w='september'), A.in_window(t, 'shutdown').assign(w='shutdown')]); r = r[r.us == 1]
tab = {}
for name, m in (('all', r.apt == r.apt), ('KSFO', r.apt == 'KSFO'), ('KBUR', r.apt == 'KBUR'), ('excl_SFO_BUR', ~r.apt.isin(['KSFO', 'KBUR']))):
    g = r[m].groupby(['w', 'year'])[['ra', 'n']].sum(); tab[name] = {f'{w}{y}': dict(events=int(g.loc[(w, y), 'ra']), per_1000=float(1000 * g.loc[(w, y), 'ra'] / g.loc[(w, y), 'n'])) for (w, y) in g.index}
out['ra_by_airport'] = tab
def ra_stat(z):
    g = z.groupby(['w', 'year'])[['ra', 'n']].sum(); q = g.ra / g.n
    return float(np.log((q[('shutdown', 2025)] / q[('september', 2025)]) / (q[('shutdown', 2024)] / q[('september', 2024)])))
z = r[~r.apt.isin(['KSFO', 'KBUR'])]; lo, hi, se = A.ci(A.boot_days(z, ra_stat, rng, NB, strata=['baseline', 'shutdown']))
out['ra_ratio_excl_SFO_BUR'] = dict(ratio=float(np.exp(ra_stat(z))), ci=[float(np.exp(lo)), float(np.exp(hi))])
json.dump(out, open(os.path.join(res, 'post_review_ops.json'), 'w'), indent=1, default=float)
def rr_(v):
    if isinstance(v, float): return round(v, 3)
    if isinstance(v, dict): return {k: rr_(b) for k, b in v.items()}
    if isinstance(v, list): return [rr_(b) for b in v]
    return v
print(json.dumps(rr_(out)))
