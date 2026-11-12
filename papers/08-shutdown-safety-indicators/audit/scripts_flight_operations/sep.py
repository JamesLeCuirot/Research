from common import *
pd.set_option('display.width',220); pd.set_option('display.max_rows',300)
t=AD.copy(); t['pdate']=pd.to_datetime(t.pdate); t['date']=pd.to_datetime(t.date)
wx=pd.read_csv('/home/claude/research/papers/08-shutdown-safety-indicators/data/weather_airport_day.csv'); wx['date']=pd.to_datetime(wx.date)
t=t.merge(wx,on=['apt','date'],how='left')
s=t[(t.pdate<'2025-10-08')&(t.us==1)]   # sep + first week oct
c=s.groupby(['apt','year']).agg(ga=('ga','sum'),n=('n','sum'),lv=('lowvis_share','mean'),ts=('ts','mean'),g=('gust25','mean')).unstack('year')
c['exp25']=c[('ga',2025)]/c[('n',2025)]*c[('n',2024)]; c['excess24']=c[('ga',2024)]-c['exp25']; c['r24']=1000*c[('ga',2024)]/c[('n',2024)]; c['r25']=1000*c[('ga',2025)]/c[('n',2025)]
print(c.sort_values('excess24',ascending=False).round(2).to_string())
print('total excess',c.excess24.sum())
# by day US
d=s.groupby(['pdate','year']).agg(ga=('ga','sum'),n=('n','sum')).unstack('year'); d['r24']=1000*d[('ga',2024)]/d[('n',2024)]; d['r25']=1000*d[('ga',2025)]/d[('n',2025)]
print(d.round(2).to_string())
# top airport-days 2024
x=s[s.year==2024].assign(r=lambda z:1000*z.ga/z.n).sort_values('ga',ascending=False).head(40)
print(x[['date','apt','n','ga','r','lowvis_share','gust25','ts']].to_string())
x=s[s.year==2025].assign(r=lambda z:1000*z.ga/z.n).sort_values('ga',ascending=False).head(15)
print(x[['date','apt','n','ga','r','lowvis_share','gust25','ts']].to_string())
