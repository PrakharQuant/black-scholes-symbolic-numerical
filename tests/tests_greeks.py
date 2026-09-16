import pytest
from src.black_scholes.greeks import symbolic_greeks, finite_difference_greeks
from src.black_scholes.validation import symbolic_numeric_greeks


def test_symbolic_greeks_have_expected_names():
    _, _, expressions = symbolic_greeks()
    assert set(expressions) == {"delta", "gamma", "vega", "theta", "rho"}


def test_finite_difference_matches_symbolic_delta():
    exact = symbolic_numeric_greeks(100, 100, 1, 0.05, 0.2)["delta"]
    estimate = finite_difference_greeks(100, 100, 1, 0.05, 0.2)["delta"]
    assert estimate == pytest.approx(exact, abs=1e-6)


def test_call_delta_and_gamma_are_positive():
    values = symbolic_numeric_greeks(100, 100, 1, 0.05, 0.2)
    assert 0 < values["delta"] < 1
    assert values["gamma"] > 0

