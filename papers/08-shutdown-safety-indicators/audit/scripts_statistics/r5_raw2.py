"""Raw-file checks: RA rebuild on random sample days (own implementation), airline-only and median follower distance from raw attempts,
retried days sanity, misc number checks."""
import glob, os, gzip, json, random, sys, numpy as np, pandas as pd
exec(open('common.py').read())
R=json.load(open(P+'results/results.json')); S=json.load(open(P+'results/supplementary.json'))
Wd='/home/claude/shutdown/'
sys.path.insert(0,P+'code'); from actypes import BIZJET, AIRLINE   # fixed type lists only (not analysis code)
G=pd.read_csv(P+'code/airports_study.csv'); ap=pd.read_csv(Wd+'ref/airports.csv',usecols=['ident','latitude_deg','longitude_deg','elevation_ft']); ap=ap[ap.ident.isin(G.icao)].reset_index(drop=True)
print('study airports found in reference file:',len(ap))
ref=pd.read_csv(P+'results/airport_day.csv')
random.seed(4242); days=random.sample(sorted(ref.date.unique()),8); print('RA sample days:',days)
def hav(lat1,lon1,lat2,lon2):
    p1,p2=np.radians(lat1),np.radians(lat2); a=np.sin((p2-p1)/2)**2+np.cos(p1)*np.cos(p2)*np.sin(np.radians(lon2-lon1)/2)**2; return 2*3440.065*np.arcsin(np.sqrt(a))
tot_m=0; tot_r=0; bad=0; alt_m=0; nopos=0; nev=0; near_excl=0
for day in days:
    recs=[]
    for line in gzip.open(Wd+f'data/acas/{day}.json.gz','rt',errors='replace'):
        line=line.strip().rstrip(',')
        if not line.startswith('{'): continue
        try: x=json.loads(line)
        except Exception: continue
        r=x.get('acas_ra') or {}
        if r.get('unix_timestamp') is None or x.get('hex') is None: continue
        recs.append((x['hex'],r['unix_timestamp'],x.get('lat'),x.get('lon'),x.get('alt_baro'),x.get('t'),r.get('advisory') or ''))
    e=pd.DataFrame(recs,columns=['hex','ts','lat','lon','alt','typ','adv'])
    e['order']=np.arange(len(e)); e['prev']=e.groupby('hex').ts.shift(1)   # file order, as in the registered definition "first after >=120 s without one"
    ev=e[e.prev.isna()|(e.ts-e.prev>120)].copy(); nev+=len(ev); nopos+=int(ev.lat.isna().sum())
    ev=ev.dropna(subset=['lat','lon']); ev['altn']=pd.to_numeric(ev.alt,errors='coerce')
    d=hav(ev.lat.values[:,None],ev.lon.values[:,None],ap.latitude_deg.values[None,:],ap.longitude_deg.values[None,:]); j=d.argmin(1)
    ev['apt']=ap.ident.values[j]; ev['dmin']=d[np.arange(len(ev)),j]; ev['agl']=ev.altn-ap.elevation_ft.fillna(0).values[j]
    ok=ev[(ev.dmin<15)&(ev.agl<7000)&ev.typ.isin(BIZJET|AIRLINE)]
    mine=ok.groupby('apt').agg(ra=('adv','size'),ra_nococ=('adv',lambda s:int((~s.str.contains('Clear of Conflict')).sum())))
    rr=ref[ref.date==day].set_index('apt')[['ra','ra_nococ']]
    c=rr.join(mine,rsuffix='_m').fillna(0); tot_m+=c.ra_m.sum(); tot_r+=c.ra.sum(); bad+=int((c.ra!=c.ra_m).sum()+(c.ra_nococ!=c.ra_nococ_m).sum())
    # is the time order monotone in file? unsorted file would break the 120 s rule
    print(day,'messages',len(e),'events',len(ev),'qualifying (all study apts)',len(ok),' in table',int(c.ra.sum()),' mine',int(c.ra_m.sum()),' file time-sorted:',bool((np.diff(e.ts.values)>=0).all()),' ts<day or >day+1:',int(((pd.to_datetime(e.ts,unit='s').dt.strftime('%Y-%m-%d'))!=day).sum()))
print('RA rebuild: total mine',tot_m,'table',tot_r,'mismatching airport-day cells',bad,'; share of events with no position',round(nopos/nev,3))
# share of RA messages lacking position/type by year over all days (capture quality), cheap pass
q=[]
for f in sorted(glob.glob(Wd+'data/acas/*.json.gz'))[::7]:
    n=0;npos=0;ntyp=0
    for line in gzip.open(f,'rt',errors='replace'):
        if '"acas_ra"' not in line: continue
        n+=1; npos+=('"lat"' in line); ntyp+=('"t":"' in line)
    q.append((os.path.basename(f)[:10],n,npos/n if n else np.nan,ntyp/n if n else np.nan))
q=pd.DataFrame(q,columns=['day','msgs','pos_share','type_share']); q['year']=q.day.str[:4]; print(q.groupby('year')[['msgs','pos_share','type_share']].mean().round(3))

# attempts: airline-only, no-rule1 and medians
rows=[]; fol=[]
for f in sorted(glob.glob(Wd+'data/att/*.parquet')):
    day=os.path.basename(f)[:10]; a=pd.read_parquet(f,columns=['apt','icao','cls','callsign','outcome','fol_nm']); a['isga']=(a.outcome=='ga').astype(int)
    rep=(a.groupby(['apt','icao']).isga.transform('sum')>=3).values; flc=a.callsign.fillna('').astype(str).str.startswith('FLC').values
    b=a[~(rep|flc)]; g=b[b.cls=='air'].groupby('apt').agg(n=('isga','size'),ga=('isga','sum')).reset_index(); g['date']=day; rows.append(g)
    x=b.loc[b.fol_nm.notna(),['apt','fol_nm']]; x['date']=day; fol.append(x)
air=pd.concat(rows).merge(ref[['date','apt','us','year','pdate']],on=['date','apt']); air=air[air.n>=30]; air['pd']=pd.to_datetime(air.pdate)
s=air[(air.pd>='2025-10-01')&(air.pd<='2025-11-12')].groupby(['apt','us','year'])[['ga','n']].sum().unstack('year')
print('airline-only RRR mine',np.exp(cond_fit(s[('ga',2024)].values,s[('ga',2025)].values,s[('n',2024)].values,s[('n',2025)].values,s.index.get_level_values('us').values.astype(float))),'json',R['airline_jets_only']['rrr'], 'pooled counts',air[(air.pd>='2025-10-01')&(air.pd<='2025-11-12')].groupby(['us','year'])[['ga','n']].sum().values.tolist())
n1=pd.read_csv('rebuilt_norule1_prefilter.csv').merge(ref[['date','apt','us','year','pdate']].drop_duplicates(['date','apt']),on=['date','apt'],how='inner'); 
# note: analysis keeps no-rule-1 airport-days with n>=30 at kept airports, not only those in the table; rebuild that properly
n1=pd.read_csv('rebuilt_norule1_prefilter.csv'); n1=n1[n1.apt.isin(ref.apt.unique())&(n1.n>=30)]; n1['year']=n1.date.str[:4].astype(int); n1['pd']=pd.to_datetime(n1.date)+pd.to_timedelta(np.where(n1.year==2024,364,0),unit='D'); n1['us']=n1.apt.map(ref.groupby('apt').us.first())
s=n1[(n1.pd>='2025-10-01')&(n1.pd<='2025-11-12')].groupby(['apt','us','year'])[['ga','n']].sum().unstack('year')
print('without rule 1 RRR mine',np.exp(cond_fit(s[('ga',2024)].values.astype(float),s[('ga',2025)].values.astype(float),s[('n',2024)].values.astype(float),s[('n',2025)].values.astype(float),s.index.get_level_values('us').values.astype(float))),'json',R['without_rule1']['rrr'])
fo=pd.concat(fol).merge(ref[['date','apt','us','year','pdate']],on=['date','apt']); fo['pd']=pd.to_datetime(fo.pdate)
for wn,(a_,b_) in (('baseline',('2025-09-01','2025-09-30')),('shutdown',('2025-10-01','2025-11-12'))):
    x=fo[(fo.pd>=a_)&(fo.pd<=b_)]
    for (u,y),g in x.groupby(['us','year']):
        k=f"{wn}_{'us' if u else 'ctl'}{y}"; print('median follower',k,round(g.fol_nm.median(),4),len(g),' json',round(S['prereg_median_follower_nm'][k]['median_nm'],4),S['prereg_median_follower_nm'][k]['pairs'])
del fo
# retried (out-of-memory) days: compare to same weekday a week before/after
dn=ref.groupby('date')[['n','ga','pairs','ra']].sum()
for d_ in ['2025-09-12','2025-09-28','2025-10-16','2025-10-21','2025-11-15','2025-11-16']:
    i=dn.index.get_loc(d_); nb=[dn.index[i-7] if i>=7 else None, dn.index[i+7] if i+7<len(dn) and dn.index[i+7][:4]=='2025' else None]
    print('retried day',d_,dn.loc[d_].tolist(),' airports',int((ref.date==d_).sum()),' neighbours +-7d:',[dn.loc[x].tolist() if x else None for x in nb])
print('airport-days per date: min',ref.groupby('date').apt.nunique().min(),ref.groupby('date').apt.nunique().idxmin(),' daily n by year (mean):',ref.groupby(['year','date']).n.sum().groupby('year').mean().round(0).to_dict())
# misc paper numbers
pa=pd.DataFrame(R['per_airport']).set_index('apt'); print(pa.loc[['KDCA','KLGA','KBNA','LSZH'],['ga24','ga25','n24','n25','rr','rr_lo','rr_hi']].round(3))
print('n ratio BNA',pa.loc['KBNA'].n25/pa.loc['KBNA'].n24,'ZRH',pa.loc['LSZH'].n25/pa.loc['LSZH'].n24)
for wn in ('baseline','phaseA','phaseB'):
    m=WIN[wn]; print(wn,{g:round(C['n'][GRP==g][:,m,1].sum()/C['n'][GRP==g][:,m,0].sum(),4) for g in ('US40','USOTHER','CA','EU')})
Ks=C['tight'][:,WIN['shutdown'],:].sum(1); Ns=C['pairs'][:,WIN['shutdown'],:].sum(1); rr=(Ks[:,1]/Ns[:,1])/(Ks[:,0]/Ns[:,0]); sel=(Ks[:,0]>20)&(Ks[:,1]>20)
print('median US airport tight-share ratio (k>20 both years):',np.median(rr[sel&(US==1)]),'n',int((sel&(US==1)).sum()),' ; all 50 US airports w/o filter:',np.nanmedian(rr[US==1]))
