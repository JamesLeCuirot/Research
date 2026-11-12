import gzip, json, glob, os, sys, numpy as np, pandas as pd
sys.path.insert(0,'/home/claude/research/papers/08-shutdown-safety-indicators/code')
from actypes import BIZJET, AIRLINE
G=pd.read_csv('/home/claude/research/papers/08-shutdown-safety-indicators/code/airports_study.csv')
ap=pd.read_csv('/home/claude/shutdown/ref/airports.csv',usecols=['ident','latitude_deg','longitude_deg','elevation_ft']).merge(G,left_on='ident',right_on='icao')
AL=np.radians(ap.latitude_deg.values)[None,:]; AO=np.radians(ap.longitude_deg.values)[None,:]
rows=[]; nmsg={}
for f in sorted(glob.glob('/home/claude/shutdown/data/acas/*.json.gz')):
    date=os.path.basename(f)[:10]; last={}; ev=[]; cur={}; n=0; first_t=None
    for line in gzip.open(f,'rt',errors='replace'):
        line=line.strip().rstrip(',')
        if not line.startswith('{'): continue
        try: x=json.loads(line)
        except Exception: continue
        r=x.get('acas_ra') or {}; t=r.get('unix_timestamp'); h=x.get('hex')
        if t is None or h is None: continue
        n+=1
        if first_t is None: first_t=t
        if h not in last or t-last[h]>120:
            e=dict(date=date,hex=h,t=t,lat=x.get('lat'),lon=x.get('lon'),alt=x.get('alt_baro'),typ=x.get('t'),adv=r.get('advisory'),df=r.get('df_type'),mte=r.get('MTE'),rat=r.get('RAT'),thr=r.get('threat_id_hex'),tti=r.get('TTI'),vr=x.get('baro_rate'),flight=(x.get('flight') or '').strip(),src=x.get('type'),nmsg=0,advs=set(),since0=t-first_t,cat=x.get('category'))
            ev.append(e); cur[h]=e
        last[h]=t; cur[h]['nmsg']+=1; cur[h]['advs'].add(r.get('advisory')); cur[h]['dur']=t-cur[h]['t']
    nmsg[date]=n
    for e in ev: e['advs']='|'.join(sorted(a for a in e['advs'] if a)); rows.append(e)
e=pd.DataFrame(rows); print('all events',len(e))
e['ground']=(e.alt.astype(str)=='ground'); e['alt']=pd.to_numeric(e.alt,errors='coerce'); e.to_parquet('ra_all_raw.parquet')
pd.Series(nmsg).to_csv('ra_nmsg.csv')
