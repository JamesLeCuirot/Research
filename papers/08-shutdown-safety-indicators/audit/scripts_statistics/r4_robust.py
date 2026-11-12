"""Per-airport intervals, Holm, heterogeneity, overdispersion, serial correlation, coverage sensitivity, placebo anatomy."""
import json, numpy as np, pandas as pd
from scipy import stats
exec(open('common.py').read())
R=json.load(open(P+'results/results.json'))
m=WIN['shutdown']; K=C['ga'][:,m,:].sum(1); N=C['n'][:,m,:].sum(1)
print('=== per-airport exact intervals (own implementation) ===')
rows=[]
for i,a in enumerate(apts):
    k24,k25=K[i]; n24,n25=N[i]; tot=k24+k25; p0=n25/(n24+n25)
    lo=stats.beta.ppf(.025,k25,tot-k25+1) if k25>0 else 0; hi=stats.beta.ppf(.975,k25+1,tot-k25) if k25<tot else 1
    f=lambda p:p/(1-p)*n24/n25
    pv=min(1,2*min(stats.binom.cdf(k25,tot,p0),stats.binom.sf(k25-1,tot,p0)))
    rows.append(dict(apt=a,us=int(US[i]),k24=int(k24),k25=int(k25),n24=int(n24),n25=int(n25),rr=(k25/n25)/(k24/n24),lo=f(lo),hi=f(hi),p=pv,nratio=n25/n24))
pa=pd.DataFrame(rows); ref=pd.DataFrame(R['per_airport']).set_index('apt').loc[pa.apt]
print('max abs diff rr/lo/hi vs json:',np.nanmax(np.abs(pa.rr.values-ref.rr.values)),np.nanmax(np.abs(pa.lo.values-ref.rr_lo.values)),np.nanmax(np.abs(pa.hi.values-ref.rr_hi.values)))
sig=pa[(pa.lo>1)|(pa.hi<1)]; print('intervals excluding 1:',len(sig),' US',int(sig.us.sum()),' ctl',int((1-sig.us).sum()),' up',int((sig.rr>1).sum()),' down',int((sig.rr<1).sum()))
print(sig[['apt','us','k24','k25','rr','lo','hi','p','nratio']].round(3).to_string())
# Holm across 76 and across 50 US
def holm(p):
    o=np.argsort(p); adj=np.empty(len(p)); run=0
    for r,i in enumerate(o): run=max(run,(len(p)-r)*p[i]); adj[i]=min(1,run)
    return adj
pa['holm76']=holm(pa.p.values); us_=pa.us==1; pa.loc[us_,'holm50']=holm(pa.p[us_].values)
print('Holm<0.05 across 76:',pa[pa.holm76<.05].apt.tolist(),' across 50 US:',pa[pa.holm50<.05].apt.tolist())
# day-clustered per-airport intervals: bootstrap day-pairs for each airport
rng=np.random.default_rng(99); idx=np.nonzero(m)[0]; NB=2000
Wb=np.stack([np.bincount(rng.choice(idx,len(idx)),minlength=D) for _ in range(NB)]).astype(float)  # NB x D
Kb=np.einsum('ady,bd->bay',C['ga'],Wb); Nb=np.einsum('ady,bd->bay',C['n'],Wb)
with np.errstate(divide='ignore',invalid='ignore'): lr=np.log((Kb[:,:,1]/Nb[:,:,1])/(Kb[:,:,0]/Nb[:,:,0]))
lo=np.array([np.percentile(lr[:,i][np.isfinite(lr[:,i])],2.5) for i in range(A)]); hi=np.array([np.percentile(lr[:,i][np.isfinite(lr[:,i])],97.5) for i in range(A)])
pa['blo']=np.exp(lo); pa['bhi']=np.exp(hi); bs=pa[(pa.blo>1)|(pa.bhi<1)]
print('day-bootstrap per-airport intervals excluding 1:',len(bs),bs.apt.tolist())
print('ratio of day-bootstrap SE to Poisson SE per airport: median',np.median([np.nanstd(lr[:,i][np.isfinite(lr[:,i])])/np.sqrt(1/K[i,0]+1/K[i,1]) for i in range(A) if K[i].min()>0]))
# calibration of "expected by chance": split the days of one year randomly in two halves; exact interval; no true change by construction
def false_pos(y,reps=400):
    cnt=[]
    for _ in range(reps):
        perm=rng.permutation(idx); h1=perm[:len(perm)//2]; h2=perm[len(perm)//2:]
        k1=C['ga'][:,h1,y].sum(1); k2=C['ga'][:,h2,y].sum(1); n1=C['n'][:,h1,y].sum(1); n2=C['n'][:,h2,y].sum(1); tot=k1+k2; p0=n2/(n1+n2)
        pv=np.minimum(1,2*np.minimum(stats.binom.cdf(k2,tot,p0),stats.binom.sf(k2-1,tot,p0))); cnt.append((pv<0.05).sum())
    return np.mean(cnt),np.percentile(cnt,[2.5,97.5])
for y in (0,1): print(f'  null calibration, random half-split of shutdown days within {2024+y}: mean # of 76 airports "significant" at exact 5%:',false_pos(y))
# heterogeneity
def dl(sel):
    c=pa[sel&(pa.k24>0)&(pa.k25>0)]; y=np.log(c.rr); v=1/c.k24+1/c.k25; w=1/v; mu=(w*y).sum()/w.sum(); Q=(w*(y-mu)**2).sum(); k=len(c)
    return k,Q,np.sqrt(max(0,(Q-(k-1))/(w.sum()-(w**2).sum()/w.sum())))
print('DL tau US',dl(pa.us==1),' ctl',dl(pa.us==0),' json',R['heterogeneity_us']['tau'],R['heterogeneity_ctl']['tau'])
# DL with variance from day bootstrap instead of Poisson
def dl_boot(sel):
    ii=np.nonzero(sel.values&(K.min(1)>0))[0]; y=np.log(pa.rr.values[ii]); v=np.array([np.nanvar(lr[:,i][np.isfinite(lr[:,i])],ddof=1) for i in ii]); w=1/v; mu=(w*y).sum()/w.sum(); Q=(w*(y-mu)**2).sum(); k=len(ii)
    return k,Q,np.sqrt(max(0,(Q-(k-1))/(w.sum()-(w**2).sum()/w.sum()))), 1-stats.chi2.cdf(Q,k-1)
print('DL tau with day-clustered variances: US',dl_boot(pa.us==1),' ctl',dl_boot(pa.us==0))

print('\n=== coverage: detected approaches 2025/2024, shutdown window ===')
print(pa.sort_values('nratio')[['apt','us','n24','n25','nratio']].round(3).iloc[np.r_[0:8,-10:0]].to_string())
print('airports with n ratio outside 0.80-1.25:',pa[(pa.nratio<.8)|(pa.nratio>1.25)].apt.tolist())
w_s=m.astype(float); w_b=WIN['baseline'].astype(float)
for lab,sel in (('all',np.ones(A,bool)),('n ratio within 0.80-1.25',((pa.nratio>=.8)&(pa.nratio<=1.25)).values),('n ratio within 0.90-1.11',((pa.nratio>=.9)&(pa.nratio<=1.11)).values)):
    e=stat('ga','n',w_s,sel=sel); eb=stat('ga','n',w_b,sel=sel)
    b=np.array([stat('ga','n',boot_w(m,rng),sel=sel) for _ in range(1000)]); bb=np.array([stat('ga','n',boot_w(WIN['baseline'],rng),sel=sel) for _ in range(1000)])
    print(f'  {lab:28s} airports {int(sel.sum())} (US {int((sel&(US==1)).sum())}): primary {np.exp(e):.3f} ({np.exp(np.percentile(b,2.5)):.3f}-{np.exp(np.percentile(b,97.5)):.3f})  placebo {np.exp(eb):.3f} ({np.exp(np.percentile(bb,2.5)):.3f}-{np.exp(np.percentile(bb,97.5)):.3f})')
# balanced airport-day pairs only
bal=(C['n'][:,:,0]>0)&(C['n'][:,:,1]>0); print('airport-day pairs present in only one year (shutdown window):',int(((C['n'][:,:,0]>0)^(C['n'][:,:,1]>0))[:,m].sum()),' by airport:',{apts[i]:int(v) for i,v in enumerate(((C['n'][:,:,0]>0)^(C['n'][:,:,1]>0))[:,m].sum(1)) if v>0})
Cb={c:C[c]*bal[:,:,None] for c in C}; Ksb=Cb['ga'][:,m,:].sum(1); Nsb=Cb['n'][:,m,:].sum(1); print('  primary on balanced pairs only:',np.exp(cond_fit(Ksb[:,0],Ksb[:,1],Nsb[:,0],Nsb[:,1],US)))
# equal-weight estimator (mean of per-airport log RR, +0.5 correction)
l=np.log(((K[:,1]+.5)/N[:,1])/((K[:,0]+.5)/N[:,0])); print('unweighted mean per-airport log RR: US',np.exp(l[US==1].mean()),'ctl',np.exp(l[US==0].mean()),'ratio',np.exp(l[US==1].mean()-l[US==0].mean()),' medians ratio',np.exp(np.median(l[US==1])-np.median(l[US==0])))

print('\n=== serial correlation and block bootstrap ===')
def daystat(d):
    f=lambda u,y:C['ga'][US==u][:,d,y].sum()/C['n'][US==u][:,d,y].sum()
    return np.log((f(1,1)/f(1,0))/(f(0,1)/f(0,0)))
s=np.array([daystat(d) for d in range(D)]); 
for lab,mm in (('all 77 days',np.ones(D,bool)),('shutdown',m)):
    z=s[mm]-s[mm].mean(); print(f'  daily log-RRR series {lab}: lag1 autocorr {np.corrcoef(z[:-1],z[1:])[0,1]:.3f}, lag2 {np.corrcoef(z[:-2],z[2:])[0,1]:.3f}, lag7 {np.corrcoef(z[:-7],z[7:])[0,1]:.3f}')
for u in (1,0):
    for y in (0,1):
        r=np.log(C['ga'][US==u][:,:,y].sum(0)/C['n'][US==u][:,:,y].sum(0)); z=r[m]-r[m].mean(); print(f'  daily log rate {"US" if u else "CTL"} {2024+y} shutdown window: lag1 autocorr {np.corrcoef(z[:-1],z[1:])[0,1]:.3f}')
for L in (3,7):
    out=[]
    n=len(idx)
    for _ in range(2000):
        starts=rng.integers(0,n,int(np.ceil(n/L))); pick=np.concatenate([idx[(s0+np.arange(L))%n] for s0 in starts])[:n]
        out.append(stat('ga','n',np.bincount(pick,minlength=D).astype(float)))
    out=np.array(out); print(f'  circular block bootstrap, block {L} days: primary CI {np.exp(np.percentile(out,2.5)):.3f}-{np.exp(np.percentile(out,97.5)):.3f}, se {out.std(ddof=1):.4f}')
# independent-years bootstrap (2024 and 2025 days resampled separately, since pairing has no physical basis)
out=[]
for _ in range(2000):
    w0=boot_w(m,rng); w1=boot_w(m,rng); K_=np.stack([C['ga'][:,:,0]@w0,C['ga'][:,:,1]@w1],1); N_=np.stack([C['n'][:,:,0]@w0,C['n'][:,:,1]@w1],1)
    out.append(cond_fit(K_[:,0],K_[:,1],N_[:,0],N_[:,1],US))
out=np.array(out); print(f'  years resampled independently: {np.exp(np.percentile(out,2.5)):.3f}-{np.exp(np.percentile(out,97.5)):.3f} se {out.std(ddof=1):.4f}')
# US and control days resampled independently in addition (4 independent blocks)
out=[]
for _ in range(2000):
    ws=[[boot_w(m,rng) for y in (0,1)] for u in (0,1)]
    K_=np.zeros((A,2)); N_=np.zeros((A,2))
    for u in (0,1):
        for y in (0,1): K_[US==u,y]=C['ga'][US==u][:,:,y]@ws[u][y]; N_[US==u,y]=C['n'][US==u][:,:,y]@ws[u][y]
    out.append(cond_fit(K_[:,0],K_[:,1],N_[:,0],N_[:,1],US))
out=np.array(out); print(f'  four cells resampled independently: {np.exp(np.percentile(out,2.5)):.3f}-{np.exp(np.percentile(out,97.5)):.3f} se {out.std(ddof=1):.4f}')

print('\n=== anatomy of the placebo / time path of the RRR ===')
wk=(np.arange(D)//7)
for w in range(11):
    mm=wk==w; f=lambda u,y:1000*C['ga'][US==u][:,mm,y].sum()/C['n'][US==u][:,mm,y].sum()
    print(f'  week {w:2d} from {str(dd[mm][0])[:10]}: US24 {f(1,0):.2f} US25 {f(1,1):.2f} CTL24 {f(0,0):.2f} CTL25 {f(0,1):.2f}  FE-RRR {np.exp(stat("ga","n",mm.astype(float))):.3f}')
for lab,a_,b_ in (('1-14 Oct','2025-10-01','2025-10-14'),('15 Oct-12 Nov','2025-10-15','2025-11-12'),('1-21 Oct','2025-10-01','2025-10-21'),('22 Oct-12 Nov','2025-10-22','2025-11-12')):
    mm=win(a_,b_); e=stat('ga','n',mm.astype(float)); b=np.array([stat('ga','n',boot_w(mm,rng)) for _ in range(2000)])
    print(f'  {lab}: RRR {np.exp(e):.3f} ({np.exp(np.percentile(b,2.5)):.3f}-{np.exp(np.percentile(b,97.5)):.3f})')
# hurricane Helene: 2024-09-25..28 -> pdate 2025-09-24..27; Milton 2024-10-08..10 -> pdate 2025-10-07..09
SE=np.isin(apts,['KATL','KCLT','KTPA','KMCO','KMIA','KFLL','KJAX','KRDU','KBNA','KMSY'])
for lab,mm,sel in (('placebo without pdates 24-28 Sep (Helene)',WIN['baseline']&~win('2025-09-24','2025-09-28'),None),('placebo without SE-US airports',WIN['baseline'],~SE),
                   ('primary without pdates 7-10 Oct (Milton)',m&~win('2025-10-07','2025-10-10'),None),('primary without Florida airports',m,~np.isin(apts,['KTPA','KMCO','KMIA','KFLL']))):
    e=stat('ga','n',mm.astype(float),sel=sel); b=np.array([stat('ga','n',boot_w(mm,rng),sel=sel) for _ in range(1000)])
    print(f'  {lab}: {np.exp(e):.3f} ({np.exp(np.percentile(b,2.5)):.3f}-{np.exp(np.percentile(b,97.5)):.3f})')
# which US airports drive Sept 2024 excess: per-airport Sept RR
Kb=C['ga'][:,WIN['baseline'],:].sum(1); Nb=C['n'][:,WIN['baseline'],:].sum(1)
pb=pd.DataFrame(dict(apt=apts,us=US,k24=Kb[:,0],k25=Kb[:,1],r24=1000*Kb[:,0]/Nb[:,0],r25=1000*Kb[:,1]/Nb[:,1])); pb['excess24']=pb.k24-pb.k25*Nb[:,0]/Nb[:,1]
print(pb[pb.us==1].sort_values('excess24',ascending=False).head(10).round(2).to_string()); print('US airports with Sept rate lower in 2025 than 2024:',int(((pb.r25<pb.r24)&(pb.us==1)).sum()),'of 50; controls:',int(((pb.r25<pb.r24)&(pb.us==0)).sum()),'of 26')
# worst days in US 2024 september
r=pd.Series(1000*C['ga'][US==1][:,:,0].sum(0)/C['n'][US==1][:,:,0].sum(0),index=dd); print('US 2024 top days by rate (pdate):',r.sort_values(ascending=False).head(8).round(1).to_dict())
r5=pd.Series(1000*C['ga'][US==1][:,:,1].sum(0)/C['n'][US==1][:,:,1].sum(0),index=dd); print('US 2025 top days:',r5.sort_values(ascending=False).head(5).round(1).to_dict())
print('US median daily rate: Sep24',r[WIN['baseline']].median().round(2),'Sep25',r5[WIN['baseline']].median().round(2),'Shut24',r[m].median().round(2),'Shut25',r5[m].median().round(2))
# RA leave-one-out
print('\n=== RA leave-one-airport-out ===')
def ra(sel):
    f=lambda w,y:C['ra'][sel][:,WIN[w],y].sum()/C['n'][sel][:,WIN[w],y].sum()
    return (f('shutdown',1)/f('baseline',1))/(f('shutdown',0)/f('baseline',0))
us=US==1; l={a:ra(us&(np.arange(A)!=i)) for i,a in enumerate(apts) if us[i]}
print('  LOO range',min(l.values()),min(l,key=l.get),max(l.values()),max(l,key=l.get))
for ex in (['KSFO'],['KSFO','KBUR','KDCA'],['KSFO','KBUR','KDCA','KPHX']):
    sel=us&~np.isin(apts,ex)
    def rs(wb,ws):
        f=lambda w,y:(C['ra'][sel][:,:,y]@w).sum()/(C['n'][sel][:,:,y]@w).sum(); return np.log((f(ws,1)/f(wb,1))/(f(ws,0)/f(wb,0)))
    b=np.array([rs(boot_w(WIN['baseline'],rng),boot_w(m,rng)) for _ in range(2000)]); print(f'  excluding {ex}: {ra(sel):.3f} ({np.exp(np.percentile(b,2.5)):.3f}-{np.exp(np.percentile(b,97.5)):.3f})')
print('  SFO alone:',ra(np.isin(apts,['KSFO'])),' RA zero-event airport-days share US:',(C['ra'][us]==0).mean())
# spacing LOO and by airport
print('\n=== spacing: leave-one-out of baseline-adjusted and shutdown RRR ===')
l={a:np.exp(stat('tight','pairs',w_s,sel=np.arange(A)!=i)-stat('tight','pairs',w_b,sel=np.arange(A)!=i)) for i,a in enumerate(apts)}
print('  baseline-adjusted LOO range',min(l.values()),min(l,key=l.get),max(l.values()),max(l,key=l.get))
Ks=C['tight'][:,m,:].sum(1); Ns=C['pairs'][:,m,:].sum(1); sp=pd.DataFrame(dict(apt=apts,us=US,t24=Ks[:,0],t25=Ks[:,1],p24=Ns[:,0],p25=Ns[:,1])); sp['rr']=(sp.t25/sp.p25)/(sp.t24/sp.p24); sp['pr']=sp.p25/sp.p24
print(sp.sort_values('t24',ascending=False).head(8).round(3).to_string())
print('  tight-pair counts: top-5 US airports share of US tight pairs 2024:',sp[sp.us==1].t24.nlargest(5).sum()/sp[sp.us==1].t24.sum())
print('  correlation (log) between per-airport change in pairs/landing coverage and change in tight share:',np.corrcoef(np.log(sp.pr[(sp.t24>20)&(sp.t25>20)]),np.log(sp.rr[(sp.t24>20)&(sp.t25>20)]))[0,1])
