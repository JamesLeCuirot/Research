"""Independent rebuild of airport_day.csv from raw attempt files (all 154 days, one file at a time),
and of RA counts for a random sample of days. Does not import analysis.py."""
import glob, os, gzip, json, datetime as dt, random
import numpy as np, pandas as pd
P='/home/claude/research/papers/08-shutdown-safety-indicators/'
W='/home/claude/shutdown/'
G=pd.read_csv(P+'code/airports_study.csv')
rows=[]; rows_no1=[]; rem=dict(rep=0,repga=0,flc=0); tot=0; cs_ws=0
for f in sorted(glob.glob(W+'data/att/*.parquet')):
    day=os.path.basename(f)[:10]
    a=pd.read_parquet(f,columns=['apt','icao','cls','callsign','outcome','fol_nm'])
    tot+=len(a)
    a['isga']=(a.outcome=='ga').astype(int)
    assert set(a.outcome.unique())<= {'ga','land'}
    # rule 1
    nga=a.groupby(['apt','icao']).isga.transform('sum')
    rep=(nga>=3).values
    cs=a.callsign.fillna('').astype(str)
    cs_ws+=int((cs.str.strip().str.startswith('FLC') & ~cs.str.startswith('FLC')).sum())
    flc=cs.str.startswith('FLC').values
    rem['rep']+=int(rep.sum()); rem['repga']+=int((rep & (a.isga.values==1)).sum()); rem['flc']+=int((flc&~rep).sum())
    for keep,store in ((~(rep|flc),rows),(np.ones(len(a),bool),rows_no1)):
        b=a[keep]
        g=b.groupby('apt').agg(n=('isga','size'),ga=('isga','sum'),pairs=('fol_nm',lambda s:int(s.notna().sum())),tight=('fol_nm',lambda s:int((s<2.5).sum()))).reset_index()
        g['date']=day; store.append(g)
t=pd.concat(rows,ignore_index=True); t0=pd.concat(rows_no1,ignore_index=True)
print('total attempts',tot,'removed',rem,'FLC with leading whitespace missed:',cs_ws)
t['year']=t.date.str[:4].astype(int)
t.to_csv('rebuilt_all_airportdays_prefilter.csv',index=False); t0.to_csv('rebuilt_norule1_prefilter.csv',index=False)
t2=t[t.n>=30]
ok=t2.groupby(['apt','year']).size().unstack(fill_value=0)
print('days passing rule 2, airports failing rule 3:'); bad=ok[(ok[2024]<60)|(ok[2025]<60)]; print(bad)
miss=set(G.icao)-set(ok.index); print('airports with no airport-days at all:',miss)
keep=ok[(ok[2024]>=60)&(ok[2025]>=60)].index
print('borderline kept (min days <=65):'); print(ok.loc[keep][(ok.loc[keep].min(axis=1)<=65)])
t3=t2[t2.apt.isin(keep)].copy()
ref=pd.read_csv(P+'results/airport_day.csv')
m=t3.merge(ref,on=['date','apt'],how='outer',suffixes=('','_ref'),indicator=True)
print('merge:',m._merge.value_counts().to_dict())
for c in ['n','ga','pairs','tight']:
    print(c,'mismatching rows:',int((m[c]!=m[c+'_ref']).sum()))
# pdate check
ref['d']=pd.to_datetime(ref.date); ref['pd']=pd.to_datetime(ref.pdate)
exp=np.where(ref.year==2025,ref.d,ref.d+pd.Timedelta(days=364))
print('pdate mismatches:',int((pd.to_datetime(exp)!=ref.pd).sum()),' weekday mismatches:',int((ref.d.dt.dayofweek!=ref.pd.dt.dayofweek).sum()))
print('pdate range',ref.pd.min(),ref.pd.max(),'unique pdates',ref.pd.nunique(), 'per year dates',ref.groupby('year').date.nunique().to_dict())
print('sum n in airport_day.csv',ref.n.sum(),' by year',ref.groupby('year').n.sum().to_dict())
print('airport-days dropped by rule 2 among kept airports:',int(((t.n<30)&t.apt.isin(keep)).sum()), 'approaches in them', int(t[(t.n<30)&t.apt.isin(keep)].n.sum()))
# missing airport-days among kept (no file rows at all)
full=len(keep)*154; print('kept airport-days',len(t3),'of possible',full)
print(ok.loc[keep].describe().T)
