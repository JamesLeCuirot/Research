# 08 · Landing on the Wrong Altimeter Setting

**Status:** working draft v0.2 (11 November 2026), revised after independent review. Pre-registered.

A pre-registered study using open ADS-B data (adsb.lol) of how often aircraft land with the broadcast altimeter setting differing from the local setting, at 119 US and European airports on 30 days in 2026.

**Findings.** Business jets landed with a setting at least 2 hPa from the consensus about three times as often as airline jets at the same airport on the same day (odds ratio 3.4, 2.9 to 4.0; supported as pre-registered and unchanged on a corrected measure). Most of that difference is small discrepancies of 2 to 3 hPa. Errors of 5 hPa or more were rare (0.20 per 1,000 landings overall) and the larger business-jet excess there is imprecise. The second hypothesis, more "standard left set" in Europe than the US, was not supported; an apparent excess was a data artefact found in review.

**Read first:** the abstract and Section 7 of [`paper.pdf`](paper.pdf), then [`AUDIT.md`](AUDIT.md).

| File | What it holds |
| --- | --- |
| [`PREREGISTRATION.md`](PREREGISTRATION.md) | Plan, committed before any altimeter data from the study days was read (commit `be41aa0`) |
| `code/` | Frozen code (`HASHES.txt`), plus the post hoc scripts `posthoc_modal_extract.py`, `posthoc_after_review.py` and `make_figure.py` |
| `results/` | `confirmatory.json` and `secondary.json` (registered measure); `modal_*.json` and `after_review.json` (corrected measure, post hoc) |
| [`AUDIT.md`](AUDIT.md) | Independent review and what changed |
| [`sources.md`](sources.md) | How each reference was checked |

**Open points.** The PDF was built with a fallback reference style (`ieeetr`) because `IEEEtran.bst` was not available where it was built; rebuild with `papers/_build/build.sh`. The processed landing tables are not in the repository. The EUROCONTROL paper has not been read in full.

AI assistance: design, code, analysis and drafting by Claude (Anthropic) under the author's direction.
