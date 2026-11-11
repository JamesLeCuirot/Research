#!/bin/bash
# Resumable driver. Usage: run_all.sh DAYLIST_FILE [max_minutes]; stops starting new days after max_minutes (default 105).
CODE=$(cd "$(dirname "$0")" && pwd); export WORK=${WORK:-/home/claude/shutdown}; LIST=$1; MAXM=${2:-105}; S=$(date +%s)
for pass in 1 2 3; do
  while read D; do
    [ -f $WORK/data/done/$D ] && continue
    [ $(( ($(date +%s)-S)/60 )) -ge $MAXM ] && { echo "time limit; resume later"; exit 0; }
    $CODE/run_day.sh $D || echo "$D failed rc=$? (pass $pass)" >> $WORK/logs/failures.log
  done < $LIST
done
echo "list complete: $(ls $WORK/data/done | wc -l) days done"
