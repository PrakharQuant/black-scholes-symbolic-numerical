import pytest
from src.black_scholes.pricing import call_price, put_price


def test_known_black_scholes_call():
    assert call_price(100, 100, 1, 0.05, 0.20) == pytest.approx(10.4506, abs=1e-4)


def test_put_call_parity():
    S, K, T, r, sigma = 100, 105, 1.5, 0.03, 0.25
    lhs = call_price(S, K, T, r, sigma) - put_price(S, K, T, r, sigma)
    rhs = S - K * __import__("math").exp(-r * T)
    assert lhs == pytest.approx(rhs, abs=1e-10)


def test_invalid_inputs():
    with pytest.raises(ValueError):
        call_price(0, 100, 1, 0.05, 0.2)

