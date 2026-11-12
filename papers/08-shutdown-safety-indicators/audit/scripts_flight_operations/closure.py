from common import *
pd.set_option('display.width',250); pd.set_option('display.max_rows',400)
a=load(); a=a[(a.win!='post')&~a.isga]
# use physical runway: all 77 days
t=a.groupby(['apt','rwy','year'],observed=True).size().unstack('year',fill_value=0)
tot=t.groupby(level=0).transform('sum'); s=t/tot
f=s[((s[2024]>=0.04)&(s[2025]<0.004))|((s[2025]>=0.04)&(s[2024]<0.004))]
out=t.join(s.round(3),rsuffix='_share').loc[f.index]
out['grp']=out.index.get_level_values(0).map(G.set_index('icao').grp)
print(out.to_string())
# dissimilarity index of runway-end use between years per airport (shutdown window)
x=a[a.win=='shut'].groupby(['apt','rwy','year'],observed=True).size().unstack('year',fill_value=0)
sh=x/x.groupby(level=0).transform('sum'); D=(sh[2024]-sh[2025]).abs().groupby(level=0).sum()/2
D=D.to_frame('dissim'); D['grp']=D.index.map(G.set_index('icao').grp); print(D.sort_values('dissim',ascending=False).head(25).round(2).T.to_string())
print(D.groupby(D.grp.isin(['US40','USOTHER'])).dissim.describe().round(2))
