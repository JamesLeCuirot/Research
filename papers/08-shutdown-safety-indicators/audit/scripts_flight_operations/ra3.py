import numpy as np, pandas as pd, sys
sys.path.insert(0,'/home/claude/research/papers/08-shutdown-safety-indicators/code')
from actypes import BIZJET
pd.set_option('display.width',250); pd.set_option('display.max_rows',400)
u=pd.read_parquet('ra_us.parquet')
AD=pd.read_csv('/home/claude/research/papers/08-shutdown-safety-indicators/results/airport_day.csv')
n=AD.assign(pdate=pd.to_datetime(AD.pdate)); n['win']=np.where(n.pdate<'2025-10-01','sep',np.where(n.pdate<='2025-11-12','shut','post')); n=n[(n.win!='post')&(n.us==1)]
def ratio(excl):
    k=u[~u.apt.isin(excl)].groupby(['win','year']).size(); d=n[~n.apt.isin(excl)].groupby(['win','year']).n.sum(); r=1000*k/d
    return dict(excl=excl, rates=r.round(2).to_dict(), ratio=round((r[('shut',2025)]/r[('sep',2025)])/(r[('shut',2024)]/r[('sep',2024)]),3), yoy_sep=round(r[('sep',2025)]/r[('sep',2024)],3), yoy_shut=round(r[('shut',2025)]/r[('shut',2024)],3))
for ex in ([],['KSFO'],['KBUR','KDCA'],['KSFO','KBUR'],['KSFO','KBUR','KDCA'],['KSFO','KBUR','KDCA','KPHX','KTEB','KDAL']): print(ratio(ex))
# corrective only
u['corrective']=u.adv.str.contains('Climb|Descend',na=False)
print(u.groupby(['win','year'])['corrective'].agg(['sum','mean']).round(3))
for apt in ['KSFO','KBUR','KPHX','KTEB','KDAL']:
    x=u[u.apt==apt].copy(); print('=====',apt,len(x))
    x['week']=((x.pdate-pd.Timestamp('2025-09-01')).dt.days//7)
    print(x.groupby(['year','week']).size().unstack('week',fill_value=0).to_string())
    print('biz share by year',x.groupby('year').typ.apply(lambda s:s.isin(BIZJET).mean()).round(2).to_dict(),'agl median',x.groupby('year').agl.median().to_dict(), 'desc share', x.groupby('year').vr.apply(lambda v:(v<-300).mean()).round(2).to_dict(),'climb share', x.groupby('year').vr.apply(lambda v:(v>300).mean()).round(2).to_dict())
    print(x.groupby('year').adv.apply(lambda s:s.value_counts().head(4).to_dict()).to_dict())
    print('top operators',x.groupby('year').flight.apply(lambda s:s.str[:3].value_counts().head(6).to_dict()).to_dict())
    # location grid 0.05 deg
    x['la']=(x.lat/0.04).round()*0.04; x['lo']=(x.lon/0.04).round()*0.04
    g=x.groupby(['la','lo','year']).size().unstack('year',fill_value=0); g['tot']=g.sum(axis=1); print(g.sort_values('tot',ascending=False).head(8).round(2).to_string())
    print('threat known',x.groupby('year').thr.apply(lambda s:s.notna().mean()).round(2).to_dict())
    print('top threats',x.thr.value_counts().head(5).to_dict())
