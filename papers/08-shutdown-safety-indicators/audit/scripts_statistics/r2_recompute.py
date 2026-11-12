"""Independent recomputation from results/airport_day.csv. Does NOT import analysis.py."""
import json, numpy as np, pandas as pd, datetime as dt
from scipy import stats
P='/home/claude/research/papers/08-shutdown-safety-indicators/'
R=json.load(open(P+'results/results.json')); S=json.load(open(P+'results/supplementary.json'))
t=pd.read_csv(P+'results/airport_day.csv'); t['pd']=pd.to_datetime(t.pdate)
apts=sorted(t.apt.unique()); days=sorted(t.pd.unique()); ai={a:i for i,a in enumerate(apts)}; di={d:i for i,d in enumerate(days)}
A,D=len(apts),len(days)
info=t.groupby('apt')[['us','grp']].first().loc[apts]; US=info.us.values.astype(float); GRP=info.grp.values
def cube(col):
    X=np.zeros((A,D,2)); X[t.apt.map(ai).values,t.pd.map(di).values,(t.year.values==2025).astype(int)]=t[col].values; return X
C={c:cube(c) for c in ['n','ga','pairs','tight','ra','ra_nococ']}
dd=pd.DatetimeIndex(days)
def win(a,b): return np.array((dd>=a)&(dd<=b))
WIN=dict(baseline=win('2025-09-01','2025-09-30'),shutdown=win('2025-10-01','2025-11-12'),phaseA=win('2025-10-01','2025-11-06'),
         phaseB=win('2025-11-07','2025-11-16'),peak=win('2025-10-31','2025-11-09'))
print('days per window',{k:int(v.sum()) for k,v in WIN.items()})

def cond_fit(k24,k25,n24,n25,tr):
    """own Newton for conditional binomial: k25|tot ~ Bin(p), logit p = log(n25/n24)+b+d*tr. returns d"""
    m=(k24+k25>0)&(n24>0)&(n25>0); k24,k25,n24,n25,tr=k24[m],k25[m],n24[m],n25[m],tr[m]
    if len(np.unique(tr))<2: return np.nan
    off=np.log(n25/n24); tot=k24+k25; X=np.column_stack([np.ones(len(tr)),tr]); beta=np.zeros(2)
    for _ in range(50):
        p=1/(1+np.exp(-(off+X@beta))); g=X.T@(k25-tot*p); H=(X*(tot*p*(1-p))[:,None]).T@X
        step=np.linalg.solve(H,g); beta+=step
        if np.abs(step).max()<1e-11: break
    return beta[1]
def stat(num,den,w,tr=US,sel=None):
    """w: weights over days (D,), sel: airport mask"""
    K=np.tensordot(C[num],w,axes=([1],[0])); N=np.tensordot(C[den],w,axes=([1],[0]))
    if sel is not None: K,N,tr=K[sel],N[sel],tr[sel]
    return cond_fit(K[:,0],K[:,1],N[:,0],N[:,1],tr)
rng=np.random.default_rng(12345); NB=2000
def boot_w(mask,rng):
    idx=np.nonzero(mask)[0]; return np.bincount(rng.choice(idx,len(idx)),minlength=D).astype(float)
def pct(b):
    b=np.asarray(b); b=b[np.isfinite(b)]; return np.exp(np.percentile(b,2.5)),np.exp(np.percentile(b,97.5)),b.std(ddof=1)
def day_block(num,den,wname,tr=US,sel=None):
    m=WIN[wname].astype(float); e=stat(num,den,m,tr,sel)
    b=[stat(num,den,boot_w(WIN[wname],rng),tr,sel) for _ in range(NB)]
    lo,hi,se=pct(b); return np.exp(e),lo,hi,se
def apt_boot(fn,tr=US,sel=None):
    """fn(K-array weights per airport)->stat. resample airports within group"""
    idx=np.arange(A) if sel is None else np.nonzero(sel)[0]
    g0=idx[tr[idx]==0]; g1=idx[tr[idx]==1]; out=[]
    for _ in range(NB):
        pick=np.r_[rng.choice(g0,len(g0)),rng.choice(g1,len(g1))]; out.append(fn(pick))
    return pct(out)
def cmp(name,mine,ref):
    mine=np.array(mine,float); ref=np.array(ref,float)
    print(f'{name:38s} mine {np.round(mine,4)}  json {np.round(ref,4)}  maxabsdiff {np.abs(mine-ref).max():.4f}')

print('\n=== Table 1 pooled counts ===')
for wn in ('shutdown','baseline'):
    m=WIN[wn]
    for u,lab in ((1,'us'),(0,'ctl')):
        for y in (0,1):
            k=C['ga'][US==u][:,m,y].sum(); n=C['n'][US==u][:,m,y].sum()
            key='primary' if wn=='shutdown' else 'placebo_september'
            ref=R[key]['counts'][f'{lab}{2024+y}']
            print(wn,lab,2024+y,int(k),int(n),round(1000*k/n,3),'json',ref,'OK' if [int(k),int(n)]==ref else 'MISMATCH')

print('\n=== Go-around RRRs (est, day lo, day hi, se_log) ===')
res={}
for wn,key in (('shutdown','primary'),('baseline','placebo_september'),('phaseA','phaseA'),('phaseB','phaseB'),('peak','peak')):
    r=day_block('ga','n',wn); res[key]=r; cmp(key,r,[R[key]['rrr'],*R[key]['ci_day'],R[key]['se_log_day']])
print('primary MDE exp(2.8se)-1 mine',np.exp(2.8*res['primary'][3])-1,'json',R['primary']['mde_rel'], ' downward 1-exp(-2.8se)=',1-np.exp(-2.8*res['primary'][3]))
# statsmodels airport-day FE Poisson check of equivalence
import statsmodels.api as sm
x=t[(t.pd>='2025-10-01')&(t.pd<='2025-11-12')].reset_index(drop=True)
Xd=pd.get_dummies(x.apt,dtype=float); y25=(x.year==2025).astype(float)
X=np.column_stack([Xd.values,y25,y25*x.us]); fit=sm.GLM(x.ga.values,X,family=sm.families.Poisson(),offset=np.log(x.n.values)).fit()
print('airport-day FE Poisson (statsmodels) RRR',np.exp(fit.params[-1]),' model-based SE',fit.bse[-1],' Pearson chi2/df',fit.pearson_chi2/fit.df_resid)
fitc=sm.GLM(x.ga.values,X,family=sm.families.Poisson(),offset=np.log(x.n.values)).fit(cov_type='cluster',cov_kwds={'groups':x.pd.map(di).values})
print('  cluster-robust SE by day-pair',fitc.bse[-1])
fita=sm.GLM(x.ga.values,X,family=sm.families.Poisson(),offset=np.log(x.n.values)).fit(cov_type='cluster',cov_kwds={'groups':x.apt.map(ai).values})
print('  cluster-robust SE by airport',fita.bse[-1])
# airport bootstrap, primary and placebo
for wn,key in (('shutdown','primary'),('baseline','placebo_september')):
    K=C['ga'][:,WIN[wn],:].sum(1); N=C['n'][:,WIN[wn],:].sum(1)
    r=apt_boot(lambda p: cond_fit(K[p,0],K[p,1],N[p,0],N[p,1],US[p])); cmp(key+' airport boot',r,[*R[key]['ci_airport'],R[key]['se_log_airport']])
# baseline-adjusted, stratified
def adj_stat(num,den,wb,ws,sel=None): return stat(num,den,ws,sel=sel)-stat(num,den,wb,sel=sel)
for num,den,key in (('ga','n','baseline_adjusted'),('tight','pairs','spacing_baseline_adjusted')):
    e=adj_stat(num,den,WIN['baseline'].astype(float),WIN['shutdown'].astype(float))
    b=[adj_stat(num,den,boot_w(WIN['baseline'],rng),boot_w(WIN['shutdown'],rng)) for _ in range(NB)]
    lo,hi,se=pct(b); cmp(key,[np.exp(e),lo,hi,se],[R[key]['rrr'],*R[key]['ci_day'],R[key]['se_log_day']])
    if key=='baseline_adjusted': cmp('  vs supplementary without_weather',[np.exp(e),lo,hi,se],[S['exploratory']['baseline_adjusted_without_weather'][k] if k!='ci' else 0 for k in ('rrr',)]+S['exploratory']['baseline_adjusted_without_weather']['ci_day']+[S['exploratory']['baseline_adjusted_without_weather']['se_log_day']])
    # airport bootstrap for the adjusted estimate (NOT in the paper)
    Kb=C[num][:,WIN['baseline'],:].sum(1); Nb=C[den][:,WIN['baseline'],:].sum(1); Ks=C[num][:,WIN['shutdown'],:].sum(1); Ns=C[den][:,WIN['shutdown'],:].sum(1)
    r=apt_boot(lambda p: cond_fit(Ks[p,0],Ks[p,1],Ns[p,0],Ns[p,1],US[p])-cond_fit(Kb[p,0],Kb[p,1],Nb[p,0],Nb[p,1],US[p]))
    print(f'   {key} AIRPORT bootstrap (reviewer): {r[0]:.3f} to {r[1]:.3f} se {r[2]:.3f}')
# groups
ctl=US==0
for g,key in (('US40','group_US40'),('USOTHER','group_USOTHER')):
    r=day_block('ga','n','shutdown',sel=ctl|(GRP==g)); cmp(key,r,[R[key]['rrr'],*R[key]['ci_day'],R[key]['se_log_day']])
for g,key in (('EU','control_europe_only'),('CA','control_canada_only')):
    r=day_block('ga','n','shutdown',sel=(US==1)|(GRP==g)); cmp(key,r,[R[key]['rrr'],*R[key]['ci_day'],R[key]['se_log_day']])
r=day_block('ga','n','phaseB',tr=(GRP=='US40').astype(float),sel=US==1); cmp('phaseB US40 vs USOTHER',r[:3],[R['phaseB_US40_vs_USOTHER']['rrr'],*R['phaseB_US40_vs_USOTHER']['ci_day']])
# LOO
m=WIN['shutdown'].astype(float); loo={a:np.exp(stat('ga','n',m,sel=np.arange(A)!=i)) for i,a in enumerate(apts)}
print('LOO primary min/max',min(loo.values()),min(loo,key=loo.get),max(loo.values()),max(loo,key=loo.get),'json',R['leave_one_out'])
mb=WIN['baseline'].astype(float); loo={a:np.exp(stat('ga','n',mb,sel=np.arange(A)!=i)) for i,a in enumerate(apts)}
print('LOO PLACEBO min/max',min(loo.values()),min(loo,key=loo.get),max(loo.values()),max(loo,key=loo.get))

print('\n=== Spacing ===')
for wn,key in (('shutdown','spacing_shutdown'),('baseline','spacing_placebo')):
    r=day_block('tight','pairs',wn); cmp(key,r,[R[key]['rrr'],*R[key]['ci_day'],R[key]['se_log_day']])
    for u,lab in ((1,'us'),(0,'ctl')):
        print('   ',lab,[round(100*C['tight'][US==u][:,WIN[wn],y].sum()/C['pairs'][US==u][:,WIN[wn],y].sum(),3) for y in (0,1)],[int(C['pairs'][US==u][:,WIN[wn],y].sum()) for y in (0,1)])
K=C['tight'][:,WIN['shutdown'],:].sum(1); N=C['pairs'][:,WIN['shutdown'],:].sum(1)
r=apt_boot(lambda p: cond_fit(K[p,0],K[p,1],N[p,0],N[p,1],US[p])); cmp('spacing airport boot',r,[*R['spacing_shutdown']['ci_airport'],R['spacing_shutdown']['se_log_airport']])
print('   share of landings with a measured pair (pairs/n), shutdown: US24,US25,CTL24,CTL25',[round(C['pairs'][US==u][:,WIN['shutdown'],y].sum()/C['n'][US==u][:,WIN['shutdown'],y].sum(),3) for u in (1,0) for y in (0,1)])
print('   same, baseline:',[round(C['pairs'][US==u][:,WIN['baseline'],y].sum()/C['n'][US==u][:,WIN['baseline'],y].sum(),3) for u in (1,0) for y in (0,1)])

print('\n=== RA ===')
def ra_stat(col,wb,ws,sel=None):
    s=(US==1) if sel is None else sel&(US==1)
    f=lambda w,y:(C[col][s][:,:,y]@w).sum()/(C['n'][s][:,:,y]@w).sum()
    return np.log((f(ws,1)/f(wb,1))/(f(ws,0)/f(wb,0)))
for col,key,sel in (('ra','ra_main',None),('ra','ra_excl_DCA_BUR',~np.isin(apts,['KDCA','KBUR'])),('ra_nococ','ra_excl_clear_of_conflict',None)):
    e=ra_stat(col,WIN['baseline'].astype(float),WIN['shutdown'].astype(float),sel)
    b=[ra_stat(col,boot_w(WIN['baseline'],rng),boot_w(WIN['shutdown'],rng),sel) for _ in range(NB)]
    lo,hi,se=pct(b); cmp(key,[np.exp(e),lo,hi,se],[R[key]['ratio'],*R[key]['ci_day'],R[key]['se_log_day']])
    if key=='ra_main': se_ra=se; e_ra=e
for wn in ('phaseA','phaseB'):
    e=ra_stat('ra',WIN['baseline'].astype(float),WIN[wn].astype(float)); b=[ra_stat('ra',boot_w(WIN['baseline'],rng),boot_w(WIN[wn],rng)) for _ in range(NB)]
    lo,hi,se=pct(b); cmp('ra_'+wn,[np.exp(e),lo,hi],[S['exploratory']['ra_'+wn]['ratio'],*S['exploratory']['ra_'+wn]['ci_day']])
# RA airport concentration and airport bootstrap
us=US==1
rab=[C['ra'][us][:,WIN[w],y].sum(1) for w in ('baseline','shutdown') for y in (0,1)]
tab=pd.DataFrame(dict(apt=np.array(apts)[us],b24=rab[0],b25=rab[1],s24=rab[2],s25=rab[3])).sort_values('s24',ascending=False)
print(tab.head(12).to_string()); print('share of all US RA events in top 5 airports (shutdown 2024):',tab.s24.head(5).sum()/tab.s24.sum())
usidx=np.nonzero(us)[0]
def ra_ap(p):
    f=lambda w,y:C['ra'][p][:,WIN[w],y].sum()/C['n'][p][:,WIN[w],y].sum()
    return np.log((f('shutdown',1)/f('baseline',1))/(f('shutdown',0)/f('baseline',0)))
b=[ra_ap(rng.choice(usidx,len(usidx))) for _ in range(NB)]; print('RA main AIRPORT bootstrap (reviewer):',pct(b))
# Holm
p2=2*(1-stats.norm.cdf(abs(np.log(R['spacing_baseline_adjusted']['rrr']))/R['spacing_baseline_adjusted']['se_log_day'])); p3=2*(1-stats.norm.cdf(abs(np.log(R['ra_main']['ratio']))/R['ra_main']['se_log_day']))
ps=sorted([p2,p3]); print('Holm: raw',p2,p3,'adjusted',min(1,2*ps[0]),min(1,max(2*ps[0],ps[1])),'json',R['holm'])
json.dump({k:list(map(float,v)) for k,v in res.items()},open('recompute_main.json','w'))
