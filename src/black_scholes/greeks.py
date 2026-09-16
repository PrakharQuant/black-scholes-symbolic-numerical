"""Symbolic and finite-difference Greeks."""

import math
import sympy as sp
from .pricing import call_price


def symbolic_greeks():
    S, K, T, r, sigma = sp.symbols("S K T r sigma", positive=True)
    d1 = (sp.log(S / K) + (r + sigma**2 / 2) * T) / (sigma * sp.sqrt(T))
    d2 = d1 - sigma * sp.sqrt(T)
    N = lambda x: sp.erf(x / sp.sqrt(2)) / 2 + sp.Rational(1, 2)
    price = S * N(d1) - K * sp.exp(-r * T) * N(d2)
    expressions = {
        "delta": sp.diff(price, S),
        "gamma": sp.diff(price, S, 2),
        "vega": sp.diff(price, sigma),
        "theta": -sp.diff(price, T),
        "rho": sp.diff(price, r),
    }
    return (S, K, T, r, sigma), price, expressions


def finite_difference_greeks(S, K, T, r, sigma, h=1e-4):
    price = lambda s, t, rr, vol: call_price(s, K, t, rr, vol)
    delta = (price(S + h, T, r, sigma) - price(S - h, T, r, sigma)) / (2 * h)
    gamma = (price(S + h, T, r, sigma) - 2 * price(S, T, r, sigma) + price(S - h, T, r, sigma)) / h**2
    vega = (price(S, T, r, sigma + h) - price(S, T, r, sigma - h)) / (2 * h)
    # Calendar-time theta is negative time-to-maturity derivative.
    theta = -(price(S, T + h, r, sigma) - price(S, T - h, r, sigma)) / (2 * h)
    rho = (price(S, T, r + h, sigma) - price(S, T, r - h, sigma)) / (2 * h)
    return {"delta": delta, "gamma": gamma, "vega": vega, "theta": theta, "rho": rho}

