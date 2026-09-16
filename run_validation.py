from pprint import pprint
from src.black_scholes.validation import make_figures


if __name__ == "__main__":
    results = make_figures()
    print("Validation results:")
    pprint(results)
    print("\nFigures written to ./figures/")
