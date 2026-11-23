import numpy as np
import pandas as pd

from load_yields import load_yields
from yield_changes import daily_changes_bp


def fit_pca(train):
    # estimate yield-curve factors(in basis point) from daily change
    covariance = train.cov()
    eigenvalues, eigenvectors = np.linalg.eigh(covariance)

    # NumPy returns the smallest eigenvalue first, but we want it to be
    # descending order.
    order = np.argsort(eigenvalues)[::-1]
    eigenvalues = eigenvalues[order]
    eigenvectors = eigenvectors[:, order]

    names = [f"Principal Component {i + 1}" for i in range(len(eigenvalues))]
    loadings = pd.DataFrame(eigenvectors, index=train.columns, columns=names)
    variance_pct = pd.Series(100 * eigenvalues / eigenvalues.sum(), index=names)

    return loadings, variance_pct


if __name__ == "__main__":
    changes_bp = daily_changes_bp(load_yields())
    train = changes_bp.loc["2022":"2024"]
    loadings, variance_pct = fit_pca(train)

    print("Share of total variance explained (%):")
    print(variance_pct.round(2))
    print(f"\nFirst two components together: {variance_pct.iloc[:2].sum():.2f}%")

    print("\nHow does each maturity move along Principal Component 1 and Principal Component 2:")
    print(loadings.iloc[:, :2])
