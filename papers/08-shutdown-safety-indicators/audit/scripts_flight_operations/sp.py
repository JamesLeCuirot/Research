import pandas as pd, numpy as np
pd.set_option('display.width',250); pd.set_option('display.max_rows',400)
a=pd.read_parquet('att_wx.parquet'); a=a[~a.isga & a.fol_nm.notna()]
a['tight']=a.fol_nm<2.5
print('pairs',len(a)); print(a.groupby(['us','year']).fol_nm.describe(percentiles=[.01,.05,.1,.5]).round(2))
print('share <1.5NM', a.groupby(['us','year']).fol_nm.apply(lambda s:(s<1.5).mean()).round(4).to_dict(), ' <1.0', a.groupby(['us','year']).fol_nm.apply(lambda s:(s<1.0).mean()).round(4).to_dict())
print('gap_s for tight pairs'); print(a[a.tight].groupby('us').gap_s.describe(percentiles=[.05,.5,.95]).round(1))
a['hb']=pd.cut(a.h_last,[-1e4,30,100,300,700],labels=['<30','30-100','100-300','300-700'])
t=a.groupby(['us','hb','year'],observed=True).agg(n=('tight','size'),tight=('tight','mean'),med=('fol_nm','median')).unstack('year'); print(t.round(3))
print(a.groupby(['us','confirmed','year']).agg(n=('tight','size'),tight=('tight','mean')).unstack('year').round(3))
def rrr(x,num='tight'):
    g=x.groupby(['win','us','year'])[num].mean()
    out={}
    for w in ('sep','shut'):
        out[w]=(g[(w,True,2025)]/g[(w,True,2024)])/(g[(w,False,2025)]/g[(w,False,2024)])
    out['adj']=out['shut']/out['sep']; return {k:round(v,3) for k,v in out.items()}, g.round(4).to_dict()
print('all pairs',rrr(a)[0])
lowl=a[(a.h_last<30)]; print('leader last seen <30 ft', rrr(lowl))
c=a[a.confirmed&(a.td_gap<=10)]; print('leader confirmed touchdown ≤10s',len(c), rrr(c))
# airports with stable low-level coverage: share of leaders h_last<30 >0.9 in both years
cov=a.groupby(['apt','year']).h_last.apply(lambda s:(s<30).mean()).unstack('year'); good=cov[(cov[2024]>0.9)&(cov[2025]>0.9)].index
print('stable airports',len(good), list(good)); s=a[a.apt.isin(good)]; print(rrr(s))
# US 2025: tight share by window and weather cat
u=a[a.us]
print(u.groupby(['year','win','cat2']).agg(n=('tight','size'),tight=('tight','mean')).unstack('cat2').round(3).to_string())
# which airports carry sept->shutdown fall in 2025 vs 2024
p=u.groupby(['apt','year','win']).agg(n=('tight','size'),k=('tight','sum')).unstack(['year','win'])
p['d25']=p[('k',2025,'shut')]/p[('n',2025,'shut')]-p[('k',2025,'sep')]/p[('n',2025,'sep')]; p['d24']=p[('k',2024,'shut')]/p[('n',2024,'shut')]-p[('k',2024,'sep')]/p[('n',2024,'sep')]
p['s24sep']=p[('k',2024,'sep')]/p[('n',2024,'sep')];p['s25sep']=p[('k',2025,'sep')]/p[('n',2025,'sep')];p['s24sh']=p[('k',2024,'shut')]/p[('n',2024,'shut')];p['s25sh']=p[('k',2025,'shut')]/p[('n',2025,'shut')]
p['contrib']=(p.d25-p.d24)*p[('n',2025,'shut')]
print(p[['s24sep','s24sh','s25sep','s25sh','contrib']].sort_values('contrib').round(3).head(14).to_string()); print(p[['s24sep','s24sh','s25sep','s25sh','contrib']].sort_values('contrib').round(3).tail(8).to_string())
print('total contrib',p.contrib.sum())
