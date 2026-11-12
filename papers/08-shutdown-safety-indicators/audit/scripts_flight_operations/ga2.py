from common import *
pd.set_option('display.width',220); pd.set_option('display.max_rows',300)
a=load(rule1=False)
a=a.sort_values(['icao','t_end']).reset_index(drop=True)
ga=a[a.isga].copy()
# duplicates across airports
d=ga.groupby(['icao','t_end'],observed=True).apt.nunique()
print('GA events with same icao,t_end at >1 airport:', (d>1).sum(), 'of', len(d))
dd=ga.merge(d[d>1].rename('k').reset_index(),on=['icao','t_end'])
print(dd.groupby('apt',observed=True).size().sort_values(ascending=False).head(20))
# near-duplicates within 240s any airport
ga['prev_t']=ga.groupby('icao',observed=True).t_end.shift(); 
print('GA within 300s of previous GA same aircraft (any apt):',((ga.t_end-ga.prev_t)<300).sum())
# next event by same aircraft (any airport)
a['nxt_out']=a.groupby('icao',observed=True).outcome.shift(-1); a['nxt_t']=a.groupby('icao',observed=True).t_end.shift(-1); a['nxt_apt']=a.groupby('icao',observed=True).apt.shift(-1)
a['prv_out']=a.groupby('icao',observed=True).outcome.shift(1); a['prv_t']=a.groupby('icao',observed=True).t_end.shift(1);a['prv_apt']=a.groupby('icao',observed=True).apt.shift(1)
g=a[a.isga].copy(); dtn=(g.nxt_t-g.t_end)
g['follow']=np.where(dtn.isna()|(dtn>3600),'none<60min',np.where(g.nxt_out.astype(str)=='ga','ga_next',np.where(g.nxt_apt.astype(str)==g.apt.astype(str),np.where(dtn<=1800,'land_same_30','land_same_30-60'),'land_other_apt')))
print(pd.crosstab(g.us,g.follow,normalize='index').round(3)); print(pd.crosstab([g.us,g.year],g.follow,normalize='index').round(3))
print(pd.crosstab(g.cls,g.follow,normalize='index').round(3))
t=pd.crosstab(g.apt.astype(str),g.follow); t['n']=t.sum(1); t['none_share']=(t['none<60min']/t.n).round(2); t['other']=(t['land_other_apt']/t.n).round(2)
print(t.sort_values('none_share',ascending=False).head(25))
# time to landing
print('time GA->landing same apt (s)'); print(dtn[g.follow.str.startswith('land_same')].describe(percentiles=[.05,.25,.5,.75,.95]))
# GA immediately preceded by a landing by same aircraft within 10 min at same airport?? (touch and go / landing then GA)
dp=(g.t_end-g.prv_t)
print('GA preceded by landing same apt within 15min:', ((dp<900)&(g.prv_out.astype(str)=='land')&(g.prv_apt.astype(str)==g.apt.astype(str))).sum())
# GAs with no follow: hmin and x_end
print(g.groupby('follow').agg(n=('hmin','size'),hmin=('hmin','median'),x=('x_end','median'),x90=('x_end',lambda s:s.quantile(.9)),biz=('cls',lambda s:(s=='biz').mean())))
# repeated go-arounds per aircraft-day-airport
k=g.groupby(['date','apt','icao'],observed=True).size(); print('GA per aircraft-airport-day'); print(k.value_counts().sort_index())
k2=g.groupby(['date','icao'],observed=True).size(); print('GA per aircraft-day any apt'); print(k2.value_counts().sort_index())
g.to_parquet('ga_all.parquet')
