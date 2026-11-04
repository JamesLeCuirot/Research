# data/

Everything in this folder except this README is gitignored. Recreate it with:

```bash
uv run afacs-ingest
```

What gets created:

| Path | What it is |
|---|---|
| `raw/MAD_full_dataset.json` | The MAST dataset (1,642 traces), downloaded from Hugging Face at a pinned revision and checked against a SHA-256 hash. |
| `processed/traces.jsonl` | One line per trace: metadata, MAST labels, inclusion/exclusion decision, and the trace split into numbered steps. |
| `processed/audit.json` | Machine-readable counts behind `docs/data_audit.md`. |
| `processed/calibration_key.csv` | Which calibration traces are controls, their MAST labels and dev/test split. Kept out of the coding sheet so coding stays blind. |
| `calibration/C01.md …` | Rendered calibration traces for hand-coding. |

**Why we don't commit traces:** the MAST data is CC-BY-4.0, so redistribution would be allowed with attribution. But the traces contain GAIA benchmark questions, and benchmark maintainers ask that these not be reposted where web crawlers can find them (it contaminates future model training). The fetch script makes the data fully reproducible without reposting it.

Source: Cemri et al. (2025), *Why Do Multi-Agent LLM Systems Fail?*, dataset `mcemri/MAST-Data` on Hugging Face, licence CC-BY-4.0.
