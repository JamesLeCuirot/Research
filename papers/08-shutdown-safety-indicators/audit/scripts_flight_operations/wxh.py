from common import *
pd.set_option('display.width',220); pd.set_option('display.max_rows',300)
w=pd.concat([pd.read_csv(f'/home/claude/shutdown/metar/metar_{y}.csv',na_values=['M'],usecols=['station','valid','sknt','gust','vsby','skyc1','skyc2','skyc3','skyc4','skyl1','skyl2','skyl3','skyl4','wxcodes'],low_memory=False) for y in (2024,2025)])
ids=set(G.icao); w['apt']=[s if s in ids else 'K'+s for s in w.station.astype(str)]
ceil=np.full(len(w),np.inf)
for i in (1,2,3,4):
    c=w[f'skyc{i}'].astype(str).str.strip(); l=pd.to_numeric(w[f'skyl{i}'],errors='coerce'); m=c.isin(['BKN','OVC','VV'])&l.notna()
    ceil=np.where(m&(l.values<ceil),l.values,ceil)
w['ceil']=ceil; w['vis']=pd.to_numeric(w.vsby,errors='coerce')
v=pd.to_datetime(w.valid); w['hr']=v.dt.floor('h')
w['ts']=w.wxcodes.fillna('').astype(str).str.contains('TS'); w['g']=pd.to_numeric(w.gust,errors='coerce').fillna(0); w['sk']=pd.to_numeric(w.sknt,errors='coerce')
h=w.groupby(['apt','hr']).agg(ceil=('ceil','min'),vis=('vis','min'),ts=('ts','max'),gust=('g','max'),sk=('sk','max')).reset_index()
h.to_parquet('wx_hour.parquet')
a=load(); a=a[a.win!='post']
a['hr']=pd.to_datetime(a.t_end,unit='s').dt.floor('h'); a['apt']=a.apt.astype(str)
a=a.merge(h,on=['apt','hr'],how='left')
print('unmatched',a.ceil.isna().mean())
vis=a.vis.fillna(10)
a['cat']=np.select([(a.ceil<200)|(vis<0.5),(a.ceil<500)|(vis<1),(a.ceil<1000)|(vis<3),(a.ceil<=3000)|(vis<=5)],['<200/½','LIFR','IFR','MVFR'],'VFR')
a['cat2']=np.where(a.ts,'TS',np.where((a.cat=='VFR')&(a.gust>=25),'VFR gust25+',a.cat))
a.to_parquet('att_wx.parquet')
for win in ('sep','shut'):
    x=a[a.win==win]
    t=x.groupby(['us','cat2','year']).agg(n=('isga','size'),ga=('isga','sum')).unstack('year'); t['r24']=1000*t[('ga',2024)]/t[('n',2024)]; t['r25']=1000*t[('ga',2025)]/t[('n',2025)]
    t['share24']=t[('n',2024)]/t[('n',2024)].groupby(level=0).transform('sum'); t['share25']=t[('n',2025)]/t[('n',2025)].groupby(level=0).transform('sum')
    print(win); print(t.round(3).to_string())
    # standardised: 2025 rates applied to 2024 mix
    for u in (True,False):
        z=t.loc[u]; print(' us' if u else ' ctl','actual r24',1000*z[('ga',2024)].sum()/z[('n',2024)].sum(),'r25',1000*z[('ga',2025)].sum()/z[('n',2025)].sum(),'r25 with 2024 wx mix',(z.r25*z.share24).sum(), 'r24 with 2025 mix',(z.r24*z.share25).sum())
