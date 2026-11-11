#!/bin/bash
# Process one archive day end to end. Usage: run_day.sh YYYY-MM-DD ; resumable and idempotent.
set -u
D=$1; Y=${D:0:4}; TAG=v${D//-/.}-planes-readsb-prod-0
CODE=$(cd "$(dirname "$0")" && pwd); W=${WORK:-/home/claude/shutdown}
RAW=$W/data/raw/$D; PTS=$W/data/pts/$D.parquet; ATT=$W/data/att/$D.parquet; ACAS=$W/data/acas/$D.json.gz; LOG=$W/logs/$D.log
[ -f "$W/data/done/$D" ] && exit 0
mkdir -p "$RAW" "$W/data/done"
PUB=$(grep -- "- $D " $W/ref/rel_$Y.md | sed -E 's/.*planes-readsb-prod-0 \(([0-9]+) MiB\).*/\1/')
[ -z "$PUB" ] && { echo "$D no published size" >> $LOG; exit 4; }
BASE=https://github.com/adsblol/globe_history_$Y/releases/download/$TAG
if [ ! -f "$PTS" ]; then
  for p in aa ab ac ad; do
    f=$RAW/$TAG.tar.$p; ok=0
    for try in $(seq 1 25); do
      code=$(curl -sL -C - -m 900 -o "$f" -w '%{http_code}' "$BASE/$TAG.tar.$p"); rc=$?
      if [ "$code" = 416 ]; then ok=1; break; fi
      if [ "$code" = 404 ]; then rm -f "$f"; ok=2; break; fi
      sleep 2
    done
    [ $ok = 2 ] && break
    [ $ok = 0 ] && { echo "$D part $p not completed" >> $LOG; exit 5; }
  done
  TOT=$(cat $RAW/*.tar.* | wc -c); MIB=$((TOT/1048576))
  echo "$D bytes $TOT MiB $MIB published $PUB" >> $LOG
  DIFF=$((MIB-PUB)); [ ${DIFF#-} -gt 2 ] && { echo "$D size mismatch" >> $LOG; rm -rf "$RAW"; exit 6; }
  cat $RAW/*.tar.* | python3 -I $CODE/extract.py $W/ref/airports.csv $CODE/airports_study.csv "$PTS" "$ACAS" 2>> $LOG || { echo "$D extract failed" >> $LOG; rm -f "$PTS"; exit 7; }
fi
rm -rf "$RAW"
python3 -I $CODE/approaches.py "$PTS" $W/ref/runways.csv $W/ref/airports.csv $CODE/airports_study.csv "$ATT" 2>> $LOG || { echo "$D approaches failed" >> $LOG; exit 8; }
rm -f "$PTS"; touch $W/data/done/$D; echo "$D done $(date -u +%H:%M:%S)" >> $LOG
