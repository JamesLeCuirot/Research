"""Post hoc (after review): setting at landing as the MODAL broadcast value in the 120 s before the last airborne point,
instead of the last value. Not pre-registered. Usage: python3 posthoc_modal_extract.py points.parquet landings_in.parquet landings_out.parquet"""
import sys, numpy as np, pandas as pd
pts, lin, out = sys.argv[1:4]
p = pd.read_parquet(pts, columns=['icao', 't', 'qnh']); p = p[p.qnh.notna()]
l = pd.read_parquet(lin)
p = p[p.icao.isin(set(l.icao))].sort_values(['icao', 't'])
g = {k: (v.t.values, v.qnh.values) for k, v in p.groupby('icao')}
mode = np.full(len(l), np.nan); nvals = np.zeros(len(l), int); held = np.full(len(l), np.nan)
for i, (ic, te) in enumerate(zip(l.icao.values, l.t_end.values)):
    if ic not in g: continue
    t, q = g[ic]; a = np.searchsorted(t, te - 120.0, 'left'); b = np.searchsorted(t, te, 'right')
    if b <= a: continue
    w = q[a:b]; u, c = np.unique(w, return_counts=True); mode[i] = u[np.argmax(c)]; nvals[i] = len(u)
    last = w[-1]; k = b - 1                       # how long the last value had been held (s), looking back up to 10 min
    a2 = np.searchsorted(t, te - 600.0, 'left')
    while k > a2 and q[k - 1] == last: k -= 1
    held[i] = t[b - 1] - t[k]
l['own_last'] = l.own; l['own'] = mode; l['n_distinct'] = nvals; l['held_s'] = held
l.to_parquet(out, index=False)
print(len(l), 'modal differs from last on', int((l.own_last.notna() & (l.own != l.own_last)).sum()), file=sys.stderr)
