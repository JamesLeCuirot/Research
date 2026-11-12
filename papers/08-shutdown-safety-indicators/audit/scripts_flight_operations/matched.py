from common import *
g=pd.read_parquet('ga_all.parquet',columns=['apt','icao','t_end','follow'])
a=load(); a=a[a.win!='post']
a['icao']=a.icao.astype(str); a['apt']=a.apt.astype(str); g['icao']=g.icao.astype(str); g['apt']=g.apt.astype(str)
a=a.merge(g,on=['apt','icao','t_end'],how='left')
a['m']=a.isga&(a.follow=='land_same_30'); a['m200']=a.m&(a.hmin>=200)
t=a.groupby(['win','us','year']).agg(n=('isga','size'),ga=('isga','sum'),m=('m','sum'),m200=('m200','sum'))
for c in ('ga','m','m200'):
    r=1000*t[c]/t.n; print(c,r.round(3).to_dict())
    for w in ('sep','shut'): print('  RRR',w,round((r[(w,True,2025)]/r[(w,True,2024)])/(r[(w,False,2025)]/r[(w,False,2024)]),3))
# excluding airports with runway-availability/coverage breaks
bad=['KBNA','KHOU','PHNL','KDTW','KBOS','KCVG','CYYC','LSZH','LEBL','LFPG','KSDF','KSTL','KTPA','LSGG','KMCO','KIND']
b=a[~a.apt.isin(bad)]; t=b.groupby(['win','us','year']).agg(n=('isga','size'),ga=('isga','sum'),m200=('m200','sum'))
for c in ('ga','m200'):
    r=1000*t[c]/t.n
    for w in ('sep','shut'): print('excl break airports',c,w,round((r[(w,True,2025)]/r[(w,True,2024)])/(r[(w,False,2025)]/r[(w,False,2024)]),3))
