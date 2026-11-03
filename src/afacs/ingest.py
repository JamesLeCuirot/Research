"""Stage 1 - ingest: download MAST, clean it, split every trace into steps.

Run:  uv run afacs-ingest

What it does, in order:
1. Downloads the MAST dataset files from Hugging Face at a pinned revision and
   checks their SHA-256 hashes, so everyone works from byte-identical data.
2. Gives each trace a unique id. (MAST's own `trace_id` repeats across groups;
   the unique id is the group key plus the index within the group.)
3. Applies the metadata corrections in `design.py` and flags data-quality
   problems: rows with no labels, the corrupt ChatDev-CodeLlama group, and
   exact duplicate texts (the first copy is kept).
4. Parses every trace into numbered steps (see `parsers.py`).
5. Writes `data/processed/traces.jsonl` (one trace per line) and an audit:
   `data/processed/audit.json` plus a readable `docs/data_audit.md`, which is
   committed so the data problems are documented in the repo.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import statistics
import urllib.request
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path

from sklearn.metrics import cohen_kappa_score

from afacs import design, paths
from afacs.parsers import parse_trace

# ---------------------------------------------------------------------------
# 1. Download
# ---------------------------------------------------------------------------


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def download_sources(force: bool = False, local_dir: Path | None = None) -> None:
    """Fetch the pinned MAST files into data/raw/ (or copy them from local_dir)."""
    paths.RAW.mkdir(parents=True, exist_ok=True)
    for name, expected in design.SOURCE_FILES.items():
        dest = paths.RAW / name
        if dest.exists() and not force and sha256_of(dest) == expected:
            print(f"  {name}: already present, hash OK")
            continue
        if local_dir is not None:
            shutil.copy(local_dir / name, dest)
            print(f"  {name}: copied from {local_dir}")
        else:
            url = f"https://huggingface.co/datasets/{design.HF_REPO}/resolve/{design.HF_REVISION}/{name}"
            print(f"  {name}: downloading {url}")
            urllib.request.urlretrieve(url, dest)
        actual = sha256_of(dest)
        if actual != expected:
            raise RuntimeError(f"{name}: SHA-256 mismatch (got {actual}, expected {expected})")
        print(f"  {name}: hash OK")


# ---------------------------------------------------------------------------
# 2-4. Clean and parse
# ---------------------------------------------------------------------------


def make_uid(key: str, index: int) -> str:
    return f"{key}__{index:03d}"


def benchmark_outcome(framework: str, raw: str) -> str | None:
    """The benchmark's own pass/fail verdict, where the log contains one."""
    if framework == "AppWorld":
        m = re.search(r'^Evaluation\s*\{\s*"success": (true|false)', raw, re.M)
        return {"true": "pass", "false": "fail"}[m.group(1)] if m else None
    if framework == "AG2" and raw.lstrip().startswith("instance_id:"):
        m = re.search(r"^  correct: (True|False)", raw, re.M)
        return {"True": "pass", "False": "fail"}[m.group(1)] if m else None
    return None


def build_traces(records: list[dict]) -> list[dict]:
    traces = []
    first_seen: dict[str, str] = {}  # trajectory text -> uid of first copy
    for r in records:
        key, index = r["trace"]["key"], r["trace"]["index"]
        raw = r["trace"]["trajectory"]
        uid = make_uid(key, index)
        labels = r["mast_annotation"]
        all_null = all(v is None for v in labels.values())

        # Data-quality exclusion: first matching reason wins.
        duplicate_of = first_seen.get(raw)
        if all_null:
            quality_exclusion = "no_mast_labels"
        elif key in design.CORRUPT_SOURCE_KEYS:
            quality_exclusion = "corrupt_source_group"
        elif duplicate_of is not None:
            quality_exclusion = "duplicate_text"
        else:
            quality_exclusion = None
        first_seen.setdefault(raw, uid)

        parsed = parse_trace(r["mas_name"], raw)
        kept_chars = sum(len(s.text) for s in parsed.steps)
        traces.append(
            {
                "uid": uid,
                "source_key": key,
                "source_index": index,
                "framework": r["mas_name"],
                "model": r["llm_name"],
                "benchmark": design.BENCHMARK_CORRECTIONS.get(key, r["benchmark_name"]),
                "benchmark_original": r["benchmark_name"],
                "mast_labels": labels,
                "mast_n_modes": None if all_null else sum(1 for v in labels.values() if v == 1),
                "mast_failed": None if all_null else any(v == 1 for v in labels.values()),
                "benchmark_outcome": benchmark_outcome(r["mas_name"], raw),
                "quality_exclusion": quality_exclusion,
                "duplicate_of": duplicate_of,
                "raw_chars": len(raw),
                "kept_chars": kept_chars,
                "dropped_chars": parsed.dropped_chars,
                # Share of the raw log accounted for by kept text + deliberately dropped
                # noise. The rest is separators/timestamps/indentation. Low values would
                # mean a parser is losing content.
                "coverage": round((kept_chars + parsed.dropped_chars) / max(len(raw), 1), 3),
                "approx_tokens": round(kept_chars / 4),
                "n_steps": len(parsed.steps),
                "parser": parsed.parser,
                "parse_notes": parsed.notes,
                "steps": [
                    {"n": i, "agent": s.agent, "kind": s.kind, "text": s.text}
                    for i, s in enumerate(parsed.steps, start=1)
                ],
            }
        )
    return traces


def design_exclusion(t: dict) -> str | None:
    """Study-design exclusions (choices, see design.py). None means eligible."""
    if t["framework"] in design.EXCLUDED_FRAMEWORKS:
        return "framework_excluded"
    if t["approx_tokens"] > design.MAX_APPROX_TOKENS:
        return "too_long"
    return None


def load_traces(path: Path = paths.TRACES_JSONL) -> list[dict]:
    """Read traces.jsonl (used by every later stage)."""
    if not path.exists():
        raise SystemExit(f"{path} not found. Run `uv run afacs-ingest` first.")
    with open(path) as f:
        return [json.loads(line) for line in f]


# ---------------------------------------------------------------------------
# 5. Audit
# ---------------------------------------------------------------------------


def label_set_agreement(pairs: list[tuple[dict, dict]]) -> dict:
    """How consistently two label sets for the *same* trace agree, code by code.

    For each MAST code we compute Cohen's kappa across all pairs, then average
    the kappas (a "macro" average). We deliberately do NOT pool all 14 codes into
    one big list: some codes are almost always 0 and others almost always 1, and
    pooling counts those easy, base-rate agreements as skill, which inflates kappa.
    Codes where kappa is undefined (everyone said the same thing every time) are
    left out of the average.
    """
    per_code = {}
    for c in design.MAST_CODES:
        a = [x[c] for x, _ in pairs]
        b = [y[c] for _, y in pairs]
        if len(set(a) | set(b)) < 2:
            per_code[c] = None  # undefined: no variation at all
        else:
            per_code[c] = round(float(cohen_kappa_score(a, b)), 3)
    defined = [k for k in per_code.values() if k is not None]
    n_cells = len(pairs) * len(design.MAST_CODES)
    agree = sum(x[c] == y[c] for x, y in pairs for c in design.MAST_CODES) / n_cells
    return {
        "pairs": len(pairs),
        "macro_kappa": round(sum(defined) / len(defined), 3) if defined else None,
        "per_code_kappa": per_code,
        "raw_agreement": round(agree, 3),
        "identical_label_sets": sum(all(x[c] == y[c] for c in design.MAST_CODES) for x, y in pairs),
    }


def human_file_check(human: list[dict]) -> dict:
    """Detect the copied-label problem in MAST's human-labelled file.

    For each round, count how many traces there are and how many *distinct*
    3-annotator label vectors they carry. If every trace in a round has its own
    labels, the two numbers match.
    """
    rounds: dict[str, dict] = {}
    for r in human:
        vector = tuple(
            (a["annotator_1"], a["annotator_2"], a["annotator_3"]) for a in r["annotations"]
        )
        info = rounds.setdefault(r["round"], {"traces": 0, "modes_in_taxonomy": len(r["annotations"]), "vectors": set()})
        info["traces"] += 1
        info["vectors"].add(vector)
    return {
        "n_traces": len(human),
        "rounds": {
            name: {"traces": v["traces"], "modes_in_taxonomy": v["modes_in_taxonomy"], "distinct_label_vectors": len(v["vectors"])}
            for name, v in rounds.items()
        },
    }


def summarise(values: list[float]) -> dict:
    if not values:
        return {}
    v = sorted(values)
    return {
        "min": v[0],
        "median": statistics.median(v),
        "p90": v[int(0.9 * (len(v) - 1))],
        "max": v[-1],
    }


def build_audit(records: list[dict], traces: list[dict], human: list[dict]) -> dict:
    audit: dict = {
        "source": {
            "dataset": design.HF_REPO,
            "revision": design.HF_REVISION,
            "rows": len(records),
            "unique_trajectory_texts": len({r["trace"]["trajectory"] for r in records}),
            "mast_trace_id_unique": len({r["trace_id"] for r in records}) == len(records),
        }
    }

    # Exclusions
    audit["quality_exclusions"] = dict(Counter(t["quality_exclusion"] or "kept" for t in traces))

    # Identical texts with different labels (MAST judge test-retest)
    groups = defaultdict(list)
    for t in traces:
        if t["mast_failed"] is not None:
            groups[t["duplicate_of"] or t["uid"]].append(t)
    dup_groups = [g for g in groups.values() if len(g) > 1]
    differing = sum(1 for g in dup_groups if len({json.dumps(x["mast_labels"], sort_keys=True) for x in g}) > 1)
    retest = {}
    for name, keep in [
        ("magentic_cross_group", lambda g: {x["source_key"] for x in g} == {"MagenticOne_GAIA_GPT4o", "Magentic_One_GPT4o"}),
        ("chatdev_codellama", lambda g: {x["source_key"] for x in g} == {"ChatDev_ProgramDev-v2_CodeLlama"}),
    ]:
        pairs = [(x["mast_labels"], y["mast_labels"]) for g in dup_groups if keep(g) for x, y in combinations(g, 2)]
        if pairs:
            retest[name] = label_set_agreement(pairs)
    audit["duplicates"] = {
        "groups": len(dup_groups),
        "rows_in_groups": sum(len(g) for g in dup_groups),
        "groups_with_differing_labels": differing,
        "test_retest": retest,
    }

    # Metadata
    audit["benchmark_corrections"] = design.BENCHMARK_CORRECTIONS
    audit["empty_task_traces"] = [t["uid"] for t in traces if "empty task requirement" in t["parse_notes"]]
    audit["benchmark_outcome_available"] = dict(Counter(f"{t['framework']}:{t['benchmark_outcome']}" for t in traces if t["benchmark_outcome"]))

    # Per framework: size, parsing, labels, eligibility
    per_fw = {}
    for fw in sorted({t["framework"] for t in traces}):
        ts = [t for t in traces if t["framework"] == fw]
        kept = [t for t in ts if t["quality_exclusion"] is None]
        eligible = [t for t in kept if design_exclusion(t) is None]
        per_fw[fw] = {
            "rows": len(ts),
            "after_quality_exclusions": len(kept),
            "mast_failed": sum(1 for t in kept if t["mast_failed"]),
            "mast_clean": sum(1 for t in kept if t["mast_failed"] is False),
            "eligible_failed": sum(1 for t in eligible if t["mast_failed"]),
            "eligible_clean": sum(1 for t in eligible if t["mast_failed"] is False),
            "approx_tokens": summarise([t["approx_tokens"] for t in kept]),
            "steps": summarise([t["n_steps"] for t in kept]),
            "coverage": summarise([t["coverage"] for t in ts]),
            "low_coverage_rows": [t["uid"] for t in ts if t["coverage"] < 0.85],
            "models": dict(Counter(t["model"] for t in kept)),
            "benchmarks": dict(Counter(t["benchmark"] for t in kept)),
        }
    audit["per_framework"] = per_fw
    audit["eligible_pool"] = {
        "failed": sum(v["eligible_failed"] for v in per_fw.values()),
        "clean": sum(v["eligible_clean"] for v in per_fw.values()),
    }

    # MAST label prevalence among kept traces
    kept = [t for t in traces if t["quality_exclusion"] is None]
    audit["mast_prevalence"] = {
        c: round(sum(1 for t in kept if t["mast_labels"][c] == 1) / len(kept), 3) for c in design.MAST_CODES
    }
    audit["human_labelled_file"] = human_file_check(human)
    return audit


def write_audit_markdown(audit: dict, path: Path) -> None:
    s, d, pf = audit["source"], audit["duplicates"], audit["per_framework"]
    lines = [
        "# Data audit: MAST traces",
        "",
        "Generated by `uv run afacs-ingest`. Do not edit by hand.",
        "",
        f"Source: `{s['dataset']}` at revision `{s['revision'][:7]}`, {s['rows']:,} rows, "
        f"{s['unique_trajectory_texts']:,} distinct trajectory texts.",
        "",
        "## Data-quality exclusions",
        "",
        "| Reason | Rows |",
        "|---|---|",
    ]
    for k, v in sorted(audit["quality_exclusions"].items(), key=lambda kv: -kv[1]):
        lines.append(f"| {k} | {v:,} |")
    lines += [
        "",
        "## Duplicates and label consistency",
        "",
        f"{d['groups']} groups of byte-identical trajectories cover {d['rows_in_groups']} rows. "
        f"In {d['groups_with_differing_labels']} of these groups, the copies carry **different** MAST labels.",
        "",
        "| Duplicate set | Pairs | Mean per-code Cohen's κ | Raw agreement | Identical label sets |",
        "|---|---|---|---|---|",
    ]
    for name, r in d["test_retest"].items():
        lines.append(f"| {name} | {r['pairs']} | {r['macro_kappa']:.2f} | {r['raw_agreement']:.2f} | {r['identical_label_sets']} |")
    lines += [
        "",
        "κ is computed separately for each of the 14 codes and then averaged (codes with no variation are "
        "skipped). Raw agreement looks high because most codes are 'no' most of the time; κ corrects for that.",
        "",
        "Per-code κ for the Magentic pairs: "
        + ", ".join(
            f"{c} {k:.2f}" if k is not None else f"{c} n/a"
            for c, k in d["test_retest"].get("magentic_cross_group", {}).get("per_code_kappa", {}).items()
        ),
        "",
        "The Magentic pairs are the same 30 traces filed under two group names; their κ is a usable "
        "test-retest figure for MAST's LLM judge (small sample: treat as indicative). The ChatDev-CodeLlama "
        "copies agree at about chance level, which suggests the text and labels in that group were "
        "mismatched upstream; the whole group is excluded.",
        "",
        "## Metadata corrections",
        "",
    ]
    for key, bench in audit["benchmark_corrections"].items():
        lines.append(f"- `{key}`: benchmark set to **{bench}**")
    lines += [
        "",
        f"Traces whose task text is empty (a harness defect): {', '.join(f'`{u}`' for u in audit['empty_task_traces']) or 'none'}.",
        "",
        "Benchmark pass/fail recorded inside the log (most traces have none): "
        + ", ".join(f"{k} = {v}" for k, v in sorted(audit["benchmark_outcome_available"].items())),
        "",
        "## Per framework",
        "",
        "Tokens are approximate (characters ÷ 4) and measured after cleaning. *Eligible* means it passes "
        f"the data-quality checks, is not an excluded framework, and is at most {design.MAX_APPROX_TOKENS:,} tokens.",
        "",
        "| Framework | Rows | Kept | MAST-failed | MAST-clean | Eligible failed | Eligible clean | Median tokens | Max tokens | Median steps | Min parse coverage |",
        "|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for fw, v in pf.items():
        lines.append(
            f"| {fw} | {v['rows']} | {v['after_quality_exclusions']} | {v['mast_failed']} | {v['mast_clean']} | "
            f"{v['eligible_failed']} | {v['eligible_clean']} | {v['approx_tokens'].get('median', 0):,.0f} | "
            f"{v['approx_tokens'].get('max', 0):,.0f} | {v['steps'].get('median', 0):.0f} | {v['coverage'].get('min', 0):.2f} |"
        )
    lines += [
        "",
        f"**Eligible pool:** {audit['eligible_pool']['failed']:,} failed traces and {audit['eligible_pool']['clean']:,} "
        "MAST-clean traces (available as controls).",
        "",
        "Parse coverage = (kept text + deliberately dropped noise) ÷ raw length. The remainder is log "
        "scaffolding (timestamps, separators, indentation). Dropped noise is: Magentic install logs, "
        "OpenManus token counters, and three ChatDev boilerplate record types.",
        "",
        "## MAST label prevalence (kept traces)",
        "",
        "| Code | Name | Share of traces flagged |",
        "|---|---|---|",
    ]
    for c, p in audit["mast_prevalence"].items():
        lines.append(f"| {c} | {design.MAST_NAMES[c]} | {p:.0%} |")
    h = audit["human_labelled_file"]
    lines += [
        "",
        "## MAST's human-labelled file (`MAD_human_labelled_dataset.json`)",
        "",
        f"{h['n_traces']} traces (the paper and some documentation say 21). Each round used a different "
        "revision of the taxonomy, so codes are not comparable across rounds.",
        "",
        "| Round | Traces | Modes in taxonomy | Distinct 3-annotator label vectors |",
        "|---|---|---|---|",
    ]
    for rnd, v in h["rounds"].items():
        lines.append(f"| {rnd} | {v['traces']} | {v['modes_in_taxonomy']} | {v['distinct_label_vectors']} |")
    lines += [
        "",
        "Within every round, different traces carry identical label vectors. The original annotation "
        "sheets in MAST's GitHub repo (`inter_annotator_agreement_annotations/*.pdf`) show different "
        "labels per trace, so the Hugging Face file appears to have been assembled incorrectly. "
        "We do not use it.",
        "",
    ]
    path.write_text("\n".join(lines))


# ---------------------------------------------------------------------------


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--force-download", action="store_true", help="re-download even if files exist")
    ap.add_argument("--local-dir", type=Path, help="copy source files from here instead of downloading")
    args = ap.parse_args()

    print("1. Fetching source files")
    download_sources(force=args.force_download, local_dir=args.local_dir)

    print("2-4. Cleaning and parsing traces")
    with open(paths.RAW / "MAD_full_dataset.json") as f:
        records = json.load(f)
    with open(paths.RAW / "MAD_human_labelled_dataset.json") as f:
        human = json.load(f)
    traces = build_traces(records)

    paths.PROCESSED.mkdir(parents=True, exist_ok=True)
    with open(paths.TRACES_JSONL, "w") as f:
        for t in traces:
            f.write(json.dumps(t, ensure_ascii=False) + "\n")
    print(f"  wrote {len(traces):,} traces to {paths.TRACES_JSONL.relative_to(paths.ROOT)}")

    print("5. Writing audit")
    audit = build_audit(records, traces, human)
    paths.AUDIT_JSON.write_text(json.dumps(audit, indent=2))
    write_audit_markdown(audit, paths.DOCS / "data_audit.md")
    print(f"  wrote {paths.AUDIT_JSON.relative_to(paths.ROOT)} and docs/data_audit.md")
    print(f"  eligible pool: {audit['eligible_pool']['failed']} failed, {audit['eligible_pool']['clean']} clean")


if __name__ == "__main__":
    main()
