import pandas as pd, glob, os, datetime as dt
cols=['apt','icao','actype','cls','rwy','outcome','t_end','callsign','confirmed','td_gap','h_last','hmin','h_end','ok1000','ok500','gap_s','fol_nm','x_end','d500','gs_ref']
fr=[]
for f in sorted(glob.glob('/home/claude/shutdown/data/att/*.parquet')):
    a=pd.read_parquet(f,columns=cols); a['date']=os.path.basename(f)[:10]
    for c in ['apt','icao','actype','cls','rwy','outcome','callsign','date']: a[c]=a[c].astype('category')
    for c in ['td_gap','h_last','hmin','h_end','gap_s','fol_nm','x_end','d500','gs_ref']: a[c]=a[c].astype('float32')
    a['ok1000']=a.ok1000.fillna(False).astype(bool); a['ok500']=a.ok500.fillna(False).astype(bool)
    fr.append(a)
a=pd.concat(fr,ignore_index=True)
for c in ['apt','icao','actype','cls','rwy','outcome','callsign','date']: a[c]=a[c].astype(str).astype('category')
a.to_parquet('all.parquet',index=False)
print(len(a), a.memory_usage(deep=True).sum()/1e6)
print(a.outcome.value_counts())
