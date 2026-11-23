from load_yields import load_yields


def daily_changes_bp(yields):
    # calculate yield change(in basis point) from the previous observation 
    changes = yields.diff() * 100
    return changes.iloc[1:]


if __name__ == "__main__":
    yields = load_yields()
    changes_bp = daily_changes_bp(yields)

    # use 2022–2024 to estimate the hedge, and reserve 2025 to evaluate it
    train = changes_bp.loc["2022":"2024"]
    test = changes_bp.loc["2025"]

    print("5-year yield check:")
    print(f"Jan 2 yield:  {yields.loc['2024-01-02', '5 Yr']:.2f}%")
    print(f"Jan 3 yield:  {yields.loc['2024-01-03', '5 Yr']:.2f}%")
    print(f"Jan 3 change: {changes_bp.loc['2024-01-03', '5 Yr']:.0f} bp")
    print(f"Training observations: {len(train)}")
    print(f"Test observations:     {len(test)}")
