"""Stage 1: stream a day's tar from stdin; keep low-altitude points of bizjet/airline-type aircraft near study airports,
and save the day's ACAS records. Outcome-agnostic.
Usage: cat day.tar.* | python3 extract.py airports.csv airports_study.csv out.parquet acas_out.json.gz"""
import sys, os, tarfile, zlib, re, itertools
import numpy as np, pandas as pd, orjson
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from actypes import BIZJET, AIRLINE
RADIUS_NM = 15.0; ALT_MAX_AGL = 7000.0
MAX_MEMBER = 30 * 1024 * 1024      # skip compressed trace files larger than 30 MB
MAX_EXPANDED = 150 * 1024 * 1024   # skip traces that expand beyond 150 MB
ap = pd.read_csv(sys.argv[1], usecols=['ident','latitude_deg','longitude_deg','elevation_ft'])
cands = list(pd.read_csv(sys.argv[2]).icao)
ap = ap[ap.ident.isin(cands)].reset_index(drop=True)
AL = np.radians(ap.latitude_deg.values); AO = np.radians(ap.longitude_deg.values); AE = ap.elevation_ft.fillna(0).values
TYPE_RE = re.compile(rb'"t":"([A-Z0-9]+)"')
def inflate(raw):
    if raw[:2] != b'\x1f\x8b': return raw
    d = zlib.decompressobj(31); out = d.decompress(raw, MAX_EXPANDED)
    if d.unconsumed_tail: return None
    return out
def proc(raw):
    try:
        data = inflate(raw)
        if data is None: return ('BIG', len(raw))
        m = TYPE_RE.search(data[:400])
        if not m: return None
        t = m.group(1).decode()
        if t in BIZJET: cls = 'biz'
        elif t in AIRLINE: cls = 'air'
        else: return None
        d = orjson.loads(data)
        tr = d.get('trace') or []
        if len(tr) < 20: return None
        base = d['timestamp']; rows = []; cs = None
        n = len(tr)
        lat = np.fromiter((p[1] for p in tr), float, n); lon = np.fromiter((p[2] for p in tr), float, n)
        alt = np.fromiter(((-1e4 if p[3]=='ground' else (np.nan if p[3] is None else p[3])) for p in tr), float, n)
        la = np.radians(lat)[:,None]; lo = np.radians(lon)[:,None]
        dx = (lo-AO[None,:])*np.cos((la+AL[None,:])/2); dy = la-AL[None,:]
        dist = np.hypot(dx,dy)*3440.065
        j = dist.argmin(1); dmin = dist[np.arange(n), j]
        gsv = np.fromiter(((np.nan if p[4] is None else p[4]) for p in tr), float, n)
        keep = (dmin < RADIUS_NM) & (alt < AE[j]+ALT_MAX_AGL) & ~((alt < -9e3) & (gsv < 30))
        css = [None]*n
        for i,p in enumerate(tr):
            a = p[8] if len(p) > 8 else None
            if a and a.get('flight'): cs = a['flight'].strip()
            css[i] = cs
        if not keep.any(): return None
        for i in np.nonzero(keep)[0]:
            p = tr[i]; a = p[8] if len(p) > 8 else None
            rows.append((d['icao'], d.get('r'), t, cls, css[i], base+p[0], p[1], p[2],
                         (np.nan if p[3]=='ground' or p[3] is None else p[3]), p[3]=='ground', p[4], p[5], p[6], p[7],
                         p[9] if len(p)>9 else None, p[10] if len(p)>10 else None, p[12] if len(p)>12 else None,
                         (a.get('nav_qnh') if a else None)))
        return rows
    except Exception as e:
        return ('ERR', repr(e))
STAT = dict(big=0, acas=0)
def gen():
    f = tarfile.open(fileobj=sys.stdin.buffer, mode='r|')
    for m in f:
        if not m.isfile(): continue
        if 'trace_full' in m.name:
            if m.size > MAX_MEMBER: STAT['big'] += 1; continue
            yield f.extractfile(m).read()
        elif m.name.endswith('acas/acas.json.gz') and m.size < 200*1024*1024:
            open(sys.argv[4], 'wb').write(f.extractfile(m).read()); STAT['acas'] += 1
if __name__ == '__main__':
    parts = []; buf = []; nerr = 0; nfiles = 0
    cols = ['icao','reg','actype','cls','callsign','t','lat','lon','alt','ground','gs','track','flags','vrate','src','geom_alt','ias','qnh']
    def flush():
        global buf
        if buf:
            df = pd.DataFrame(buf, columns=cols)
            for c in ['gs','track','vrate','geom_alt','ias','flags','qnh']: df[c] = pd.to_numeric(df[c], errors='coerce')
            for c in ['icao','reg','actype','cls','callsign','src']: df[c] = df[c].astype('category')
            parts.append(df); buf = []
    with Pool(2) as pool:
        g = gen()
        while True:
            batch = list(itertools.islice(g, 400))
            if not batch: break
            for r in pool.map(proc, batch, chunksize=50):
                nfiles += 1
                if r is None: continue
                if isinstance(r, tuple) and r[0]=='ERR': nerr += 1; continue
                if isinstance(r, tuple) and r[0]=='BIG': STAT['big'] += 1; continue
                buf.extend(r)
            if len(buf) > 300000: flush()
    flush()
    for p in parts:
        for c in ['icao','reg','actype','cls','callsign','src']: p[c] = p[c].astype(object)
    df = pd.concat(parts, ignore_index=True)
    df.to_parquet(sys.argv[3] + '.tmp', index=False); os.replace(sys.argv[3] + '.tmp', sys.argv[3])
    print('files', nfiles, 'errors', nerr, 'oversize_skipped', STAT['big'], 'acas_saved', STAT['acas'], 'rows', len(df), 'aircraft', df.icao.nunique(), file=sys.stderr)
    if nfiles < 20000: sys.exit(3)   # a truncated archive must not be accepted as a full day
