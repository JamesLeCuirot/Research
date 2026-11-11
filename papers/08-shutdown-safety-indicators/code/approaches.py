"""Stage 2: identify approach attempts (landings, go-arounds), gate measurements and in-trail spacing.
Detection logic is unchanged from the author's previous study (validated there by inspection); this version adds
the follower-distance spacing measure and the study airport list.
Usage: python3 approaches.py points.parquet runways.csv airports.csv airports_study.csv out_attempts.parquet"""
import sys, numpy as np, pandas as pd
NM = 1852.0; FT = 0.3048
GATES = (1000, 500)
def load_runways(path, apts):
    r = pd.read_csv(path); r = r[r.airport_ident.isin(apts) & (r.closed == 0)]
    r = r.dropna(subset=['le_latitude_deg','le_longitude_deg','he_latitude_deg','he_longitude_deg'])
    ends = []
    for _, w in r.iterrows():
        for a, b in (('le','he'), ('he','le')):
            ends.append(dict(apt=w.airport_ident, rwy=str(w[a+'_ident']), lat=w[a+'_latitude_deg'], lon=w[a+'_longitude_deg'],
                             olat=w[b+'_latitude_deg'], olon=w[b+'_longitude_deg'],
                             elev=w[a+'_elevation_ft'], disp=(w[a+'_displaced_threshold_ft'] if pd.notna(w[a+'_displaced_threshold_ft']) else 0.0),
                             width=w.width_ft if pd.notna(w.width_ft) else 150.0))
    return pd.DataFrame(ends)
def proj(lat, lon, lat0, lon0):
    return np.radians(lon - lon0) * np.cos(np.radians(lat0)) * 6371000.0, np.radians(lat - lat0) * 6371000.0
def angdiff(a, b): return (a - b + 180.0) % 360.0 - 180.0
def qnh_corr(q): return -145366.45 * (1.0 - (q / 1013.25) ** 0.190284)

def process_airport(apt, df, ends, apt_elev):
    lat0, lon0 = ends.lat.mean(), ends.lon.mean()
    E = []
    for _, e in ends.iterrows():
        tx, ty = proj(e.lat, e.lon, lat0, lon0); ox, oy = proj(e.olat, e.olon, lat0, lon0)
        L = np.hypot(ox-tx, oy-ty); ux, uy = (ox-tx)/L, (oy-ty)/L
        tx += ux*e.disp*FT; ty += uy*e.disp*FT; L -= e.disp*FT
        E.append(dict(rwy=e.rwy, tx=tx, ty=ty, ux=ux, uy=uy, L=L, course=(np.degrees(np.arctan2(ux, uy)) % 360),
                      elev=(e.elev if pd.notna(e.elev) else apt_elev), halfw=max(e.width*FT/2, 23.0)+25.0))
    df = df[~((df['flags'].fillna(0).astype(int) & 8) > 0) | df.ground]      # drop points whose altitude is geometric
    df = df.sort_values(['icao','t']).reset_index(drop=True)
    # --- QNH series from crew-selected altimeter settings (nav_qnh) of aircraft low near the airport
    q = df[df.qnh.between(940, 1060) & (df.alt < apt_elev + 2500)][['t','qnh','icao']]
    if len(q) < 5: return []
    qt = q.t.values; qv = q.qnh.values; qi = q.icao.values
    o = np.argsort(qt); qt, qv, qi = qt[o], qv[o], qi[o]
    def qnh_at(tq):
        for half in (1800, 7200):
            a, b = np.searchsorted(qt, [tq-half, tq+half])
            if b-a >= 5 and len(set(qi[a:b])) >= 3: return float(np.median(qv[a:b]))
        return np.nan
    x, y = proj(df.lat.values, df.lon.values, lat0, lon0)
    df['x'] = x; df['y'] = y
    out = []
    def rel(e, X, Y):
        return -((X-e['tx'])*e['ux'] + (Y-e['ty'])*e['uy']), -(X-e['tx'])*e['uy'] + (Y-e['ty'])*e['ux']
    def gates(v, e, t_end, corr, rec):
        tv = v.t.values
        m = (tv >= t_end-600) & (tv <= t_end) & ~v.ground.values & np.isfinite(v.alt.values)
        a = v[m]
        if len(a) < 5: return
        t = a.t.values; h = a.alt.values + corr - e['elev']
        d, c = rel(e, a.x.values, a.y.values)
        gs = a.gs.values; vr = a.vrate.values; trk = a.track.values; src = a.src.values
        low = (h >= 50) & (h <= 300) & (d > -200)
        rec['gs_ref'] = float(np.nanmedian(gs[low])) if low.sum() >= 2 else np.nan
        rec['hmin'] = float(np.nanmin(h)); rec['h_end'] = float(h[-1])
        for G in GATES:
            cr = np.nonzero((h[:-1] >= G) & (h[1:] < G))[0]
            if len(cr) == 0: continue
            k = cr[-1]
            if t[k+1]-t[k] > 15 or not (str(src[k]).startswith('adsb_icao') and str(src[k+1]).startswith('adsb_icao')): continue
            f = (h[k]-G)/max(h[k]-h[k+1], 1e-6); tg = t[k] + f*(t[k+1]-t[k])
            w = (np.abs(h-G) <= 100) & (np.abs(t-tg) <= 40)
            if w.sum() < 2: continue
            dg = d[k] + f*(d[k+1]-d[k]); cg = c[k] + f*(c[k+1]-c[k])
            sink = np.nanmedian(vr[w]) if np.isfinite(vr[w]).any() else np.nan
            if not np.isfinite(sink):
                ww = np.nonzero(w)[0]; sink = (h[ww[-1]]-h[ww[0]])/max(t[ww[-1]]-t[ww[0]],1e-6)*60
            rec[f'ok{G}'] = True; rec[f't{G}'] = tg; rec[f'd{G}'] = dg; rec[f'x{G}'] = cg; rec[f'sink{G}'] = float(sink)
            rec[f'gs{G}'] = float(np.nanmedian(gs[w])); rec[f'trk{G}'] = float(angdiff(trk[k+1], e['course']))
            rec[f'theta{G}'] = float(np.degrees(np.arctan2(G*FT, dg + 1000*FT)))
            iw = a.ias.values[w]; rec[f'ias{G}'] = float(np.nanmedian(iw)) if np.isfinite(iw).any() else np.nan
    for icao, g in df.groupby('icao', sort=False):
        tt = g.t.values
        brk = np.nonzero(np.diff(tt) > 600)[0] + 1
        for s, e_ in zip(np.r_[0, brk], np.r_[brk, len(g)]):
            v = g.iloc[s:e_]
            if len(v) < 10: continue
            t = v.t.values; gr = v.ground.values; alt = v.alt.values; X = v.x.values; Y = v.y.values; trk = v.track.values; gs = v.gs.values
            base = dict(apt=apt, icao=icao, reg=v.reg.iloc[0], actype=v.actype.iloc[0], cls=v.cls.iloc[0])
            air = ~gr & np.isfinite(alt); ai = np.nonzero(air)[0]
            if len(ai) < 8: continue
            # ---- landing: last airborne point of a run, on short final, followed by ground on that runway (<=90 s) or by no airborne data for the rest of the visit
            land = None
            nxt_gr = np.r_[gr[1:], False][ai]; gap_next = np.r_[np.diff(t[ai]), np.inf]
            for n_ in np.nonzero(nxt_gr | (gap_next > 90))[0]:
                p = ai[n_]
                Q = qnh_at(t[p])
                if not np.isfinite(Q): continue
                corr = qnh_corr(Q)
                pre = (t >= t[p]-600) & (t <= t[p]) & air
                if np.nanmax(alt[pre]) < alt[p] + 1500: continue
                for k, e in enumerate(E):
                    dd, cc = rel(e, X[p], Y[p]); h = alt[p] + corr - e['elev']
                    if not (abs(cc) <= 150 and -e['L'] <= dd <= 2.5*NM and h < 700 and np.isfinite(trk[p]) and abs(angdiff(trk[p], e['course'])) <= 15): continue
                    confirmed = False
                    if p+1 < len(v) and gr[p+1] and t[p+1]-t[p] <= 90:
                        d2, c2 = rel(e, X[p+1], Y[p+1])
                        confirmed = (-e['L']-300 <= d2 <= 300) and abs(c2) <= e['halfw']
                    later_air = air & (t > t[p]) & (t <= t[p]+600) & (alt > alt[p]+200)
                    if confirmed or not later_air.any():
                        land = dict(p=p, k=k, t=t[p], corr=corr, confirmed=confirmed, gap=(t[p+1]-t[p] if p+1 < len(v) else np.nan), h_last=h)
                        break
                if land: break
            t_land = land['t'] if land else np.inf
            # ---- go-arounds before the landing
            ga_times = []
            aj = ai[t[ai] <= t_land] if land else ai
            if len(aj) >= 10:
                ta = t[aj]; aa = alt[aj]; last = -1e18
                drop = np.maximum.accumulate(aa) - aa
                cand = np.nonzero((drop >= 800) & (np.maximum.accumulate(aa[::-1])[::-1] - aa >= 500))[0]
                for j in cand:
                    if j < 1 or j >= len(aj)-1: continue
                    if ta[j] - last < 240: continue
                    wloc = (ta >= ta[j]-90) & (ta <= ta[j]+90)
                    if aa[j] > aa[wloc].min(): continue
                    wpre = (ta >= ta[j]-300) & (ta <= ta[j]); wpost = (ta >= ta[j]) & (ta <= ta[j]+180)
                    if aa[wpre].max() < aa[j]+800 or aa[wpost].max() < aa[j]+500: continue
                    Q = qnh_at(ta[j])
                    if not np.isfinite(Q): continue
                    corr = qnh_corr(Q)
                    if aa[j] + corr - apt_elev >= 3000: continue
                    if (gr[(t >= ta[j]-120) & (t <= ta[j]+120)]).any(): continue
                    seg = (ta >= ta[j]-120) & (ta <= ta[j]+180)
                    if np.diff(ta[seg]).max(initial=0) > 60: continue
                    p = aj[j]
                    if not (gs[p] > 80): continue
                    best = None; bc = 1e9
                    for k, e in enumerate(E):
                        dd, cc = rel(e, X[p], Y[p])
                        if -1.5*NM <= dd <= 6*NM and abs(cc) <= 0.5*NM and np.isfinite(trk[p]) and abs(angdiff(trk[p], e['course'])) <= 30 and abs(cc) < bc:
                            best = k; bc = abs(cc)
                    if best is None: continue
                    rec = dict(base, k=best, rwy=E[best]['rwy'], outcome='ga', t_end=float(ta[j]), callsign=v.callsign.iloc[p], qnh=Q, confirmed=True, x_end=float(bc))
                    gates(v, E[best], ta[j], corr, rec); out.append(rec); last = ta[j]; ga_times.append(ta[j])
            if land:
                e = E[land['k']]
                rec = dict(base, k=land['k'], rwy=e['rwy'], outcome='land', t_end=float(land['t']), callsign=v.callsign.iloc[land['p']], qnh=qnh_at(land['t']),
                           confirmed=land['confirmed'], td_gap=land['gap'], h_last=land['h_last'])
                vv = v if not ga_times else v[v.t.values > max(ga_times)]
                gates(vv, e, land['t'], land['corr'], rec); out.append(rec)
    # ---- in-trail spacing: for each landing, distance from the threshold of the next aircraft to land on the same
    #      runway (within 400 s) at the moment the leader was last seen airborne
    tracks = {}
    lands = sorted([r for r in out if r['outcome'] == 'land'], key=lambda r: (r['k'], r['t_end']))
    for a, b in zip(lands[:-1], lands[1:]):
        if a['k'] != b['k'] or a['icao'] == b['icao']: continue
        gap = b['t_end'] - a['t_end']
        if not (0 < gap <= 400): continue
        a['gap_s'] = float(gap)
        if b['icao'] not in tracks:
            g = df[(df.icao == b['icao']) & ~df.ground]
            tracks[b['icao']] = (g.t.values, g.x.values, g.y.values)
        tt, xx, yy = tracks[b['icao']]
        i = np.searchsorted(tt, a['t_end'])
        if i == 0 or i >= len(tt) or tt[i] - tt[i-1] > 30: continue
        f = (a['t_end'] - tt[i-1]) / max(tt[i] - tt[i-1], 1e-6)
        dd, cc = rel(E[a['k']], xx[i-1] + f*(xx[i]-xx[i-1]), yy[i-1] + f*(yy[i]-yy[i-1]))
        if abs(cc) <= 1.0*NM and 0 < dd <= 15*NM: a['fol_nm'] = float(dd / NM)
    return out

if __name__ == '__main__':
    pts = pd.read_parquet(sys.argv[1])
    apinfo = pd.read_csv(sys.argv[3], usecols=['ident','latitude_deg','longitude_deg','elevation_ft']).set_index('ident')
    cands = list(pd.read_csv(sys.argv[4]).icao)
    ends = load_runways(sys.argv[2], cands)
    res = []; plat = pts.lat.values; plon = pts.lon.values
    for apt in cands:
        en = ends[ends.apt == apt]
        if len(en) == 0 or apt not in apinfo.index: continue
        la, lo = apinfo.loc[apt].latitude_deg, apinfo.loc[apt].longitude_deg
        dist = np.hypot(np.radians(plon-lo)*np.cos(np.radians(la)), np.radians(plat-la))*3440.065
        g = pts[dist < 15.0].copy()
        if len(g) < 100: continue
        el = apinfo.loc[apt].elevation_ft
        res.extend(process_airport(apt, g, en, float(el) if pd.notna(el) else 0.0))
    out = pd.DataFrame(res)
    out.to_parquet(sys.argv[5] + '.tmp', index=False)
    import os; os.replace(sys.argv[5] + '.tmp', sys.argv[5])
    print('attempts', len(out), 'airports', out.apt.nunique(), file=sys.stderr)   # no outcome split is printed (blinding)
