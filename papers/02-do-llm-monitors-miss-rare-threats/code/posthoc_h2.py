"""Post-hoc check of the H2 random-intercept model, requested by the audit (4 November 2026).

Not pre-registered. The registered result is the 40-node Gauss-Hermite fit in analyse.py (§9 item 9) and
stays the registered result. This script asks how accurate that fit is.

For each monitor, on the backdoored items of Experiment 2 (flag ~ condition, reference S50, + (1 | item)):

1. Registered approximation (40-node non-adaptive Gauss-Hermite, the same likelihood as analyse.py):
   - the log-likelihood at the registered estimate;
   - a multi-start fit (Nelder-Mead then BFGS from several sigma starts), to see whether the
     registered single-start BFGS run stopped at a local optimum of its own likelihood.
2. Accurate likelihood: dense-grid integration over the standardised random effect, +/-9 SD with
   6,001 points (spacing 0.003 SD). It is validated here against per-item adaptive integration
   (scipy.integrate.quad with breakpoints at each logistic step) at the registered estimate and at the
   accurate optimum. BFGS from several sigma starts; SEs from the numerical Hessian; Wald z and p for
   S1 vs S50; a likelihood-ratio test of the S1 term; the profile log-likelihood over sigma (also under
   the 40-node approximation, for comparison).
3. Accuracy table: the log-likelihood at those two points under each approximation (40-node
   non-adaptive Gauss-Hermite; adaptive Gauss-Hermite with 30 and 60 nodes; dense grid; adaptive
   integration). Gauss-Hermite rules, adaptive ones included, are inaccurate when sigma is large,
   because each item's integrand is then a sharp logistic step (width about 1 on the logit scale)
   times a wide normal. Nodes spaced several logit units apart cannot resolve the step.
4. Exact paired test (McNemar, exact binomial) on backdoored items: items flagged under S50 but not S1
   against items flagged under S1 but not S50. Also none vs S50.

Results are written to results/posthoc_h2.json after every stage, so an interrupted run keeps what it
finished. Usage: python posthoc_h2.py [--monitor Haiku|Sonnet]   (default: both, one after the other)
"""

from __future__ import annotations

import argparse
import json
import math
import time

import numpy as np
import pandas as pd
from scipy import integrate, optimize
from scipy.special import expit, log_expit
from scipy.stats import binomtest, chi2, norm
from statsmodels.tools.numdiff import approx_hess

from common import RESULTS

OUT = RESULTS / "posthoc_h2.json"
CONDS = ["none", "S1"]  # dummies; reference S50 (same order as analyse.glmm_random_intercept)
SIGMA_STARTS = (1.0, 3.0, 10.0, 30.0)
PROFILE_SIGMAS = (1, 2, 5, 10, 13.4, 20, 32.83, 60)
T0 = time.time()


def log(msg: str) -> None:
    print(f"[{time.time() - T0:6.0f} s] {msg}", flush=True)


class Data:
    """Backdoored Experiment 2 judgments of one monitor, sorted so that each item's rows are contiguous."""

    def __init__(self, d: pd.DataFrame):
        d = d.sort_values(["problem_id", "condition"]).reset_index(drop=True)
        self.d = d
        self.X = np.column_stack([np.ones(len(d))] + [(d.condition == c).to_numpy(float) for c in CONDS])
        self.y = d.flag.to_numpy(float)
        self.codes, uniq = pd.factorize(d.problem_id)
        self.n = len(uniq)
        self.starts = np.r_[0, np.flatnonzero(np.diff(self.codes)) + 1]
        self.n_obs = np.diff(np.r_[self.starts, len(d)])

    def item_sum(self, M: np.ndarray) -> np.ndarray:
        return np.add.reduceat(M, self.starts, axis=0)


def nll_points(D: Data, z: np.ndarray, log_w: np.ndarray, scale_sqrt2: bool):
    """Fixed-point rule: integral over the standardised random effect at points z with log weights."""
    def f(theta):
        beta, s = theta[:-1], math.exp(theta[-1])
        lin = (D.X @ beta)[:, None] + (math.sqrt(2) * s if scale_sqrt2 else s) * z[None, :]
        G = D.item_sum(D.y[:, None] * lin - np.logaddexp(0, lin)) + log_w[None, :]
        m = G.max(axis=1, keepdims=True)
        return -(m[:, 0] + np.log(np.exp(G - m).sum(axis=1))).sum()
    return f


def nll_ghq(D: Data, n_nodes: int = 40):
    """Non-adaptive Gauss-Hermite: the same likelihood as analyse.glmm_random_intercept."""
    x, w = np.polynomial.hermite.hermgauss(n_nodes)
    return nll_points(D, x, np.log(w / math.sqrt(math.pi)), True)


def nll_grid(D: Data, half_width: float = 9.0, n_points: int = 6001):
    """Dense grid over z in [-9, 9]: sum of integrand x normal density x spacing."""
    z = np.linspace(-half_width, half_width, n_points)
    return nll_points(D, z, np.log(norm.pdf(z) * (z[1] - z[0])), False)


def nll_agq(D: Data, n_nodes: int = 30):
    """Adaptive Gauss-Hermite quadrature (as in lme4's nAGQ): each item's integrand exp(g(u)), with
    g(u) = sum_j log p(y_ij | eta_ij + u) - u^2 / (2 sigma^2), is centred at its mode and scaled by
    tau = (-g''(mode))^(-1/2). g' is strictly decreasing; its root is found by vectorised bisection
    (plain Newton overshoots when the curvature is tiny), then polished by two bracketed Newton steps."""
    nodes, weights = np.polynomial.hermite.hermgauss(n_nodes)
    log_w = np.log(weights) + nodes ** 2

    def f(theta):
        beta, s = theta[:-1], math.exp(theta[-1])
        eta = D.X @ beta
        M = (D.n_obs + 1.0) * s ** 2 + 1.0
        lo, hi = -M, M.copy()
        for _ in range(200):
            mid = 0.5 * (lo + hi)
            g1 = D.item_sum(D.y - expit(eta + mid[D.codes])) - mid / s ** 2
            lo, hi = np.where(g1 > 0, mid, lo), np.where(g1 > 0, hi, mid)
            if np.max(hi - lo) < 1e-11 * max(1.0, s):
                break
        u = 0.5 * (lo + hi)
        for _ in range(2):
            p = expit(eta + u[D.codes])
            u_new = u - (D.item_sum(D.y - p) - u / s ** 2) / (-D.item_sum(p * (1 - p)) - 1 / s ** 2)
            u = np.where((u_new > lo) & (u_new < hi), u_new, u)
        p = expit(eta + u[D.codes])
        tau = 1 / np.sqrt(D.item_sum(p * (1 - p)) + 1 / s ** 2)
        uk = u[:, None] + math.sqrt(2) * tau[:, None] * nodes[None, :]
        lin = eta[:, None] + uk[D.codes]
        G = D.item_sum(D.y[:, None] * lin - np.logaddexp(0, lin)) - uk ** 2 / (2 * s ** 2) + log_w[None, :]
        m = G.max(axis=1, keepdims=True)
        logL = m[:, 0] + np.log(np.exp(G - m).sum(axis=1)) + np.log(math.sqrt(2) * tau) - math.log(s * math.sqrt(2 * math.pi))
        return -logL.sum()
    return f


def nll_quad(D: Data):
    """Reference: per-item adaptive integration (scipy.integrate.quad) over z in [-12, 12], with
    breakpoints at each observation's logistic step. Slow; used only for validation."""
    def f(theta):
        beta, s = theta[:-1], math.exp(theta[-1])
        eta = D.X @ beta
        total = 0.0
        for a, k in zip(D.starts, D.n_obs):
            e, yy = eta[a:a + k], D.y[a:a + k]

            def integrand(z):
                lin = e + s * z
                return math.exp(float(np.sum(yy * log_expit(lin) + (1 - yy) * log_expit(-lin)))) * norm.pdf(z)
            pts = sorted({float(np.clip(-ej / s, -11.9, 11.9)) for ej in e})
            v, _ = integrate.quad(integrand, -12, 12, points=pts, limit=1000, epsabs=1e-14, epsrel=1e-12)
            total += math.log(v)
        return -total
    return f


def multistart(nll, beta0, nelder_mead: bool):
    best = None
    for s0 in SIGMA_STARTS:
        x = np.r_[beta0, math.log(s0)]
        if nelder_mead:
            x = optimize.minimize(nll, x, method="Nelder-Mead", options={"maxiter": 20000, "xatol": 1e-9, "fatol": 1e-11}).x
        r = optimize.minimize(nll, x, method="BFGS", options={"gtol": 1e-6, "maxiter": 2000})
        if best is None or r.fun < best.fun:
            best = r
    return best


def summarise(nll, x):
    H = approx_hess(x, nll)
    se = np.sqrt(np.diag(np.linalg.inv(H)))
    z = x[2] / se[2]
    return {"loglik": float(-nll(x)), "sigma": float(math.exp(x[-1])), "beta": [float(b) for b in x[:-1]],
            "S1_logodds": float(x[2]), "S1_se": float(se[2]), "S1_z": float(z), "S1_p": float(2 * norm.sf(abs(z))),
            "none_logodds": float(x[1]), "none_se": float(se[1]), "hessian_min_eig": float(np.linalg.eigvalsh(H).min())}


def lr_test(nll, x_full):
    """Refit without the S1 term (warm starts) and compare log-likelihoods."""
    red = lambda th: nll(np.r_[th[0], th[1], 0.0, th[2]])  # noqa: E731
    best = None
    for ls in (x_full[-1], math.log(5.0)):
        r = optimize.minimize(red, np.r_[x_full[:2], ls], method="BFGS", options={"gtol": 1e-6})
        if best is None or r.fun < best.fun:
            best = r
    lr = 2 * (best.fun - nll(x_full))
    return {"LR": float(lr), "df": 1, "p": float(chi2.sf(lr, 1)), "loglik_reduced": float(-best.fun),
            "sigma_reduced": float(math.exp(best.x[-1]))}


def profile(nll, beta0):
    out, b = [], np.asarray(beta0, float)
    for s in PROFILE_SIGMAS:
        g = lambda bb: nll(np.r_[bb, math.log(s)])  # noqa: E731
        r = min((optimize.minimize(g, start, method="BFGS") for start in (b, np.asarray(beta0, float))), key=lambda r: r.fun)
        b = r.x
        out.append({"sigma": s, "loglik": float(-r.fun), "S1_logodds": float(r.x[2])})
    return out


def exact_paired(d: pd.DataFrame, a: str, b: str) -> dict:
    """Exact McNemar test: items flagged under a but not b, against under b but not a."""
    w = d.pivot_table(index="problem_id", columns="condition", values="flag")
    n_ab = int(((w[a] == 1) & (w[b] == 0)).sum())
    n_ba = int(((w[a] == 0) & (w[b] == 1)).sum())
    p = binomtest(n_ab, n_ab + n_ba, 0.5).pvalue if n_ab + n_ba else float("nan")
    return {f"flagged_{a}_not_{b}": n_ab, f"flagged_{b}_not_{a}": n_ba, "p_exact_two_sided": float(p), "n_items": int(len(w))}


def load_out() -> dict:
    if OUT.exists():
        o = json.loads(OUT.read_text())
        if o.get("version") == 2:
            return o
    return {"version": 2, "note": "Post hoc (not pre-registered). The registered H2 result is the 40-node fit in analysis.json.",
            "accurate_method": "dense-grid integration, +/-9 SD, 6,001 points, validated against per-item adaptive integration",
            "monitors": {}}


def run_monitor(mon: str, A: dict, df: pd.DataFrame, out: dict) -> None:
    def save():
        r["complete"] = stage == "done"
        out["monitors"][mon] = r
        OUT.write_text(json.dumps(out, indent=1))

    D = Data(df[(df.monitor == mon) & (df.experiment == "exp2") & (df.backdoored == 1)])
    g = A["H2"][mon]["glmm"]
    reg = np.array([g["coefs"]["Intercept"]["coef"], g["coefs"]["C(condition)[T.none]"]["coef"],
                    g["coefs"]["C(condition)[T.S1]"]["coef"], math.log(g["sigma_item"])])
    n40, grid = nll_ghq(D, 40), nll_grid(D)
    stage = "start"
    r = {"items_flagged_in_0_1_2_3_conditions": [int((D.d.groupby("problem_id").flag.sum() == k).sum()) for k in range(4)],
         "exact_S50_vs_S1": exact_paired(D.d, "S50", "S1"), "exact_S50_vs_none": exact_paired(D.d, "S50", "none"),
         "registered_40node": {"sigma": g["sigma_item"], "S1_logodds": float(reg[2]), "S1_se": g["coefs"]["C(condition)[T.S1]"]["se"],
                               "S1_p": g["coefs"]["C(condition)[T.S1]"]["p"], "loglik_under_40node": float(-n40(reg))}}
    save()
    log(f"{mon}: exact tests done: {r['exact_S50_vs_S1']}")
    m40 = multistart(n40, reg[:3], nelder_mead=True)
    r["multistart_40node"] = {"loglik": float(-m40.fun), "sigma": float(math.exp(m40.x[-1])), "S1_logodds": float(m40.x[2])}
    save()
    log(f"{mon}: 40-node multistart {r['multistart_40node']}")
    best = multistart(grid, reg[:3], nelder_mead=False)
    r["accurate_dense_grid"] = summarise(grid, best.x)
    save()
    log(f"{mon}: accurate fit {r['accurate_dense_grid']}")
    r["accurate_dense_grid"]["LR_test_S1"] = lr_test(grid, best.x)
    save()
    log(f"{mon}: LR {r['accurate_dense_grid']['LR_test_S1']}")
    p40, pg = profile(n40, reg[:3]), profile(grid, best.x[:3])
    r["profile"] = [{"sigma": a["sigma"], "loglik_40node": a["loglik"], "S1_40node": a["S1_logodds"],
                     "loglik_accurate": b["loglik"], "S1_accurate": b["S1_logodds"]} for a, b in zip(p40, pg)]
    save()
    log(f"{mon}: profiles done")
    meths = {"GH40 (registered)": n40, "AGQ30": nll_agq(D, 30), "AGQ60": nll_agq(D, 60), "dense grid": grid,
             "adaptive integration (reference)": nll_quad(D)}
    r["accuracy"] = {pt: {k: float(-f(th)) for k, f in meths.items()}
                     for pt, th in (("at registered estimate", reg), ("at accurate optimum", best.x))}
    stage = "done"
    save()
    log(f"{mon}: accuracy table {r['accuracy']}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--monitor", choices=["Haiku", "Sonnet"], default=None)
    args = ap.parse_args()
    A = json.loads((RESULTS / "analysis.json").read_text())
    df = pd.read_csv(RESULTS / "judgments.csv")
    out = load_out()
    for mon in ([args.monitor] if args.monitor else ["Haiku", "Sonnet"]):
        run_monitor(mon, A, df, out)


if __name__ == "__main__":
    main()
