import pandas as pd

from load_yields import load_yields
from yield_changes import daily_changes_bp
from curve_pca import fit_pca
from hedge_weights import build_hedges


def run_backtest():
    changes_bp = daily_changes_bp(load_yields())
    train = changes_bp.loc["2022":"2024"]
    test = changes_bp.loc["2025"]

    # set the hedge amounts using only information available before 2025
    five_year_dv01 = 1000
    loadings, _ = fit_pca(train)
    hedges = build_hedges(loadings, five_year_dv01)

    # daily P&L = - sum of (yield change * DV01)
    moves = test[["2 Yr", "5 Yr", "10 Yr"]]
    PnL = -(moves @ hedges)
    PnL.insert(0, "Unhedged", -five_year_dv01 * moves["5 Yr"])

    return PnL


if __name__ == "__main__":
    PnL = run_backtest()

    print("January 2, 2025: estimated P&L ($)")
    print(PnL.loc["2025-01-02"])

    volatility = PnL.std()
    summary = pd.DataFrame({
        "Daily P&L volatility ($)": volatility,
        "Volatility reduction (%)": 100 * (1 - volatility / volatility["Unhedged"]),
        "Worst daily P&L ($)": PnL.min(),
        "Worst date": PnL.idxmin().dt.strftime("%Y-%m-%d"),
    })

    print(f"\nResults for {len(PnL)} observations in 2025:")
    print(summary.to_string())
