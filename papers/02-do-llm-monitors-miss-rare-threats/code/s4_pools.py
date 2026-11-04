"""Stage 4: split verified pairs at random into a calibration pool (40 pairs) and a main pool (the rest).

Usage: python s4_pools.py --version v1 [--final]
Writes data/pools_<version>.json (and data/pools.json with --final).
"""

from __future__ import annotations

import argparse
import json
import random
import shutil

from common import DATA, read_jsonl

POOL_SEED = 4021
N_CAL = 40


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--version", default="v1")
    ap.add_argument("--final", action="store_true")
    args = ap.parse_args()
    items = read_jsonl(DATA / f"items_{args.version}.jsonl")
    ids = sorted(it["problem_id"] for it in items)
    rng = random.Random(POOL_SEED)
    rng.shuffle(ids)
    pools = {"seed": POOL_SEED, "version": args.version, "n_verified": len(ids),
             "calibration": sorted(ids[:N_CAL]), "main": sorted(ids[N_CAL:])}
    (DATA / f"pools_{args.version}.json").write_text(json.dumps(pools, indent=1))
    print(f"calibration pool {len(pools['calibration'])}, main pool {len(pools['main'])}")
    if args.final:
        shutil.copy(DATA / f"pools_{args.version}.json", DATA / "pools.json")


if __name__ == "__main__":
    main()
