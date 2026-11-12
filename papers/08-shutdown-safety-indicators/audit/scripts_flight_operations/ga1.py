from common import *
a=load()
print(len(a), a.isga.sum())
ga=a[a.isga]
print('by cls'); print(a.groupby(['us','cls'],observed=True).agg(n=('isga','size'),ga=('isga','sum')).assign(r=lambda x:1000*x.ga/x.n))
print('hmin dist GA (ft above rwy)'); print(ga.groupby('us').hmin.describe(percentiles=[.05,.1,.25,.5,.75,.9,.95]))
bins=[-1e4,0,50,100,200,400,700,1000,1500,2000,3000,1e5]
print(pd.crosstab(pd.cut(ga.hmin,bins),ga.us,normalize='columns').round(3))
print('GA hmin NaN',ga.hmin.isna().mean())
print('x_end (lateral offset m at minimum)'); print(ga.x_end.describe(percentiles=[.5,.75,.9,.95,.99]))
print(pd.crosstab(pd.cut(ga.x_end,[0,50,100,150,300,500,926]),ga.us,normalize='columns').round(3))
# landing confirmed
ld=a[~a.isga]
print('landing confirmed share by us/year'); print(ld.groupby(['us','year']).confirmed.mean())
print('h_last landing'); print(ld.groupby(['us','year']).h_last.describe(percentiles=[.5,.9,.99]))
print('td_gap'); print(ld.groupby(['us','year']).td_gap.describe(percentiles=[.5,.9,.99]))
# per airport rates
r=a.groupby(['apt','year'],observed=True).agg(n=('isga','size'),ga=('isga','sum')).reset_index(); r['rate']=1000*r.ga/r.n
p=r.pivot(index='apt',columns='year',values=['n','ga','rate']); p['nratio']=p[('n',2025)]/p[('n',2024)]
pd.set_option('display.width',200); pd.set_option('display.max_rows',200)
print(p.sort_values(('rate',2024)).round(2))
