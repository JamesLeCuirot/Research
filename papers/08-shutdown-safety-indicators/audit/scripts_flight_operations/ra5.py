import numpy as np, pandas as pd
from common import *
pd.set_option('display.width',250)
e=pd.read_parquet('ra_all_raw.parquet',columns=['hex','t']).sort_values('t')
a=load(); g=a[a.isga&a.us&(a.win!='post')].copy().sort_values('t_end'); g['icao']=g.icao.astype(str); e['hex']=e.hex.astype(str); g['t_end']=g.t_end.astype(float)
m=pd.merge_asof(g,e.rename(columns={'hex':'icao','t':'tra'}),left_on='t_end',right_on='tra',by='icao',direction='nearest',tolerance=180)
m['ra']=m.tra.notna()
print(m.groupby(['win','year']).agg(ga=('ra','size'),with_ra=('ra','sum')).assign(share=lambda z:(z.with_ra/z.ga).round(3)))
t=m.groupby(['apt','year'],observed=True).agg(ga=('ra','size'),with_ra=('ra','sum')).unstack('year'); t['tot']=t[('with_ra',2024)]+t[('with_ra',2025)]
print(t.sort_values('tot',ascending=False).head(8))
n=a[a.us&(a.win!='post')].groupby(['win','year']).size()
k=m[~m.ra].groupby(['win','year']).size(); print('US GA rate excluding RA-linked GAs', (1000*k/n).round(3).to_dict())
k=m[~m.ra&(m.apt!='KSFO')].groupby(['win','year']).size(); n2=a[a.us&(a.win!='post')&(a.apt!='KSFO')].groupby(['win','year']).size(); print('excl SFO too',(1000*k/n2).round(3).to_dict())
