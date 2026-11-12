# Processed data for paper 08 (shutdown and go-around rates)

This branch holds data only. The paper, code and results are on `main` under `papers/08-shutdown-safety-indicators/`.

| Folder | Contents |
|---|---|
| `attempts/` | One parquet file per UTC day (154 days: 2 Sep–17 Nov 2024 and 1 Sep–16 Nov 2025). One row per approach attempt at a study airport: the output of `code/approaches.py`. |
| `acas/` | Daily TCAS resolution advisory message files, copied unchanged from the adsb.lol archive. |
| `metar/` | Hourly METAR for the 84 study airports from the Iowa Environmental Mesonet, as downloaded on 11 Nov 2026 (gzipped). |
| `reference/` | OurAirports airports and runways files used for processing, and the archive's published size indexes. |
| `logs/` | Per-day processing logs. |

To rerun the analysis: make a working folder with `data/att/` (the `attempts/` files) and `data/acas/` (the `acas/` files), then run `python3 code/analysis.py WORKDIR results` from the paper folder on `main`.

The raw position data within 15 NM of each airport were deleted after processing and are not here. `code/run_day.sh` rebuilds them from the public archive.

Flight data are derived from adsb.lol globe_history, licensed under the Open Database License (ODbL) 1.0.
