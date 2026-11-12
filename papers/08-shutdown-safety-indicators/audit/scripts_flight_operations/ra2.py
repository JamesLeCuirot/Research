import numpy as np, pandas as pd, sys
sys.path.insert(0,'/home/claude/research/papers/08-shutdown-safety-indicators/code')
from actypes import BIZJET, AIRLINE
pd.set_option('display.width',250); pd.set_option('display.max_rows',400)
G=pd.read_csv('/home/claude/research/papers/08-shutdown-safety-indicators/code/airports_study.csv')
ap=pd.read_csv('/home/claude/shutdown/ref/airports.csv',usecols=['ident','latitude_deg','longitude_deg','elevation_ft']).merge(G,left_on='ident',right_on='icao')
AL=np.radians(ap.latitude_deg.values)[None,:]; AO=np.radians(ap.longitude_deg.values)[None,:]
e=pd.read_parquet('ra_all_raw.parquet')
print('ground flagged events',e.ground.sum(),'no position',e.lat.isna().sum(), 'df types',e.df.value_counts().to_dict(), 'src', e.src.value_counts().head(6).to_dict())
e=e.dropna(subset=['lat','lon'])
la=np.radians(e.lat.values)[:,None]; lo=np.radians(e.lon.values)[:,None]
dd=np.hypot((lo-AO)*np.cos((la+AL)/2),la-AL)*3440.065; j=dd.argmin(1); e['dmin']=dd[np.arange(len(e)),j]; e['apt']=ap.icao.values[j]; e['agl']=e.alt-ap.elevation_ft.fillna(0).values[j]; e['grp']=ap.grp.values[j]
s=e[(e.dmin<15)&(e.agl<7000)&e.typ.isin(BIZJET|AIRLINE)].copy()
s['date']=pd.to_datetime(s.date); s['year']=s.date.dt.year; s['pdate']=s.date.where(s.year==2025,s.date+pd.Timedelta(days=364))
s['win']=np.where(s.pdate<'2025-10-01','sep',np.where(s.pdate<='2025-11-12','shut','post'))
s['us']=s.grp.isin(['US40','USOTHER'])
AD=pd.read_csv('/home/claude/research/papers/08-shutdown-safety-indicators/results/airport_day.csv'); kept=set(AD.apt)
u=s[s.us&s.apt.isin(kept)&(s.win!='post')].copy()
print('US events by win/year (all, before n>=30 airport-day filter)'); print(u.groupby(['win','year']).size().unstack())
u['coc_first']=u.adv.fillna('').str.contains('Clear of Conflict'); u['coc_only']=(u.advs=='Clear of Conflict')
u['midnight']=u.since0<30
print('first msg CoC',u.coc_first.mean(),'CoC only',u.coc_only.mean(),'single-msg events',(u.nmsg==1).mean(),'within 30s of file start',u.midnight.mean())
print(u.groupby(['win','year']).agg(n=('hex','size'),coc_first=('coc_first','mean'),coc_only=('coc_only','mean'),single=('nmsg',lambda x:(x==1).mean()),mte=('mte',lambda x:(x.astype(str)=='1').mean()),agl_med=('agl','median'),low1000=('agl',lambda x:(x<1000).mean()),climbing=('vr',lambda x:(x>500).mean()),desc=('vr',lambda x:(x<-300).mean()),thr_known=('thr',lambda x:x.notna().mean()),biz=('typ',lambda x:x.isin(BIZJET).mean())).round(3).to_string())
print(u.adv.value_counts().head(25))
t=u.groupby(['adv','win','year']).size().unstack(['win','year']).fillna(0); t['tot']=t.sum(axis=1); print(t.sort_values('tot',ascending=False).head(15).to_string())
print(pd.crosstab(u.df,[u.win,u.year])); print(pd.crosstab(u.src,[u.win,u.year]))
print(pd.crosstab(pd.cut(u.agl,[-5000,0,500,1000,2000,3000,5000,7000]),[u.win,u.year]))
print(pd.crosstab(pd.cut(u.dmin,[0,2,5,10,15]),[u.win,u.year]))
a=u.groupby(['apt','win','year']).size().unstack(['win','year']).fillna(0); 
n=AD.assign(pdate=pd.to_datetime(AD.pdate)); n['win']=np.where(n.pdate<'2025-10-01','sep',np.where(n.pdate<='2025-11-12','shut','post')); nn=n[n.win!='post'].groupby(['apt','win','year']).n.sum().unstack(['win','year'])
r=(1000*a/nn.loc[a.index]).round(2); r.columns=['r_'+w+str(y) for w,y in r.columns]
a.columns=[w+str(y) for w,y in a.columns]; z=a.join(r); z['tot']=a.sum(axis=1)
print(z.sort_values('tot',ascending=False).to_string())
u.to_parquet('ra_us.parquet')
# controls
c=s[~s.us]; print('control events',c.groupby(['grp','year']).size())
# all-world events per day (network-level capture proxy) and far-from-airport US events
e['date']=pd.to_datetime(e.date); e['year']=e.date.dt.year
print('all events with position by year',e.groupby('year').size().to_dict())
