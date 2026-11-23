# Hedging a 5-Year U.S. Treasury Exposure

This Python project compares two ways to hedge a 5-year Treasury position using 2-year and 10-year Treasuries. 
The simple hedge sets its weights by maturity, while the PCA hedge sets its weights using historical yield movements.

## Data and results

I used U.S. Treasury yield data from 2022–2024 to build the hedges and tested them on 249 days in 2025.

| Strategy | Daily P&L volatility | Worst daily P&L |
|---|---:|---:|
| Unhedged | $5,402.37 | −$18,000.00 |
| Simple hedge | $1,398.57 | −$4,125.00 |
| PCA hedge | $1,167.88 | −$4,832.93 |

The PCA hedge had 16.5% lower daily P&L volatility than the simple hedge, but its worst single-day loss was larger.

## Run the project

With pandas and NumPy installed and the Treasury CSV files in `data/raw data/`, open `backtest.py` in IDLE and press F5.

[Read the one-page project summary](Report/Treasury%20Hedge%20Summary.pdf)