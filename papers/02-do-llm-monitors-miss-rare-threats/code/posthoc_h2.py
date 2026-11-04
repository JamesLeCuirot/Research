"""Post-hoc check of the H2 random-intercept model, requested by the audit (4 November 2026).

Not pre-registered. The registered result is the 40-node Gauss-Hermite fit in analyse.py (§9 item 9) and
stays the registered result. This script asks how accurate that fit is.

For each monitor, on the backdoored items of Experiment 2 (flag ~ condition, reference S50, + (1 | item)):

1. Registered approximation (40-node non-adaptive Gauss-Hermite, the same likelihood as analyse.py):
   - the log-likelihood at the registered estimate;
   - the profile log-likelihood over the item SD (sigma), maximised over the fixed effects;
   - a multi-start fit (Nelder-Mead then BFGS from several sigma starts), to see whether the
     registered BFGS run stopped at a local optimum.
2. Accurate likelihood: dense-grid integration over the standardised random effect, +/-9 SD with
   6,001 points (spacing 0.003 SD). It is validated in this script against per-item adaptive
   integration (scipy.integrate.quad with breakpoints at each logistic step) at the registered estimate
   and at the accurate optimum. Multi-start optimisation; SEs from the numerical Hessian; Wald z and p
   for S1 vs S50; a likelihood-ratio test of the S1 term; the profile log-likelihood over sigma.
3. Accuracy table: the log-likelihood at those two points under each approximation (40-node
   non-adaptive Gauss-Hermite; adaptive Gauss-Hermite with 30 and 60 nodes; dense grid; adaptive
   integration). Gauss-Hermite rules, adaptive ones included, are inaccurate when sigma is large,
   because each item's integrand is then a sharp logistic step (width about 1 on the logit scale)
   times a wide normal. Nodes spaced several logit units apart cannot resolve the step.
4. Exact paired test (McNemar, exact binomial) on backdoored items: items flagged under S50 but not S1
   against items flagged under S1 but not S50. Also none vs S50.

Writes results/posthoc_h2.json and prints a summary.
"""

from __future__ import annotations

import json
import math

import numpy as np
import pandas as pd
from scipy import optimize
from scipy.special import expit
from scipy.stats import binomtest, chi2, norm
from statsmodels.tools.numdiff import approx_hess

from common import RESULTS

CONDS = ["none", "S1"]  # dummies; reference S50 (same order as analyse.glmm_random_intercept)
STARTS = (0.5, 1, 2, 5, 10, 20, 50)


def design(d: pd.DataFrame):
    X = np.column_stack([np.ones(len(d))] + [(d.condition == c).to_numpy(float) for c in CONDS])
    y = d.flag.to_numpy(float)
    codes, uniq = pd.factorize(d.problem_id)
    return X, y, codes, len(uniq)


def nll_ghq(X, y, codes, n_items, n_nodes=40):
    """Non-adaptive Gauss-Hermite negative log-likelihood: identical to analyse.glmm_random_intercept."""
    nodes, weights = np.polynomial.hermite.hermgauss(n_nodes)

    def f(theta):
        beta, s = theta[:-1], math.exp(theta[-1])
        lin = (X @ beta)[:, None] + (math.sqrt(2) * s * nodes)[None, :]
        ll = y[:, None] * lin - np.logaddexp(0, lin)
        L = np.zeros((n_items, n_nodes))
        np.add.at(L, codes, ll)
        m = L.max(axis=1, keepdims=True)
        return -(m[:, 0] + np.log((np.exp(L - m) * weights[None, :]).sum(axis=1) / math.sqrt(math.pi))).sum()
    return f


def nll_grid(X, y, codes, n_items, half_width=9.0, n_points=6001):
    """Dense-grid integration over the standardised random effect z in [-9, 9] (trapezoid-like sum)."""
    z = np.linspace(-half_width, half_width, n_points)
    w = norm.pdf(z) * (z[1] - z[0])

    def f(theta):
        beta, s = theta[:-1], math.exp(theta[-1])
        lin = (X @ beta)[:, None] + s * z[None, :]
        ll = y[:, None] * lin - np.logaddexp(0, lin)
        L = np.zeros((n_items, n_points))
        np.add.at(L, codes, ll)
        m = L.max(axis=1, keepdims=True)
        return -(m[:, 0] + np.log((np.exp(L - m) * w[None, :]).sum(axis=1))).sum()
    return f


def nll_agq(X, y, codes, n_items, n_nodes=30):
    """Adaptive Gauss-Hermite quadrature: for each item, the integrand exp(g(u)), with
    g(u) = sum_j log p(y_ij | eta_ij + u) - u^2 / (2 sigma^2), is centred at its mode u_hat and
    scaled by tau = (-g''(u_hat))^(-1/2). g is strictly concave, so Newton's method finds the mode."""
    nodes, weights = np.polynomial.hermite.hermgauss(n_nodes)
    log_w = np.log(weights) + nodes ** 2
    n_obs = np.bincount(codes, minlength=n_items)

    def f(theta):
        beta, s = theta[:-1], math.exp(theta[-1])
        eta = X @ beta
        # g'(u) = sum_j (y_ij - p_ij(u)) - u / s^2 is strictly decreasing, with g'(-M) > 0 > g'(M) for
        # M = (n_i + 1) s^2. Find its root by vectorised bisection (plain Newton overshoots when the
        # curvature is tiny at large s), then polish with two Newton steps kept inside the bracket.
        M = (n_obs + 1.0) * s ** 2 + 1.0
        lo, hi = -M, M.copy()
        for _ in range(200):
            mid = 0.5 * (lo + hi)
            g1 = np.bincount(codes, y - expit(eta + mid[codes]), n_items) - mid / s ** 2
            pos = g1 > 0
            lo = np.where(pos, mid, lo)
            hi = np.where(pos, hi, mid)
            if np.max(hi - lo) < 1e-11 * max(1.0, s):
                break
        u = 0.5 * (lo + hi)
        for _ in range(2):
            p = expit(eta + u[codes])
            g1 = np.bincount(codes, y - p, n_items) - u / s ** 2
            g2 = -np.bincount(codes, p * (1 - p), n_items) - 1 / s ** 2
            u_new = u - g1 / g2
            u = np.where((u_new > lo) & (u_new < hi), u_new, u)
        p = expit(eta + u[codes])
        tau = 1 / np.sqrt(np.bincount(codes, p * (1 - p), n_items) + 1 / s ** 2)
        uk = u[:, None] + math.sqrt(2) * tau[:, None] * nodes[None, :]  # (items, nodes)
        lin = eta[:, None] + uk[codes]  # (obs, nodes)
        ll = y[:, None] * lin - np.logaddexp(0, lin)
        G = np.zeros((n_items, n_nodes))
        np.add.at(G, codes, ll)
        G = G - uk ** 2 / (2 * s ** 2) + log_w[None, :]
        m = G.max(axis=1, keepdims=True)
        logL = m[:, 0] + np.log(np.exp(G - m).sum(axis=1)) + np.log(math.sqrt(2) * tau) - math.log(s * math.sqrt(2 * math.pi))
        return -logL.sum()
    return f


def fit(nll, start_beta, starts=STARTS):
    """Multi-start: Nelder-Mead then BFGS from each sigma start; return the best."""
    best = None
    for s0 in starts:
        x0 = np.r_[start_beta, math.log(s0)]
        r = optimize.minimize(nll, x0, method="Nelder-Mead", options={"maxiter": 40000, "xatol": 1e-10, "fatol": 1e-12})
        r = optimize.minimize(nll, r.x, method="BFGS", options={"gtol": 1e-7, "maxiter": 5000})
        if best is None or r.fun < best.fun:
            best = r
    return best


def summarise(nll, res, idx=2):
    H = approx_hess(res.x, nll)
    cov = np.linalg.inv(H)
    se = np.sqrt(np.diag(cov))
    z = res.x[idx] / se[idx]
    return {"loglik": float(-res.fun), "sigma": float(math.exp(res.x[-1])), "beta": [float(b) for b in res.x[:-1]],
            "S1_logodds": float(res.x[idx]), "S1_se": float(se[idx]), "S1_z": float(z), "S1_p": float(2 * norm.sf(abs(z))),
            "none_logodds": float(res.x[1]), "none_se": float(se[1]),
            "hessian_min_eig": float(np.linalg.eigvalsh(H).min())}


def lr_test(nll, full):
    """Refit without the S1 term and compare log-likelihoods."""
    def nll_red(th):  # th = [b0, b_none, log sigma]
        return nll(np.r_[th[0], th[1], 0.0, th[2]])
    best = None
    for s0 in STARTS:
        r = optimize.minimize(nll_red, np.r_[full.x[:2], math.log(s0)], method="Nelder-Mead",
                              options={"maxiter": 40000, "xatol": 1e-10, "fatol": 1e-12})
        r = optimize.minimize(nll_red, r.x, method="BFGS", options={"gtol": 1e-7})
        if best is None or r.fun < best.fun:
            best = r
    lr = 2 * (best.fun - full.fun)
    return {"LR": float(lr), "df": 1, "p": float(chi2.sf(lr, 1)), "loglik_reduced": float(-best.fun)}


def exact_paired(d: pd.DataFrame, a: str, b: str) -> dict:
    """Exact McNemar test: items flagged under a but not b, against under b but not a."""
    w = d.pivot_table(index="problem_id", columns="condition", values="flag")
    n_ab = int(((w[a] == 1) & (w[b] == 0)).sum())
    n_ba = int(((w[a] == 0) & (w[b] == 1)).sum())
    p = binomtest(n_ab, n_ab + n_ba, 0.5).pvalue if n_ab + n_ba else float("nan")
    return {f"flagged_{a}_not_{b}": n_ab, f"flagged_{b}_not_{a}": n_ba, "p_exact_two_sided": float(p),
            "n_items": int(len(w))}


def nll_adaptive_integration(X, y, codes, n_items):
    """Reference value: per-item adaptive integration (scipy.integrate.quad) over z in [-12, 12],
    with breakpoints at each observation's logistic step. Slow; used only for validation."""
    from scipy import integrate
    from scipy.special import log_expit

    def f(theta):
        beta, s = theta[:-1], math.exp(theta[-1])
        eta = X @ beta
        total = 0.0
        for i in range(n_items):
            e, yy = eta[codes == i], y[codes == i]

            def integrand(z):
                lin = e + s * z
                return math.exp(float(np.sum(yy * log_expit(lin) + (1 - yy) * log_expit(-lin)))) * norm.pdf(z)
            pts = sorted({float(np.clip(-ej / s, -11.9, 11.9)) for ej in e})
            v, _ = integrate.quad(integrand, -12, 12, points=pts, limit=1000, epsabs=1e-14, epsrel=1e-12)
            total += math.log(v)
        return -total
    return f


def profile(f, beta0, sigmas):
    out = []
    for s in sigmas:
        g = lambda b: f(np.r_[b, math.log(s)])
        r = optimize.minimize(g, beta0, method="Nelder-Mead", options={"maxiter": 20000, "xatol": 1e-10, "fatol": 1e-12})
        r = optimize.minimize(g, r.x, method="BFGS")
        out.append((float(-r.fun), float(r.x[2])))
    return out


def main() -> None:
    A = json.loads((RESULTS / "analysis.json").read_text())
    df = pd.read_csv(RESULTS / "judgments.csv")
    out = {"note": "Post hoc (not pre-registered). The registered H2 result is the 40-node fit in analysis.json.",
           "accurate_method": "dense-grid integration, +/-9 SD, 6,001 points, validated against per-item adaptive integration",
           "monitors": {}}
    sigmas = (1, 2, 5, 10, 13.4, 20, 32.83, 60, 100, 260)
    for mon in ("Haiku", "Sonnet"):
        d = df[(df.monitor == mon) & (df.experiment == "exp2") & (df.backdoored == 1)]
        X, y, codes, n = design(d)
        g = A["H2"][mon]["glmm"]
        reg = np.array([g["coefs"]["Intercept"]["coef"], g["coefs"]["C(condition)[T.none]"]["coef"],
                        g["coefs"]["C(condition)[T.S1]"]["coef"], math.log(g["sigma_item"])])
        n40, grid = nll_ghq(X, y, codes, n, 40), nll_grid(X, y, codes, n)
        r = {"registered_40node": {"sigma": g["sigma_item"], "S1_logodds": float(reg[2]),
                                   "S1_se": g["coefs"]["C(condition)[T.S1]"]["se"], "S1_p": g["coefs"]["C(condition)[T.S1]"]["p"],
                                   "loglik_under_40node": float(-n40(reg))}}
        # Is the registered 40-node fit the optimum of its own (40-node) likelihood?
        m40 = fit(n40, reg[:3])
        r["multistart_40node"] = {"loglik": float(-m40.fun), "sigma": float(math.exp(m40.x[-1])), "S1_logodds": float(m40.x[2])}
        # Accurate fit
        best = fit(grid, reg[:3])
        acc = summarise(grid, best)
        acc["LR_test_S1"] = lr_test(grid, best)
        r["accurate_dense_grid"] = acc
        # Profile log-likelihood over sigma: 40-node approximation vs accurate
        p40, pgrid = profile(n40, reg[:3], sigmas), profile(grid, reg[:3], sigmas)
        r["profile"] = [{"sigma": s, "loglik_40node": a[0], "S1_40node": a[1], "loglik_accurate": b[0], "S1_accurate": b[1]}
                        for s, a, b in zip(sigmas, p40, pgrid)]
        # Accuracy of each approximation at the registered estimate and at the accurate optimum
        meths = {"GH40 (registered)": n40, "AGQ30": nll_agq(X, y, codes, n, 30), "AGQ60": nll_agq(X, y, codes, n, 60),
                 "dense grid": grid, "adaptive integration (reference)": nll_adaptive_integration(X, y, codes, n)}
        r["accuracy"] = {pt: {k: float(-f(th)) for k, f in meths.items()}
                         for pt, th in (("at registered estimate", reg), ("at accurate optimum", best.x))}
        r["exact_S50_vs_S1"] = exact_paired(d, "S50", "S1")
        r["exact_S50_vs_none"] = exact_paired(d, "S50", "none")
        r["items_flagged_in_0_1_2_3_conditions"] = [int((d.groupby("problem_id").flag.sum() == k).sum()) for k in range(4)]
        out["monitors"][mon] = r
        print(f"\n{mon}: registered 40-node sigma {g['sigma_item']:.2f}, S1 {reg[2]:.3f}, 40-node loglik {r['registered_40node']['loglik_under_40node']:.3f}; "
              f"multi-start 40-node optimum: loglik {r['multistart_40node']['loglik']:.3f} at sigma {r['multistart_40node']['sigma']:.2f}, S1 {r['multistart_40node']['S1_logodds']:.3f}")
        print(f"   accurate: sigma {acc['sigma']:.2f}, loglik {acc['loglik']:.4f}, S1 {acc['S1_logodds']:.3f} (SE {acc['S1_se']:.3f}), "
              f"z {acc['S1_z']:.2f}, p {acc['S1_p']:.4f}; LR {acc['LR_test_S1']['LR']:.2f}, p {acc['LR_test_S1']['p']:.5f}")
        for row in r["profile"]:
            print(f"   sigma {row['sigma']:7.2f}: 40-node {row['loglik_40node']:9.3f}   accurate {row['loglik_accurate']:9.3f} (S1 {row['S1_accurate']:.3f})")
        for pt, v in r["accuracy"].items():
            print(f"   loglik {pt}: " + "; ".join(f"{k} {x:.4f}" for k, x in v.items()))
        print("   exact S50 vs S1:", r["exact_S50_vs_S1"], "| S50 vs none:", r["exact_S50_vs_none"])
    (RESULTS / "posthoc_h2.json").write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
