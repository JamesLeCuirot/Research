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

