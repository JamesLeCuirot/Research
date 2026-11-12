from common import *
pd.set_option('display.width',220); pd.set_option('display.max_rows',300)
a=load(); a=a[a.win=='shut']
a['low']=a.isga&(a.hmin<200); a['hi']=a.isga&(a.hmin>=200)
t=a.groupby(['apt','year'],observed=True).agg(n=('isga','size'),low=('low','sum'),hi=('hi','sum'),conf=('confirmed','mean')).unstack('year')
t['us']=t.index.map(G.set_index('icao').grp).isin(['US40','USOTHER'])
t['dlow']=t[('low',2025)]-t[('low',2024)]
print(t[~t.us].sort_values('dlow').round(2).to_string())
print(t[t.us].sort_values('dlow').round(2).to_string())
# stable-coverage subset: airports with confirmed share change <0.1 abs and n ratio within 0.9-1.1 and ok
t['dconf']=(t[('conf',2025)]-t[('conf',2024)]).abs(); t['nr']=t[('n',2025)]/t[('n',2024)]
s=t[(t.dconf<0.1)&(t.nr.between(0.9,1.1))]
print('stable-coverage airports', s.us.value_counts().to_dict())
for u in (True,False):
    x=s[s.us==u]; 
    for c in ('low','hi'):
        print(u,c, 1000*x[(c,2024)].sum()/x[('n',2024)].sum(), 1000*x[(c,2025)].sum()/x[('n',2025)].sum())
    tot24=(x[('low',2024)]+x[('hi',2024)]).sum()/x[('n',2024)].sum(); tot25=(x[('low',2025)]+x[('hi',2025)]).sum()/x[('n',2025)].sum(); print(u,'all',1000*tot24,1000*tot25,tot25/tot24)
