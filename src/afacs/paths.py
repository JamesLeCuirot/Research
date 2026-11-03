"""Where everything lives. All paths are relative to the repository root."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

DATA = ROOT / "data"
RAW = DATA / "raw"
PROCESSED = DATA / "processed"
CALIBRATION_RENDERS = DATA / "calibration"

TRACES_JSONL = PROCESSED / "traces.jsonl"
AUDIT_JSON = PROCESSED / "audit.json"
CALIBRATION_KEY = PROCESSED / "calibration_key.csv"
BULK_SAMPLE = PROCESSED / "bulk_sample.csv"

CODEBOOK_DIR = ROOT / "codebook"
PROMPTS_DIR = ROOT / "prompts"
HUMAN_ANNOTATIONS = ROOT / "annotations" / "human"
LLM_ANNOTATIONS = ROOT / "annotations" / "llm"
FIGURES = ROOT / "figures"
DOCS = ROOT / "docs"

CALIBRATION_SHEET = HUMAN_ANNOTATIONS / "calibration_sheet.csv"
