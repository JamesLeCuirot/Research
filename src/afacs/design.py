"""Every study-design decision in one place, with the reason for it.

If you change a number here, the whole pipeline (ingest audit, sampling,
annotation) picks it up. Changing these after the calibration set has been
hand-coded would change which traces are in it, so treat them as frozen once
coding starts.
"""

# ---- Source data -----------------------------------------------------------

HF_REPO = "mcemri/MAST-Data"
# Pin the exact dataset revision so anyone re-running gets byte-identical data.
HF_REVISION = "95118ac951421753cf1deb87ddea3b01e693c41b"
SOURCE_FILES = {
    # filename: expected SHA-256 (checked after download)
    "MAD_full_dataset.json": "d636ac63dfc1c6af2d312e862f4b7d383b62d3898d431ccd0e7a79d21d85406f",
    "MAD_human_labelled_dataset.json": "30a0c4075078e9a1b8c39bc608d2b5156cc64c6bda1f6fd262786eb81ff4a286",
}

MAST_CODES = ["1.1", "1.2", "1.3", "1.4", "1.5", "2.1", "2.2", "2.3", "2.4", "2.5", "2.6", "3.1", "3.2", "3.3"]
MAST_NAMES = {
    "1.1": "Disobey Task Specification",
    "1.2": "Disobey Role Specification",
    "1.3": "Step Repetition",
    "1.4": "Loss of Conversation History",
    "1.5": "Unaware of Termination Conditions",
    "2.1": "Conversation Reset",
    "2.2": "Fail to Ask for Clarification",
    "2.3": "Task Derailment",
    "2.4": "Information Withholding",
    "2.5": "Ignored Other Agent's Input",
    "2.6": "Reasoning-Action Mismatch",
    "3.1": "Premature Termination",
    "3.2": "No or Incomplete Verification",
    "3.3": "Incorrect Verification",
}

# ---- Data-quality exclusions (facts about the data, not choices) -----------

# In this group, 100 rows hold only 30 distinct trajectory texts, and copies of
# the same text carry unrelated MAST labels (kappa ~ 0). The text and labels
# appear to have been mismatched upstream, so none of these rows can be trusted.
CORRUPT_SOURCE_KEYS = {"ChatDev_ProgramDev-v2_CodeLlama"}

# Metadata corrections: (field, wrong value) -> right value, per source key.
# OpenManus traces are GAIA questions (MAST's own repo folder is "OpenManus_GAIA").
# The AG2 "GSM" traces are GSM-Plus, a perturbed version of GSM8K.
BENCHMARK_CORRECTIONS = {
    "OpenManus_ProgramDev_GPT4o": "GAIA",
    "AG2_GSM_Plus_Claude": "GSM-Plus",
    "AG2_GSM_Plus_GPT4o": "GSM-Plus",
}

# ---- Study-design choices ---------------------------------------------------

# ChatDev traces are 60k-500k tokens each (roughly 100+ pages). Too long to
# hand-code, and the LLM annotator could not be validated at that length.
EXCLUDED_FRAMEWORKS = {"ChatDev"}

# Upper limit on the length of a trace we will code, measured on the cleaned,
# rendered text (approximate tokens = characters / 4). About 40 printed pages.
MAX_APPROX_TOKENS = 30_000

# A trace counts as "failed" if the MAST judge flagged at least one failure
# mode. MAST does not record whether the task actually succeeded, so this is
# the only failure signal available for most traces.

# Random seed for every sampling step, so the samples are reproducible.
SEED = 20261103

# Traces the coder has already seen together with their MAST labels (they were
# shown as examples while planning). Coding them would not be blind.
SEEN_BY_CODER = {"MetaGPT_ProgramDev2_GPT4o__099", "Magentic_One_GPT4o__065"}

# Calibration set: hand-coded by the domain expert.
# Equal numbers per framework (not proportional), so small frameworks are not
# swamped by AG2 and MetaGPT.
CALIBRATION_FRAMEWORKS = ["AG2", "MetaGPT", "Magentic", "AppWorld", "OpenManus", "HyperAgent"]
CALIBRATION_PER_FRAMEWORK = 5
# Of the 5 per framework, how many go to the held-out test set (the rest are dev).
CALIBRATION_TEST_PER_FRAMEWORK = 2
# Controls: traces MAST judged failure-free, mixed in blind. They test whether
# AFACS coding finds failures MAST missed, and stop the coder assuming every
# trace is "guilty".
CALIBRATION_CONTROLS = 4
CALIBRATION_CONTROLS_TEST = 2

# Bulk set for the LLM annotator (frozen codebook + prompt), stratified by framework.
BULK_SIZE = 250
