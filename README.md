# Black–Scholes from PDE to Practice

A compact symbolic–numerical study of European option pricing, Greeks, and the limits of closed-form solutions.

## What this project demonstrates

- Black–Scholes European call and put pricing.
- Symbolic generation of Greeks with SymPy.
- Verification of the Black–Scholes PDE residual.
- Comparison of symbolic Greeks with central finite differences.
- Convergence of a Cox–Ross–Rubinstein tree to the Black–Scholes price.
- Pricing of an American put, where early exercise removes the simple European closed form.

## Assumptions

The basic Black–Scholes model assumes constant volatility and interest rate, no dividends, frictionless markets, continuous trading, and European exercise.

The implementation uses `T` as **time to maturity**. Therefore, the reported calendar-time Theta is:

```text
Theta = -dV/dT
