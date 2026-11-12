from common import *
pd.set_option('display.width',220); pd.set_option('display.max_rows',300)
a=load(rule1=True)
cs=a.callsign.astype(str)
p=cs.str.extract(r'^([A-Z]{3})(?=\d)')[0]; alt=pd.Series(np.where(cs.str.match(r'^N\d'),'N-reg',np.where(cs.isin(['None','nan','']),'none','other')),index=a.index); a['pre']=p.where(p.notna(),alt)
r=a.groupby(['us','pre']).agg(n=('isga','size'),ga=('isga','sum')).reset_index(); r['rate']=1000*r.ga/r.n
print(r[(r.n>=40)&(r.rate>12)].sort_values('rate',ascending=False).head(40))
print(r[r.pre.isin(['N-reg','none','other','BOE','EJA','FDX','UPS','SWA','AAL','DAL','UAL','SKW','RPA','ENY','JIA','LXJ','FLC','RCH','CNV'])])
# type
r=a.groupby(['us','actype'],observed=True).agg(n=('isga','size'),ga=('isga','sum')).reset_index(); r['rate']=1000*r.ga/r.n
print(r[r.n>3000].sort_values(['us','rate']).to_string())
# 2-GA aircraft days
g=a[a.isga]; k=g.groupby(['date','apt','icao'],observed=True).size(); two=k[k==2].reset_index()
m=g.merge(two,on=['date','apt','icao'])
print('two-GA days: n ac-days',len(two),'biz share',(m.cls=='biz').mean()); print(m.pre.value_counts().head(15)); print(m.apt.astype(str).value_counts().head(12))
print('median hmin 2-GA', m.hmin.median(), 'vs single', g.hmin.median())
# attempts by those aircraft that day: how many landings
key=pd.MultiIndex.from_frame(a[['date','apt','icao']]); sel=a[key.isin(pd.MultiIndex.from_frame(two[['date','apt','icao']]))]
print('2-GA aircraft-days: landings', (~sel.isga).sum(), 'GAs', sel.isga.sum())
# hour local (approx by longitude tz)
ap=pd.read_csv('/home/claude/shutdown/ref/airports.csv',usecols=['ident','longitude_deg']).set_index('ident').longitude_deg
a['lh']=((a.t_end/3600 + a.apt.astype(str).map(ap).astype(float)/15)%24).astype(int)
h=a[a.us].groupby('lh').agg(n=('isga','size'),ga=('isga','sum')); h['rate']=1000*h.ga/h.n; print(h.round(2).T.to_string())
h=a[~a.us].groupby('lh').agg(n=('isga','size'),ga=('isga','sum')); h['rate']=1000*h.ga/h.n; print(h.round(2).T.to_string())
