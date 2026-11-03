"""AFACS: layered, HFACS-style failure analysis of LLM multi-agent traces.

Pipeline stages, one module each (see docs/GUIDE.md for a plain-English walkthrough):

    ingest    -> download MAST, clean it, split each trace into numbered steps
    render    -> turn one trace into a readable markdown file
    sample    -> pick the calibration set (hand-coded by a human expert) and the bulk set
    annotate  -> have Claude code traces with the AFACS codebook
    agreement -> measure human-vs-LLM and LLM-vs-LLM agreement (Cohen's kappa)
    analysis  -> answer the research questions and draw the figures
"""

__version__ = "0.1.0"
