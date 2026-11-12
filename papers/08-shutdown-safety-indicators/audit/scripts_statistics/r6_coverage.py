"""Archive-level coverage diagnostics: extraction log rows/aircraft per day, published archive size, ACAS message volumes per day,
and a negative-control RA series (events of study-type aircraft with a position that are NOT near any US study airport)."""
import glob, os, re, gzip, json, sys, numpy as np, pandas as pd
P='/home/claude/research/papers/08-shutdown-safety-indicators/'; Wd='/home/claude/shutdown/'
sys.path.insert(0,P+'code'); from actypes import BIZJET, AIRLINE
rows=[]
for f in sorted(glob.glob(Wd+'logs/20*.log')):
    d=os.path.basename(f)[:10]; txt=open(f).read()
    m=re.findall(r'files (\d+) errors (\d+) oversize_skipped (\d+) acas_saved (\d+) rows (\d+) aircraft (\d+)',txt); mm=re.findall(r'published (\d+)',txt)
    if m: rows.append((d,)+tuple(map(int,m[-1]))+(int(mm[-1]) if mm else np.nan,))
L=pd.DataFrame(rows,columns=['date','files','errors','oversize','acas','rows','aircraft','mib']); L['year']=L.date.str[:4].astype(int)
L['pd']=pd.to_datetime(L.date)+pd.to_timedelta(np.where(L.year==2024,364,0),unit='D'); L['rpa']=L.rows/L.aircraft
print('days with log line:',len(L),' errors total',L.errors.sum(),' oversize skipped total',L.oversize.sum())
L['win']=np.where(L.pd<'2025-10-01','Sep',np.where(L.pd<='2025-11-12','Shutdown','post'))
print(L.groupby(['year','win'])[['files','rows','aircraft','rpa','mib']].mean().round(1))
p=L.pivot(index='pd',columns='year',values=['mib','rows','aircraft','files'])
print('archive size ratio 2025/2024: mean of daily ratios',(p[('mib',2025)]/p[('mib',2024)]).mean().round(3),' ratio of totals',(p[('mib',2025)].sum()/p[('mib',2024)].sum()).round(3))
print('extracted rows ratio 2025/2024 (points near study airports):',(p[('rows',2025)].sum()/p[('rows',2024)].sum()).round(3),' aircraft ratio',(p[('aircraft',2025)].sum()/p[('aircraft',2024)].sum()).round(3))
wk=((p.index-pd.Timestamp('2025-09-01')).days//7); print((p[('rows',2025)]/p[('rows',2024)]).groupby(wk).mean().round(2).to_dict())
print('rows per aircraft by week 2024:',(p[('rows',2024)]/p[('aircraft',2024)]).groupby(wk).mean().round(0).to_dict()); print('rows per aircraft by week 2025:',(p[('rows',2025)]/p[('aircraft',2025)]).groupby(wk).mean().round(0).to_dict())
# ACAS per day
G=pd.read_csv(P+'code/airports_study.csv'); ap=pd.read_csv(Wd+'ref/airports.csv',usecols=['ident','latitude_deg','longitude_deg','elevation_ft']); ap=ap[ap.ident.isin(G.icao)].merge(G,left_on='ident',right_on='icao')
usap=ap[ap.grp.isin(['US40','USOTHER'])]
T=BIZJET|AIRLINE; out=[]
for f in sorted(glob.glob(Wd+'data/acas/*.json.gz')):
    d=os.path.basename(f)[:10]; last={}; n=0; npos=0; ev=[]; ndf={}
    for line in gzip.open(f,'rt',errors='replace'):
        line=line.strip().rstrip(',')
        if not line.startswith('{'): continue
        try: x=json.loads(line)
        except Exception: continue
        r=x.get('acas_ra') or {}; t=r.get('unix_timestamp'); h=x.get('hex')
        if t is None or h is None: continue
        n+=1; npos+=(x.get('lat') is not None); ndf[r.get('df_type')]=ndf.get(r.get('df_type'),0)+1
        if h not in last or t-last[h]>120: ev.append((x.get('lat'),x.get('lon'),x.get('alt_baro'),x.get('t'),r.get('df_type')))
        last[h]=t
    e=pd.DataFrame(ev,columns=['lat','lon','alt','typ','df']); ne=len(e); e=e.dropna(subset=['lat','lon']); nep=len(e); e=e[e.typ.isin(T)]; nept=len(e)
    la=np.radians(e.lat.values)[:,None]; lo=np.radians(e.lon.values)[:,None]; AL=np.radians(usap.latitude_deg.values)[None,:]; AO=np.radians(usap.longitude_deg.values)[None,:]
    dd=np.hypot((lo-AO)*np.cos((la+AL)/2),la-AL)*3440.065; near=dd.min(1)<15 if len(e) else np.array([],bool)
    conus=(e.lat.between(24,50)&e.lon.between(-125,-66)).values
    out.append(dict(date=d,msgs=n,pos_share=npos/max(n,1),events=ne,events_pos=nep,events_pos_type=nept,near_us_study=int(near.sum()),conus_not_near=int((conus&~near).sum()),outside_conus=int((~conus).sum()),df17=ndf.get(17,0),df18=ndf.get(18,0),df_other=n-ndf.get(17,0)-ndf.get(18,0)))
Aq=pd.DataFrame(out); Aq['year']=Aq.date.str[:4].astype(int); Aq['pd']=pd.to_datetime(Aq.date)+pd.to_timedelta(np.where(Aq.year==2024,364,0),unit='D'); Aq.to_csv('acas_daily.csv',index=False)
Aq['win']=np.where(Aq.pd<'2025-10-01','Sep',np.where(Aq.pd<='2025-11-12','Shutdown','post'))
print(Aq.groupby(['year','win'])[['msgs','pos_share','events','events_pos','events_pos_type','near_us_study','conus_not_near','outside_conus','df17','df18','df_other']].mean().round(2).to_string())
Aq['wk']=(Aq.pd-pd.Timestamp('2025-09-01')).dt.days//7
print(Aq.groupby(['year','wk'])[['msgs','pos_share','events','events_pos_type','near_us_study','conus_not_near','outside_conus']].mean().round(1).to_string())
g=Aq[Aq.win!='post'].groupby(['year','win'])[['near_us_study','conus_not_near','outside_conus','events','events_pos_type']].mean()
for c in g.columns:
    r=(g.loc[(2025,'Shutdown'),c]/g.loc[(2025,'Sep'),c])/(g.loc[(2024,'Shutdown'),c]/g.loc[(2024,'Sep'),c]); print(f'  per-day count ratio-of-ratios (shutdown/Sep, 2025 vs 2024) for {c}: {r:.3f}   [2024 S/B {g.loc[(2024,"Shutdown"),c]/g.loc[(2024,"Sep"),c]:.3f}, 2025 S/B {g.loc[(2025,"Shutdown"),c]/g.loc[(2025,"Sep"),c]:.3f}]')
# locate step in 2024 daily messages
a4=Aq[Aq.year==2024].set_index('date'); print(a4.loc['2024-09-25':'2024-10-12',['msgs','pos_share','events','events_pos_type','near_us_study','df17','df18']].to_string())
