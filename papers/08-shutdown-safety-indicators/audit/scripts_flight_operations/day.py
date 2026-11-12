import pandas as pd, numpy as np, sys
pd.set_option('display.width',250); pd.set_option('display.max_rows',400)
g=pd.read_parquet('ga_all.parquet'); h=pd.read_parquet('wx_hour.parquet')
a=pd.read_parquet('att_wx.parquet',columns=['apt','date','hr','isga','rwy'])
def show(apt,date):
    x=g[(g.apt==apt)&(g.date==date)].sort_values('t_end')
    x=x.assign(utc=pd.to_datetime(x.t_end,unit='s').dt.strftime('%H:%M'))
    print('==',apt,date,len(x)); print(x[['utc','callsign','actype','rwy','hmin','x_end','follow']].to_string(index=False))
    d=a[(a.apt==apt)&(a.date==date)]
    hh=d.groupby('hr').agg(n=('isga','size'),ga=('isga','sum'),rw=('rwy',lambda s:','.join(f'{k}:{v}' for k,v in s.value_counts().head(4).items()))).reset_index().merge(h[h.apt==apt],on='hr',how='left')
    print(hh[['hr','n','ga','rw','ceil','vis','sk','gust','ts']].to_string(index=False))
for s in sys.argv[1:]:
    apt,date=s.split(':'); show(apt,date)
