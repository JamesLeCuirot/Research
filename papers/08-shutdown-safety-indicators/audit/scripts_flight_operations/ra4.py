import numpy as np, pandas as pd
pd.set_option('display.width',250)
u=pd.read_parquet('ra_us.parquet')
a=pd.read_parquet('all.parquet',columns=['apt','icao','rwy','outcome','t_end','cls','actype'])
for apt in ['KSFO','KBUR','KPHX']:
    x=u[u.apt==apt].copy(); L=a[(a.apt==apt)]
    own=x.merge(L[['icao','t_end','rwy','outcome']],left_on='hex',right_on='icao',how='left'); own['dt']=own.t_end-own.t
    own=own[(own.dt>-60)&(own.dt<900)].sort_values('dt').drop_duplicates(['hex','t'])
    x=x.merge(own[['hex','t','rwy','outcome','dt']],on=['hex','t'],how='left')
    thr=x.dropna(subset=['thr']).merge(L[['icao','t_end','rwy','outcome']].rename(columns={'rwy':'trwy','outcome':'tout','t_end':'tt'}),left_on='thr',right_on='icao',how='left'); thr['d2']=thr.tt-thr.t
    thr=thr[(thr.d2>-60)&(thr.d2<900)].sort_values('d2').drop_duplicates(['hex','t'])
    x=x.merge(thr[['hex','t','trwy','tout','d2']],on=['hex','t'],how='left')
    print('==',apt)
    print(x.groupby('year').agg(n=('hex','size'),own_arrival_here=('rwy',lambda s:s.notna().mean()),own_ga=('outcome',lambda s:(s=='ga').mean()),threat_id=('thr',lambda s:s.notna().mean()),threat_is_study_arrival_here=('trwy',lambda s:s.notna().mean())).round(3))
    both=x.dropna(subset=['rwy','trwy']); print('own rwy x threat rwy'); print(pd.crosstab(both.rwy,both.trwy).loc[lambda d:d.sum(axis=1)>10, lambda d:d.sum()>10])
    print('landing time diff own vs threat (s): ', (both.dt-both.d2).abs().describe(percentiles=[.5,.9]).round(0).to_dict())
    # RA rate per own approach by year for arrivals here
    print('own-arrival RA followed by own go-around share', x[x.rwy.notna()].groupby('year').outcome.apply(lambda s:(s=='ga').mean()).round(3).to_dict())
