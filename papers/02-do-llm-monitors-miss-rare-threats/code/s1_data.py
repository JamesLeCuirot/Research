"""Stage 1: download MBPP (full config, all splits), check each reference solution
runs against its own tests in our sandbox, and draw the generation sample.

Outputs
- data/mbpp_raw/full_<split>.parquet   (downloaded files)
- data/mbpp_download.json              (URLs, SHA-256, sizes, date)
- data/mbpp_problems.jsonl             (all 974 problems + split, entry point, eligibility)
- data/sample.json                     (seed, the 450 sampled task_ids, and the remaining
                                        eligible task_ids in a fixed random order, used if
                                        the verified yield is too low)
"""

from __future__ import annotations

import hashlib
import json
import random
import subprocess
from concurrent.futures import ThreadPoolExecutor

import pandas as pd

from common import DATA, entry_point, execute_candidates, now

SPLITS = ["train", "test", "validation", "prompt"]
URL = "https://huggingface.co/api/datasets/google-research-datasets/mbpp/parquet/full/{split}/0.parquet"
SAMPLE_SEED = 20261103
N_SAMPLE = 450


def download() -> dict:
    raw = DATA / "mbpp_raw"
    raw.mkdir(parents=True, exist_ok=True)
    record = {"dataset": "google-research-datasets/mbpp", "config": "full", "license": "CC BY 4.0",
              "downloaded_at": now(), "files": []}
    for split in SPLITS:
        path = raw / f"full_{split}.parquet"
        url = URL.format(split=split)
        if not path.exists():
            subprocess.run(["curl", "-sSL", "--fail", "-o", str(path), url], check=True)
        data = path.read_bytes()
        record["files"].append({"split": split, "url": url, "path": str(path.relative_to(DATA.parent)),
                                "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()})
    (DATA / "mbpp_download.json").write_text(json.dumps(record, indent=2))
    return record


def check_reference(p: dict) -> dict:
    entry = entry_point(p["code"], p["test_list"])
    p["entry_point"] = entry
    if entry is None:
        p["eligible"], p["ineligible_reason"] = False, "no entry point found in tests"
        return p
    r = execute_candidates({"reference": p["code"]}, p["test_list"], p["test_setup_code"], entry, None)
    ok = r["candidates"]["reference"]["tests_passed"]
    p["eligible"] = bool(ok)
    p["ineligible_reason"] = None if ok else "reference fails its own tests in sandbox"
    return p


def main() -> None:
    rec = download()
    problems = []
    for split in SPLITS:
        df = pd.read_parquet(DATA / "mbpp_raw" / f"full_{split}.parquet")
        for _, r in df.iterrows():
            problems.append({
                "task_id": int(r.task_id), "split": split, "text": r.text, "code": r.code,
                "test_list": [str(t) for t in r.test_list], "test_setup_code": r.test_setup_code or "",
            })
    with ThreadPoolExecutor(8) as pool:
        problems = list(pool.map(check_reference, problems))
    problems.sort(key=lambda p: p["task_id"])
    with open(DATA / "mbpp_problems.jsonl", "w") as f:
        for p in problems:
            f.write(json.dumps(p) + "\n")
    eligible = [p["task_id"] for p in problems if p["eligible"]]
    rng = random.Random(SAMPLE_SEED)
    order = eligible[:]
    rng.shuffle(order)
    sample = {"seed": SAMPLE_SEED, "n_problems": len(problems), "n_eligible": len(eligible),
              "ineligible": {str(p["task_id"]): p["ineligible_reason"] for p in problems if not p["eligible"]},
              "sample": sorted(order[:N_SAMPLE]), "reserve_order": order[N_SAMPLE:]}
    (DATA / "sample.json").write_text(json.dumps(sample, indent=1))
    print(json.dumps({k: v for k, v in sample.items() if k not in ("sample", "reserve_order")}, indent=1))
    print("sampled", len(sample["sample"]), "reserve", len(sample["reserve_order"]))
    print([f["sha256"][:12] for f in rec["files"]])


if __name__ == "__main__":
    main()
