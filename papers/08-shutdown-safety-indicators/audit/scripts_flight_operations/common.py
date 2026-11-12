import pandas as pd, numpy as np, datetime as dt
G=pd.read_csv('/home/claude/research/papers/08-shutdown-safety-indicators/code/airports_study.csv')
AD=pd.read_csv('/home/claude/research/papers/08-shutdown-safety-indicators/results/airport_day.csv')
KEPT=set(AD.apt)
def load(rule1=True):
    a=pd.read_parquet('all.parquet')
    a['date']=pd.to_datetime(a.date.astype(str))
    a['year']=a.date.dt.year
    a['pdate']=a.date.where(a.year==2025,a.date+pd.Timedelta(days=364))
    a['us']=a.apt.astype(str).map(G.set_index('icao').grp.isin(['US40','USOTHER']))
    a['isga']=(a.outcome=='ga')
    a=a[a.apt.isin(KEPT)]
    if rule1:
        g=a[a.isga].groupby(['date','apt','icao'],observed=True).size(); rep=g[g>=3].index
        key=pd.MultiIndex.from_frame(a[['date','apt','icao']])
        a=a[~(key.isin(rep) | a.callsign.astype(str).str.startswith('FLC').values)]
    a['win']=np.where(a.pdate<'2025-10-01','sep',np.where(a.pdate<='2025-11-12','shut','post'))
    return a
