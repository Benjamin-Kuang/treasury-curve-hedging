import numpy as np
import pandas as pd

from load_yields import load_yields
from yield_changes import daily_changes_bp
from curve_pca import fit_pca


def build_hedges(loadings, five_year_dv01=1000): # 1000 as DV01 by default
    # simple hedge: 5 years lies 3/8 of the way from 2 years to 10 years
    simple_2yr = -(5 / 8) * five_year_dv01
    simple_10yr = -(3 / 8) * five_year_dv01

    # PCA hedge: use the first two components, given descending order
    factors = loadings.columns[:2]
    hedge_matrix = loadings.loc[["2 Yr", "10 Yr"], factors].T
    target = -five_year_dv01 * loadings.loc["5 Yr", factors]
    pca_2yr, pca_10yr = np.linalg.solve(hedge_matrix, target)

    return pd.DataFrame(
        {
            "Simple hedge": [simple_2yr, five_year_dv01, simple_10yr],
            "PCA hedge": [pca_2yr, five_year_dv01, pca_10yr],
        },
        index=["2 Yr", "5 Yr", "10 Yr"],
    )


if __name__ == "__main__":
    changes_bp = daily_changes_bp(load_yields())
    train = changes_bp.loc["2022":"2024"]
    loadings, _ = fit_pca(train)
    hedges = build_hedges(loadings)

    print("Signed DV01 ($ per basis point):")
    print(hedges.round(2))

    print("\nRemaining exposure to the first two components:")
    factor_loadings = loadings.loc[hedges.index, loadings.columns[:2]]
    print((hedges.T @ factor_loadings).round(4))
