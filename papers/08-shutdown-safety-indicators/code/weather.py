"""Airport-day weather covariates from hourly METAR (PREREGISTRATION.md section 7.4). Contains no outcome data.
Usage: python3 weather.py airports_study.csv out.csv metar_file [metar_file ...]
Input: Iowa Environmental Mesonet ASOS/METAR download (routine + special reports), comma separated, UTC, missing = M.
Definitions (days are UTC days, as in the flight data):
  lowvis_share  share of clock hours with any report showing a ceiling (lowest BKN/OVC/VV layer) under 1,000 ft
                or visibility under 3 statute miles, among hours with at least one report
  gust25        1 if any report that day has a gust of 25 kt or more
  ts            1 if any report that day has a thunderstorm present-weather code (TS, including VCTS)
  hours         number of clock hours with at least one report (coverage check)"""
import sys
import numpy as np, pandas as pd

def main(study_csv, out, files):
    G = pd.read_csv(study_csv)
    w = pd.concat([pd.read_csv(f, na_values=['M'], low_memory=False) for f in files], ignore_index=True)
    ids = set(G.icao)
    w['apt'] = [s if s in ids else 'K' + s for s in w.station.astype(str)]
    assert set(w.apt) <= ids, sorted(set(w.apt) - ids)
    v = pd.to_datetime(w.valid); w['date'] = v.dt.date; w['hour'] = v.dt.hour
    ceil = np.full(len(w), np.inf)
    for i in (4, 3, 2, 1):            # lowest broken/overcast/vertical-visibility layer
        c = w[f'skyc{i}'].astype(str).str.strip(); l = pd.to_numeric(w[f'skyl{i}'], errors='coerce')
        m = c.isin(['BKN', 'OVC', 'VV']) & l.notna()
        ceil = np.where(m & (l.values < ceil), l.values, ceil)
    vis = pd.to_numeric(w.vsby, errors='coerce')
    w['low'] = ((ceil < 1000) | (vis < 3)).astype(int)
    w['g25'] = (pd.to_numeric(w.gust, errors='coerce') >= 25).astype(int)
    w['tsr'] = w.wxcodes.fillna('').astype(str).str.contains('TS').astype(int)
    h = w.groupby(['apt', 'date', 'hour']).agg(low=('low', 'max')).reset_index()
    a = h.groupby(['apt', 'date']).agg(lowvis_share=('low', 'mean'), hours=('low', 'size')).reset_index()
    b = w.groupby(['apt', 'date']).agg(gust25=('g25', 'max'), ts=('tsr', 'max')).reset_index()
    a = a.merge(b, on=['apt', 'date']); a['lowvis_share'] = a.lowvis_share.round(4)
    a.sort_values(['apt', 'date']).to_csv(out, index=False)
    print('airport-days', len(a), 'airports', a.apt.nunique(), 'dates', a.date.min(), a.date.max())
    print('airport-days with under 18 reporting hours:', int((a.hours < 18).sum()))
    a['year'] = [x.year for x in a.date]; a['us'] = a.apt.map(G.set_index('icao').grp.isin(['US40', 'USOTHER']))
    print(a.groupby(['us', 'year'])[['lowvis_share', 'gust25', 'ts', 'hours']].mean().round(3).to_string())

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3:])
