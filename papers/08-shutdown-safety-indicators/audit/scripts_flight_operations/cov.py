from common import *
pd.set_option('display.width',220); pd.set_option('display.max_rows',300)
a=load()
a=a[a.win!='post']
a['lowga']=a.isga&(a.hmin<200); a['higa']=a.isga&(a.hmin>=200); a['mid']=a.isga&(a.hmin>=400)
t=a.groupby(['win','us','year']).agg(n=('isga','size'),ga=('isga','sum'),low=('lowga','sum'),hi=('higa','sum'),mid=('mid','sum'))
for c in ['ga','low','hi','mid']: t['r_'+c]=1000*t[c]/t.n
print(t.round(3))
def rrr(c,w):
    r=t['r_'+c]; return (r[(w,True,2025)]/r[(w,True,2024)])/(r[(w,False,2025)]/r[(w,False,2024)])
for c in ['ga','low','hi','mid']: print(c,'RRR shut',round(rrr(c,'shut'),3),'sep',round(rrr(c,'sep'),3))
ld=a[~a.isga]
c=ld.groupby(['us','year']).agg(conf=('confirmed','mean'),ok500=('ok500','mean'),ok1000=('ok1000','mean'),hl=('h_last','median'),hl200=('h_last',lambda s:(s>200).mean()))
print(c.round(3))
ca=ld[ld.win=='shut'].groupby(['apt','year'],observed=True).agg(conf=('confirmed','mean'),ok500=('ok500','mean'),hl200=('h_last',lambda s:(s>200).mean()),n=('confirmed','size')).unstack('year')
ga=a[a.win=='shut'].groupby(['apt','year'],observed=True).agg(ga=('isga','sum'),n=('isga','size')).unstack('year')
ca['rr']=(ga[('ga',2025)]/ga[('n',2025)])/(ga[('ga',2024)]/ga[('n',2024)])
ca['dconf']=ca[('conf',2025)]-ca[('conf',2024)]; ca['dok']=ca[('ok500',2025)]-ca[('ok500',2024)]; ca['nrat']=ca[('n',2025)]/ca[('n',2024)]
ca['us']=ca.index.map(G.set_index('icao').grp).isin(['US40','USOTHER'])
print(ca.sort_values('dconf').round(2).to_string())
from scipy.stats import spearmanr
for u in (True,False):
    x=ca[ca.us==u]; print('US' if u else 'CTL','spearman log rr vs dconf',spearmanr(np.log(x.rr),x.dconf), 'vs dok500',spearmanr(np.log(x.rr),x.dok),'vs nrat',spearmanr(np.log(x.rr),x.nrat))
print(ca.groupby('us')[['dconf','dok','nrat']].describe().T.round(3))
