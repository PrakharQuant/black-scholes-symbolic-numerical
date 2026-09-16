"""Cox–Ross–Rubinstein binomial option pricing."""

import math


def _tree_inputs(S, K, T, r, sigma, steps):
    if steps < 1 or int(steps) != steps:
        raise ValueError("steps must be a positive integer")
    dt = T / steps
    u = math.exp(sigma * math.sqrt(dt))
    d = 1 / u
    growth = math.exp(r * dt)
    p = (growth - d) / (u - d)
    if not 0 <= p <= 1:
        raise ValueError("risk-neutral probability is outside [0, 1]")
    return dt, u, d, p, math.exp(-r * dt)


def european_put_binomial(S, K, T, r, sigma, steps=200):
    dt, u, d, p, discount = _tree_inputs(S, K, T, r, sigma, steps)
    values = [max(K - S * u**j * d**(steps - j), 0.0) for j in range(steps + 1)]
    for i in range(steps - 1, -1, -1):
        values = [discount * (p * values[j + 1] + (1 - p) * values[j]) for j in range(i + 1)]
    return values[0]


def american_put_binomial(S, K, T, r, sigma, steps=200):
    dt, u, d, p, discount = _tree_inputs(S, K, T, r, sigma, steps)
    values = [max(K - S * u**j * d**(steps - j), 0.0) for j in range(steps + 1)]
    for i in range(steps - 1, -1, -1):
        values = [
            max(
                discount * (p * values[j + 1] + (1 - p) * values[j]),
                K - S * u**j * d**(i - j),
            )
            for j in range(i + 1)
        ]
    return values[0]

