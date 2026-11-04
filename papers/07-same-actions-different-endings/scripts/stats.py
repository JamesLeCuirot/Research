"""Small statistics helpers in plain Python, with no third-party dependencies, for reproducibility.

- Wilcoxon signed-rank test. Zero differences are dropped (Wilcoxon's method), tied absolute
  differences get average ranks, and the two-sided p-value comes from the normal
  approximation with a tie-corrected variance and no continuity correction.
- Holm step-down adjustment.
- Percentile bootstrap confidence interval for a mean, with a fixed seed.
- Fleiss' kappa for agreement across repeated runs.
"""
import math
import random


def _avg_ranks(values):
    order = sorted(range(len(values)), key=lambda i: values[i])
    ranks = [0.0] * len(values)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and values[order[j + 1]] == values[order[i]]:
            j += 1
        r = (i + j) / 2 + 1
        for k in range(i, j + 1):
            ranks[order[k]] = r
        i = j + 1
    return ranks


def wilcoxon(diffs):
    """Return (n_nonzero, W_plus, z, p_two_sided). p is None if fewer than 1 non-zero difference."""
    d = [x for x in diffs if x != 0]
    n = len(d)
    if n == 0:
        return 0, 0.0, 0.0, None
    ranks = _avg_ranks([abs(x) for x in d])
    w_plus = sum(r for r, x in zip(ranks, d) if x > 0)
    mean = n * (n + 1) / 4
    # tie correction
    counts = {}
    for a in (abs(x) for x in d):
        counts[a] = counts.get(a, 0) + 1
    tie = sum(t ** 3 - t for t in counts.values())
    var = n * (n + 1) * (2 * n + 1) / 24 - tie / 48
    if var <= 0:
        return n, w_plus, 0.0, 1.0
    z = (w_plus - mean) / math.sqrt(var)
    p = math.erfc(abs(z) / math.sqrt(2))
    return n, w_plus, z, p


def holm(pvals):
    """Holm-adjusted p-values, in the input order. None stays None."""
    idx = [i for i, p in enumerate(pvals) if p is not None]
    adj = [None] * len(pvals)
    m = len(idx)
    running = 0.0
    for rank, i in enumerate(sorted(idx, key=lambda i: pvals[i])):
        val = min(1.0, (m - rank) * pvals[i])
        running = max(running, val)
        adj[i] = running
    return adj


def bootstrap_ci(values, n_boot=10000, seed=20261004, alpha=0.05):
    if not values:
        return None, None
    rng = random.Random(seed)
    n = len(values)
    means = sorted(sum(rng.choice(values) for _ in range(n)) / n for _ in range(n_boot))
    lo = means[int((alpha / 2) * n_boot)]
    hi = means[int((1 - alpha / 2) * n_boot) - 1]
    return lo, hi


def fleiss_kappa(items):
    """items: a list of lists of category labels, one inner list per item, all the same length."""
    items = [it for it in items if len(it) >= 2]
    if not items:
        return None
    n = len(items[0])
    items = [it for it in items if len(it) == n]
    N = len(items)
    cats = sorted({c for it in items for c in it})
    p_j = {c: sum(it.count(c) for it in items) / (N * n) for c in cats}
    P_i = [(sum(it.count(c) ** 2 for c in cats) - n) / (n * (n - 1)) for it in items]
    P_bar = sum(P_i) / N
    P_e = sum(v ** 2 for v in p_j.values())
    if P_e == 1:
        return 1.0
    return (P_bar - P_e) / (1 - P_e)
