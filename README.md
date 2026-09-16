Black–Scholes from PDE to Practice

A compact symbolic–numerical study of European option pricing, Greeks, and the limits of closed-form solutions.

What this project demonstrates

•
Black–Scholes European call and put pricing.

•
Symbolic generation of Greeks with SymPy.

•
Verification of the Black–Scholes PDE residual.

•
Comparison of symbolic Greeks with central finite differences.

•
Convergence of a Cox–Ross–Rubinstein tree to the Black–Scholes price.

•
Pricing of an American put, where early exercise removes the simple European closed form.

Assumptions

The basic Black–Scholes model assumes constant volatility and interest rate, no dividends, frictionless markets, continuous trading, and European exercise.

The implementation uses T as time to maturity. Therefore, the reported calendar-time Theta is:

Plain Text


Theta = -dV/dT



Project structure

Plain Text


black-scholes-symbolic/
├── README.md
├── requirements.txt
├── src/
│   └── black_scholes/
│       ├── __init__.py
│       ├── pricing.py
│       ├── greeks.py
│       ├── binomial.py
│       └── validation.py
├── tests/
│   ├── test_pricing.py
│   ├── test_greeks.py
│   └── test_binomial.py
└── run_validation.py



Setup

Bash


python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
pip install -r requirements.txt



Run the validation script:

Bash


python run_validation.py



Run tests:

Bash


pytest -q



The script creates a figures/ directory containing:

•
greek_validation.png

•
finite_difference_error.png

•
tree_convergence.png

Mathematical outline

The Black–Scholes PDE for an option value V(S,t) is

Plain Text


V_t + 1/2 sigma^2 S^2 V_SS + r S V_S - r V = 0.



With the log-price transformation x = ln(S) and time-to-maturity tau = T - t, followed by an exponential rescaling of the dependent variable, the PDE becomes the heat equation. Solving the heat equation with the European call payoff gives

Plain Text


C = S N(d1) - K exp(-rT) N(d2)



where

Plain Text


d1 = [ln(S/K) + (r + sigma^2/2)T] / (sigma sqrt(T))
d2 = d1 - sigma sqrt(T).



The put price follows from put–call parity or directly from the corresponding formula.

This repository uses SymPy to verify the PDE identity and to generate symbolic Greeks. The derivation itself is documented analytically because a computer algebra system does not reliably choose all substitutions, boundary conditions, and solution steps automatically.

Interpretation of results

The finite-difference Greeks should approach the symbolic values as the bump size becomes smaller, until floating-point cancellation begins to dominate. The binomial European price should converge toward the Black–Scholes price as the number of steps increases. The American put should be no cheaper than the corresponding European put because early exercise is an additional right.

Limitations and possible extensions

This is an educational implementation, not a production pricing library. It does not model dividends, stochastic volatility, jumps, transaction costs, or market-data calibration. Natural extensions include continuous dividends, implied-volatility inversion, Monte Carlo validation, and a finite-difference PDE solver for American options.
