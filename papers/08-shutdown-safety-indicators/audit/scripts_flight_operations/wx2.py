import pandas as pd, numpy as np
pd.set_option('display.width',220); pd.set_option('display.max_rows',300)
a=pd.read_parquet('att_wx.parquet')
v=a[(a.cat2=='VFR')&a.us]
for win in ('sep','shut'):
    t=v[v.win==win].groupby(['apt','year']).agg(n=('isga','size'),ga=('isga','sum')).unstack('year')
    t['r24']=1000*t[('ga',2024)]/t[('n',2024)]; t['r25']=1000*t[('ga',2025)]/t[('n',2025)]; t['exc24']=t[('ga',2024)]-t.r25*t[('n',2024)]/1000
    print(win,'VFR-hours only; total excess 2024',t.exc24.sum()); print(t.sort_values('exc24',ascending=False).round(2).head(18).to_string()); print(t.sort_values('exc24').round(2).head(8).to_string())
    print('airports with r24>r25:',(t.r24>t.r25).sum(),'of',len(t))
# control VFR by airport count
c=a[(a.cat2=='VFR')&~a.us]
for win in ('sep','shut'):
    t=c[c.win==win].groupby(['apt','year']).agg(n=('isga','size'),ga=('isga','sum')).unstack('year'); t['r24']=1000*t[('ga',2024)]/t[('n',2024)]; t['r25']=1000*t[('ga',2025)]/t[('n',2025)]
    print(win,'ctl airports r24>r25:',(t.r24>t.r25).sum(),'of',len(t))
# hmin bands in VFR hours US by year sept
v=v.assign(band=pd.cut(v.hmin,[-1e4,200,500,1000,3100]))
x=v[v.isga].groupby(['win','year','band'],observed=True).size().unstack('band'); n=v.groupby(['win','year']).size(); print((x.div(n,axis=0)*1000).round(3))
# by class
print(v.groupby(['win','cls','year']).agg(n=('isga','size'),ga=('isga','sum')).assign(r=lambda z:1000*z.ga/z.n).round(2))
# by hmin band with follow
