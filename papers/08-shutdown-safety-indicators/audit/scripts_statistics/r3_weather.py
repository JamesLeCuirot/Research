"""Weather: (a) recompute covariates from raw METAR with own code and compare to data/weather_airport_day.csv;
(b) weather-adjusted model with own IRLS + day-pair bootstrap; (c) verify supplementary.py Newton fit against statsmodels."""
import json, numpy as np, pandas as pd, statsmodels.api as sm
P='/home/claude/research/papers/08-shutdown-safety-indicators/'
R=json.load(open(P+'results/results.json')); S=json.load(open(P+'results/supplementary.json'))
G=pd.read_csv(P+'code/airports_study.csv'); ids=set(G.icao)
# (a)
parts=[]
for y in (2024,2025):
    w=pd.read_csv(f'/home/claude/shutdown/metar/metar_{y}.csv',na_values=['M'],usecols=['station','valid','gust','vsby','skyc1','skyc2','skyc3','skyc4','skyl1','skyl2','skyl3','skyl4','wxcodes'],low_memory=False)
    parts.append(w)
w=pd.concat(parts,ignore_index=True); del parts
w['apt']=np.where(w.station.isin(ids),w.station,'K'+w.station)
v=pd.to_datetime(w.valid); w['date']=v.dt.strftime('%Y-%m-%d'); w['hour']=v.dt.hour
ceil=pd.Series(np.inf,index=w.index)
for i in (1,2,3,4):
    is_c=w[f'skyc{i}'].astype(str).str.strip().isin(['BKN','OVC','VV']); l=pd.to_numeric(w[f'skyl{i}'],errors='coerce')
    ceil=np.minimum(ceil,l.where(is_c,np.inf).fillna(np.inf))
w['low']=((ceil<1000)|(pd.to_numeric(w.vsby,errors='coerce')<3)).astype(int)
w['g']=(pd.to_numeric(w.gust,errors='coerce')>=25).astype(int)
w['ts']=w.wxcodes.fillna('').str.contains('TS').astype(int)
h=w.groupby(['apt','date','hour']).low.max().reset_index().groupby(['apt','date']).agg(lowvis_share=('low','mean'),hours=('low','size')).reset_index()
b=w.groupby(['apt','date']).agg(gust25=('g','max'),ts=('ts','max')).reset_index()
mine=h.merge(b,on=['apt','date'])
ref=pd.read_csv(P+'data/weather_airport_day.csv')
m=mine.merge(ref,on=['apt','date'],how='outer',suffixes=('','_r'),indicator=True)
print('weather rows merge',m._merge.value_counts().to_dict(),' max |lowvis diff|',np.abs(m.lowvis_share-m.lowvis_share_r).max(),' gust mism',int((m.gust25!=m.gust25_r).sum()),' ts mism',int((m.ts!=m.ts_r).sum()),' hours mism',int((m.hours!=m.hours_r).sum()))
print('airport-days with <18 reporting hours:',int((ref.hours<18).sum()),' by apt:',ref[ref.hours<18].apt.value_counts().head(8).to_dict())
# data quality: vis missing share, VV/BKN with missing height, by region
w['us']=w.apt.map(G.set_index('icao').grp.isin(['US40','USOTHER']))
print('share of reports with missing vsby by US flag:',w.groupby('us').vsby.apply(lambda s:s.isna().mean()).round(4).to_dict())
print('share of reports with skyc1 missing:',w.groupby('us').skyc1.apply(lambda s:s.isna().mean()).round(4).to_dict())
print('reports per airport-day (median) by US flag:',w.groupby(['us','apt','date']).size().groupby('us').median().to_dict())
del w
# (b)
t=pd.read_csv(P+'results/airport_day.csv'); t['pd']=pd.to_datetime(t.pdate)
WX=['lowvis_share','gust25','ts']
def design(x,cov=True):
    Ad=pd.get_dummies(x.apt,dtype=float).values; y25=(x.year==2025).astype(float).values
    cols=[Ad,y25,y25*x.us.values]
    if cov: cols.append(x[WX].values.astype(float))
    return np.column_stack(cols),Ad.shape[1]+1
def irls(X,y,off,wt=None):
    wt=np.ones(len(y)) if wt is None else wt
    beta=np.zeros(X.shape[1]); beta[:]=0; 
    # start: intercept-like
    mu0=np.log((wt*y).sum()/(wt*np.exp(off)).sum()); 
    for _ in range(100):
        eta=np.clip(X@beta+off+ (mu0 if _==0 and not beta.any() else 0),-30,30); mu=np.exp(eta)
        if _==0 and not beta.any():
            # absorb start into FE columns: do one WLS step on working response
            z=(eta-off)+(y-mu)/mu
        else: z=(eta-off)+(y-mu)/mu
        W=wt*mu; XtW=X.T*W; new=np.linalg.lstsq(XtW@X,XtW@z,rcond=None)[0]
        if np.abs(new-beta).max()<1e-9: beta=new; break
        beta=new
    return beta
rng=np.random.default_rng(777)
def wxmodel(lo,hi,NB=2000,label=''):
    x=t[(t.pd>=lo)&(t.pd<=hi)].merge(ref[['apt','date']+WX],on=['apt','date'],how='left')
    miss=int(x[WX].isna().any(axis=1).sum()); x=x.dropna(subset=WX).reset_index(drop=True)
    Xa,k=design(x,True); Xu,_=design(x,False); y=x.ga.values.astype(float); off=np.log(x.n.values)
    ba=irls(Xa,y,off); bu=irls(Xu,y,off)
    smf=sm.GLM(y,Xa,family=sm.families.Poisson(),offset=off).fit()
    print(label,'rows',len(x),'missing wx',miss,' adjusted RRR own IRLS',np.exp(ba[k]),' statsmodels',np.exp(smf.params[k]),' unadjusted',np.exp(bu[k]))
    print('   covariate RRs',np.exp(ba[k+1:]).round(3),' Pearson disp',smf.pearson_chi2/smf.df_resid)
    days=sorted(x.pd.unique()); dix=x.pd.map({d:i for i,d in enumerate(days)}).values; bs=[]
    for _ in range(NB):
        wt=np.bincount(rng.integers(0,len(days),len(days)),minlength=len(days))[dix].astype(float); m=wt>0
        Xm=Xa[m]; keep=np.abs(Xm).sum(0)>0; kk=int(keep[:k].sum())
        try: bs.append(irls(Xm[:,keep],y[m],off[m],wt[m])[kk])
        except Exception: bs.append(np.nan)
    bs=np.array(bs); bs=bs[np.isfinite(bs)]
    print('   day-pair bootstrap CI',np.exp(np.percentile(bs,[2.5,97.5])).round(4),'se',bs.std(ddof=1).round(4),'n ok',len(bs))
    # interactions: does weather effect differ US vs control? (reviewer check)
    Xi=np.column_stack([Xa,x[WX].values*x.us.values[:,None]]); fi=sm.GLM(y,Xi,family=sm.families.Poisson(),offset=off).fit()
    print('   with weather x US interactions: RRR',np.exp(fi.params[k]).round(4),' lowvis RR ctl',np.exp(fi.params[k+1]).round(2),' lowvis RR US',np.exp(fi.params[k+1]+fi.params[k+4]).round(2),' gust ctl/US',np.exp(fi.params[k+2]).round(2),np.exp(fi.params[k+2]+fi.params[k+5]).round(2),' ts ctl/US',np.exp(fi.params[k+3]).round(2),np.exp(fi.params[k+3]+fi.params[k+6]).round(2))
    # weighted covariate means (approach-weighted)
    for (u,yr),g in x.groupby(['us','year']): print('   ',('US' if u else 'CTL'),yr,'unweighted',g[WX].mean().round(3).tolist(),'approach-weighted',[(g[c]*g.n).sum()/g.n.sum() for c in WX])
    return x
x=wxmodel('2025-10-01','2025-11-12',label='SHUTDOWN'); print('  json adjusted',R['weather_adjusted']['adjusted'],R['weather_adjusted']['covariate_rate_ratios'])
wxmodel('2025-09-01','2025-09-30',label='SEPTEMBER (exploratory)'); print('  json',S['exploratory']['weather_adjusted_placebo_september']['adjusted'])
# (c) supplementary 2b: Newton vs statsmodels on the real data
x=pd.concat([t[(t.pd>='2025-09-01')&(t.pd<='2025-09-30')].assign(sh=0),t[(t.pd>='2025-10-01')&(t.pd<='2025-11-12')].assign(sh=1)]).merge(ref[['apt','date']+WX],on=['apt','date']).reset_index(drop=True)
FE=pd.get_dummies(x.apt+'_'+x.sh.astype(str),dtype=float).values; y25=(x.year==2025).astype(float).values
core=np.column_stack([FE,y25,y25*x.sh,y25*x.us,y25*x.us*x.sh]); k=FE.shape[1]+3; off=np.log(x.n.values); yv=x.ga.values
def newton(X,wt=None):   # verbatim logic of supplementary.fit
    w=np.ones(len(yv)) if wt is None else wt
    m=w>0; Xm,ym,om,wm=X[m],yv[m],off[m],w[m]
    keep=np.abs(Xm).sum(0)>0; Xm=Xm[:,keep]; kk=int(keep[:k].sum())
    beta=np.zeros(Xm.shape[1]); it=0
    for it in range(60):
        mu=np.exp(np.clip(Xm@beta+om,-30,30)); g=Xm.T@(wm*(ym-mu)); H=(Xm*(wm*mu)[:,None]).T@Xm
        step=np.linalg.lstsq(H+1e-9*np.eye(len(beta)),g,rcond=None)[0]; beta=beta+np.clip(step,-5,5)
        if np.max(np.abs(step))<1e-8: break
    return float(beta[kk]),it,float(np.max(np.abs(step)))
for name,X in (('with_weather',np.column_stack([core,x[WX].values.astype(float)])),('without_weather',core)):
    b,it,st=newton(X); s=sm.GLM(yv,X,family=sm.families.Poisson(),offset=off).fit()
    print('2b',name,'rows',len(x),'Newton',np.exp(b),'iters',it+1,'last step',st,' statsmodels',np.exp(s.params[k]),' json',S['exploratory']['baseline_adjusted_'+name]['rrr'])
    # one weighted bootstrap draw
    r2=np.random.default_rng(5); days=sorted(x.pd.unique()); dix=x.pd.map({d:i for i,d in enumerate(days)}).values
    wt=np.bincount(r2.integers(0,len(days),len(days)),minlength=len(days))[dix].astype(float); m=wt>0
    b2,it2,st2=newton(X,wt); Xm=X[m]; keep=np.abs(Xm).sum(0)>0
    s2=sm.GLM(yv[m],Xm[:,keep],family=sm.families.Poisson(),offset=off[m],freq_weights=wt[m]).fit()
    print('    weighted draw: Newton',np.exp(b2),'iters',it2+1,'last step',st2,' statsmodels',np.exp(s2.params[int(keep[:k].sum())]))
