from common import *
import sys
pd.set_option('display.width',250); pd.set_option('display.max_rows',400)
a=load(); a=a[a.win!='post']
for apt in sys.argv[1:]:
    x=a[a.apt==apt]
    t=x.groupby(['win','rwy','year'],observed=True).agg(n=('isga','size'),ga=('isga','sum'),conf=('confirmed','mean'),low=('hmin',lambda s:0)).drop(columns='low').unstack('year').fillna(0)
    t['r24']=(1000*t[('ga',2024)]/t[('n',2024)]).round(1); t['r25']=(1000*t[('ga',2025)]/t[('n',2025)]).round(1)
    t=t[(t[('n',2024)]+t[('n',2025)])>150]
    print('=====',apt); print(t.round(2).to_string())
    # daily concentration in shutdown window
    s=x[x.win=='shut']; d=s.groupby(['year','date']).agg(n=('isga','size'),ga=('isga','sum'))
    for y in (2024,2025):
        dd=d.loc[y].sort_values('ga',ascending=False); print(y,'total ga',dd.ga.sum(),'n',dd.n.sum(),'top5 days:',[(str(i.date()),int(r.ga),int(r.n)) for i,r in dd.head(5).iterrows()],'days n<50%median:',int((dd.n<0.5*dd.n.median()).sum()), 'ndays',len(dd))
    # top operators GA
    g=s[s.isga]; print('GA by operator', g.groupby('year').callsign.apply(lambda c:c.astype(str).str[:3].value_counts().head(5).to_dict()).to_dict())
    print('GA hmin median', g.groupby('year').hmin.median().round(0).to_dict(), 'share <200ft', g.groupby('year').hmin.apply(lambda h:(h<200).mean()).round(2).to_dict())
