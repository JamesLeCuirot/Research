"""Stage A: for each detected landing, read the crew-selected altimeter setting broadcast by the aircraft.
Frozen with the preregistration.
Usage: python3 qnh_extract.py points_DATE.parquet attempts_DATE.parquet out_landings_DATE.parquet"""
import sys, numpy as np, pandas as pd
pts, att, out = sys.argv[1:4]
p = pd.read_parquet(pts, columns=['icao', 't', 'qnh'])
p = p[p.qnh.notna()].sort_values('t')
a = pd.read_parquet(att)
l = a[a.outcome == 'land'][['apt', 'rwy', 'icao', 'reg', 'actype', 'cls', 'callsign', 't_end', 'confirmed']].sort_values('t_end').copy()
q = p.rename(columns={'t': 'tq', 'qnh': 'own'})
# setting at landing: last broadcast value in the 120 s up to the last airborne point
j = pd.merge_asof(l, q, left_on='t_end', right_on='tq', by='icao', direction='backward', tolerance=120.0)
# setting about five minutes earlier: last broadcast value between 10 and 5 minutes before landing
l2 = l[['icao', 't_end']].assign(t5=l.t_end - 300.0).sort_values('t5')
j5 = pd.merge_asof(l2, q.rename(columns={'own': 'own5', 'tq': 'tq5'}), left_on='t5', right_on='tq5', by='icao', direction='backward', tolerance=300.0)
j = j.merge(j5[['icao', 't_end', 'own5']], on=['icao', 't_end'], how='left')
j = j.drop(columns=['tq'])
j.to_parquet(out, index=False)
print(len(j), 'landings; setting at landing present for', round(float(j.own.notna().mean()), 4), file=sys.stderr)
