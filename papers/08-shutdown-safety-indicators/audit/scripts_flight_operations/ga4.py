from common import *
pd.set_option('display.width',220); pd.set_option('display.max_rows',300)
g=pd.read_parquet('ga_all.parquet')
g['off']=g.x_end>150
t=g.groupby(g.apt.astype(str)).agg(n=('off','size'),off=('off','sum'),hmed=('hmin','median'),h_hi=('hmin',lambda s:(s>1500).mean()),h_lo=('hmin',lambda s:(s<100).mean()))
t['offshare']=(t.off/t.n).round(3); print(t.sort_values('offshare',ascending=False).head(20).round(2))
print(t.sort_values('h_hi',ascending=False).head(12).round(2))
print(t.sort_values('h_lo',ascending=False).head(12).round(2))
o=g[g.off]
print(pd.crosstab(o.apt.astype(str),o.follow).assign(n=lambda x:x.sum(axis=1)).sort_values('n',ascending=False).head(12))
print(o[o.apt=='KSEA'][['date','icao','actype','callsign','rwy','hmin','x_end','follow']].head(30))
print(o[o.apt=='KSEA'].callsign.astype(str).str[:3].value_counts().head())
# GA with hmin>1500 : follow status
print(pd.crosstab(pd.cut(g.hmin,[-1e4,100,400,1000,1500,3100]),g.follow,normalize='index').round(3))
# by year: hmin distribution
print(pd.crosstab([g.us,g.year],pd.cut(g.hmin,[-1e4,100,400,1000,1500,3100]),normalize='index').round(3))
print(pd.crosstab([g.us,g.year],pd.cut(g.hmin,[-1e4,100,400,1000,1500,3100])))
