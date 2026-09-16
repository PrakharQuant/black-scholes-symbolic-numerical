"""Validation utilities and plots."""

from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp

from .pricing import call_price, put_price
from .greeks import symbolic_greeks, finite_difference_greeks
from .binomial import european_put_binomial, american_put_binomial


def symbolic_numeric_greeks(S, K, T, r, sigma):
    symbols, _, expressions = symbolic_greeks()
    values = {}
    for name, expression in expressions.items():
        fn = sp.lambdify(symbols, expression, "numpy")
        values[name] = float(fn(S, K, T, r, sigma))
    return values


def pde_residual(S, T, r, sigma):
    """Numerically evaluate the PDE residual using central differences."""
    h_s, h_t = 1e-3 * S, 1e-5
    v = lambda s, t: call_price(s, 100.0, t, r, sigma)
    # T is time to maturity, so calendar-time V_t equals -V_T.
    v_t = -(v(S, T + h_t) - v(S, T - h_t)) / (2 * h_t)
    v_s = (v(S + h_s, T) - v(S - h_s, T)) / (2 * h_s)
    v_ss = (v(S + h_s, T) - 2 * v(S, T) + v(S - h_s, T)) / h_s**2
    return v_t + 0.5 * sigma**2 * S**2 * v_ss + r * S * v_s - r * v(S, T)


def make_figures(output_dir="figures"):
    output = Path(output_dir)
    output.mkdir(exist_ok=True)
    K, T, r, sigma = 100.0, 1.0, 0.05, 0.20
    spots = np.linspace(60, 140, 100)
    names = ["delta", "gamma", "vega"]

    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    for ax, name in zip(axes, names):
        analytic = []
        finite = []
        for S in spots:
            analytic.append(symbolic_numeric_greeks(S, K, T, r, sigma)[name])
            finite.append(finite_difference_greeks(S, K, T, r, sigma)[name])
        ax.plot(spots, analytic, label="symbolic", linewidth=2)
        ax.plot(spots, finite, "--", label="finite difference")
        ax.set_title(name.capitalize())
        ax.set_xlabel("Spot price S")
        ax.grid(alpha=0.3)
    axes[0].set_ylabel("Greek value")
    axes[-1].legend()
    fig.tight_layout()
    fig.savefig(output / "greek_validation.png", dpi=160)
    plt.close(fig)

    stepsizes = np.logspace(-1, -5, 20)
    errors = []
    exact_delta = symbolic_numeric_greeks(100, K, T, r, sigma)["delta"]
    for h in stepsizes:
        estimate = finite_difference_greeks(100, K, T, r, sigma, h=h)["delta"]
        errors.append(abs(estimate - exact_delta))
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.loglog(stepsizes, errors, marker="o")
    ax.set_xlabel("Finite-difference bump size")
    ax.set_ylabel("Absolute Delta error")
    ax.set_title("Finite-difference error versus bump size")
    ax.grid(alpha=0.3, which="both")
    fig.tight_layout()
    fig.savefig(output / "finite_difference_error.png", dpi=160)
    plt.close(fig)

    step_values = [10, 25, 50, 100, 200, 400]
    bs_put = put_price(100, K, T, r, sigma)
    tree_puts = [european_put_binomial(100, K, T, r, sigma, n) for n in step_values]
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(step_values, tree_puts, marker="o", label="European binomial")
    ax.axhline(bs_put, linestyle="--", label="Black–Scholes")
    ax.set_xlabel("Tree steps")
    ax.set_ylabel("Put price")
    ax.set_title("Binomial convergence")
    ax.legend()
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(output / "tree_convergence.png", dpi=160)
    plt.close(fig)

    return {
        "call": call_price(100, K, T, r, sigma),
        "put": bs_put,
        "pde_residual": pde_residual(100, T, r, sigma),
        "greeks": symbolic_numeric_greeks(100, K, T, r, sigma),
        "american_put": american_put_binomial(100, K, T, r, sigma, 400),
        "tree_convergence": dict(zip(step_values, tree_puts)),
    }

