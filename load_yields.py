from pathlib import Path

import pandas as pd


RAW_DATA = Path(__file__).resolve().parent / "data" / "raw data"
MATURITIES = ["1 Yr", "2 Yr", "3 Yr", "5 Yr", "7 Yr", "10 Yr", "20 Yr", "30 Yr"]


def load_yields():
    # load daily treasury par yields in percent, sorted from the oldest to the newest
    annual_tables = []

    for year in range(2022, 2026):
        file_path = RAW_DATA / f"treasury_{year}.csv"
        table = pd.read_csv(file_path, usecols=["Date", *MATURITIES])
        table["Date"] = pd.to_datetime(table["Date"], format="%m/%d/%Y")

        if not table["Date"].dt.year.eq(year).all():
            raise ValueError(f"Unexpected date in {file_path.name}")

        annual_tables.append(table)

    yields = pd.concat(annual_tables).set_index("Date").sort_index()
    yields = yields[MATURITIES].apply(pd.to_numeric, errors="raise")

    if not yields.index.is_unique:
        raise ValueError("Duplicate dates found in the Treasury data.")
    if yields.isna().any().any():
        raise ValueError("Missing yields found. Inspect the data before continuing.")

    return yields


if __name__ == "__main__":
    yields = load_yields()
    print("Observations per year:")
    print(yields.groupby(yields.index.year).size())
    print(f"\nTotal: {len(yields)} dates, {len(yields.columns)} maturities")	
