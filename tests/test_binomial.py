import pytest
from src.black_scholes.pricing import put_price
from src.black_scholes.binomial import european_put_binomial, american_put_binomial


def test_european_tree_approaches_black_scholes():
    bs = put_price(100, 100, 1, 0.05, 0.20)
    tree = european_put_binomial(100, 100, 1, 0.05, 0.20, steps=800)
    assert tree == pytest.approx(bs, abs=0.03)


def test_american_put_not_less_than_european_put():
    european = european_put_binomial(100, 100, 1, 0.05, 0.20, steps=200)
    american = american_put_binomial(100, 100, 1, 0.05, 0.20, steps=200)
    assert american >= european

