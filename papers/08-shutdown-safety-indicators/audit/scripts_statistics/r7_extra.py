"""(a) weather x US interaction model with day-pair bootstrap; (b) RA with baseline restricted to days after the 26-27 Sep 2024 ACAS logging change;
(c) track-quality proxies by group and year from raw attempts; (d) which log had the error/oversize."""
import glob, os, json, numpy as np, pandas as pd, re
exec(open('common.py').read())
ref=pd.read_csv(P+'data/weather_airport_day.csv'); WX=['lowvis_share','gust25','ts']
x=t[(t.pd>='2025-10-01')&(t.pd<='2025-11-12')].merge(ref[['apt','date']+WX],on=['apt','date']).reset_index(drop=True)
Ad=pd.get_dummies(x.apt,dtype=float).values; y25=(x.year==2025).astype(float).values; k=Ad.shape[1]+1
base=np.column_stack([Ad,y25,y25*x.us.values,x[WX].values]); y=x.ga.values.astype(float); off=np.log(x.n.values)
def irls(X,y,off,wt):
    beta=np.zeros(X.shape[1]); eta=np.log((y+0.5)/np.exp(off))
    for _ in range(100):
        mu=np.exp(np.clip(eta+off,-30,30)); z=eta+(y-mu)/mu; W=wt*mu; XtW=X.T*W; new=np.linalg.lstsq(XtW@X,XtW@z,rcond=None)[0]
        eta=X@new
        if np.abs(new-beta).max()<1e-9: beta=new; break
        beta=new
    return beta
variants={'common coefficients (registered)':base,
          'weather x US':np.column_stack([base,x[WX].values*x.us.values[:,None]]),
          'weather x US and x year':np.column_stack([base,x[WX].values*x.us.values[:,None],x[WX].values*y25[:,None]]),
          'lowvis only':np.column_stack([Ad,y25,y25*x.us.values,x[['lowvis_share']].values]),
          'lowvis + lowvis^2':np.column_stack([base,x[['lowvis_share']].values**2])}
days=sorted(x.pd.unique()); dix=x.pd.map({d:i for i,d in enumerate(days)}).values; rng=np.random.default_rng(31)
Wt=[np.bincount(rng.integers(0,len(days),len(days)),minlength=len(days))[dix].astype(float) for _ in range(1000)]
for name,X in variants.items():
    e=irls(X,y,off,np.ones(len(y)))[k]; bs=[]
    for wt in Wt:
        m=wt>0; Xm=X[m]; keep=np.abs(Xm).sum(0)>0; bs.append(irls(Xm[:,keep],y[m],off[m],wt[m])[int(keep[:k].sum())])
    bs=np.array(bs); print(f'  weather model [{name}]: RRR {np.exp(e):.3f} ({np.exp(np.percentile(bs,2.5)):.3f}-{np.exp(np.percentile(bs,97.5)):.3f})')
# (b)
us=US==1
def rate(mask,y,col='ra'): return C[col][us][:,mask,y].sum()/C['n'][us][:,mask,y].sum()
late=win('2025-09-26','2025-09-30'); early=win('2025-09-01','2025-09-24'); sh=WIN['shutdown']
print('RA per 1000, US: 2024 pdates 1-24 Sep',1000*rate(early,0),' 26-30 Sep',1000*rate(late,0),' shutdown',1000*rate(sh,0)); print('               2025 pdates 1-24 Sep',1000*rate(early,1),' 26-30 Sep',1000*rate(late,1),' shutdown',1000*rate(sh,1))
print('registered ratio',(rate(sh,1)/rate(WIN['baseline'],1))/(rate(sh,0)/rate(WIN['baseline'],0)))
print('ratio with baseline = pdates 26-30 Sep (after 2024 logging change) in both years:',(rate(sh,1)/rate(late,1))/(rate(sh,0)/rate(late,0)))
print('ratio with baseline = pdates 1-24 Sep (before change):',(rate(sh,1)/rate(early,1))/(rate(sh,0)/rate(early,0)))
print('2025-only shutdown/September rate ratio:',rate(sh,1)/rate(WIN['baseline'],1))
# bootstrap for late-baseline version
def bw(mask): idx=np.nonzero(mask)[0]; return np.bincount(rng.choice(idx,len(idx)),minlength=D).astype(float)
def rs(wb,ws): f=lambda w,y:(C['ra'][us][:,:,y]@w).sum()/(C['n'][us][:,:,y]@w).sum(); return np.log((f(ws,1)/f(wb,1))/(f(ws,0)/f(wb,0)))
b=np.array([rs(bw(late),bw(sh)) for _ in range(2000)]); print('  late-baseline CI',np.exp(np.percentile(b,[2.5,97.5])).round(3))
# excluding SFO too
us2=us&~np.isin(apts,['KSFO']); f=lambda mask,y:C['ra'][us2][:,mask,y].sum()/C['n'][us2][:,mask,y].sum(); print('  late-baseline, excluding SFO:',(f(sh,1)/f(late,1))/(f(sh,0)/f(late,0)))
# (c)
rows=[]
for fn in sorted(glob.glob('/home/claude/shutdown/data/att/*.parquet'))[::3]:
    a=pd.read_parquet(fn,columns=['apt','outcome','confirmed','td_gap','ok1000','ok500','fol_nm','gap_s']); a['date']=os.path.basename(fn)[:10]
    l=a[a.outcome=='land']; g=l.groupby('apt').agg(n=('confirmed','size'),conf=('confirmed','sum'),ok1000=('ok1000',lambda s:int((s==True).sum())),ok500=('ok500',lambda s:int((s==True).sum())),gap=('gap_s',lambda s:int(s.notna().sum())),fol=('fol_nm',lambda s:int(s.notna().sum()))).reset_index(); g['date']=a.date.iloc[0]; rows.append(g)
q=pd.concat(rows).merge(t[['date','apt','us','year']],on=['date','apt']); s=q.groupby(['us','year'])[['n','conf','ok1000','ok500','gap','fol']].sum()
print((s.div(s.n,axis=0)).round(3)); print('share of same-runway pairs within 400 s that got a distance (fol/gap):',(s.fol/s.gap).round(3).to_dict())
for f in glob.glob('/home/claude/shutdown/logs/20*.log'):
    txt=open(f).read()
    for m in re.finditer(r'errors (\d+) oversize_skipped (\d+)',txt):
        if m.group(1)!='0' or m.group(2)!='0': print('log',os.path.basename(f),m.group(0))
