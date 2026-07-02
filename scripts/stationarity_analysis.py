import os
import pandas as pd
from statsmodels.tsa.stattools import adfuller

DATA_DIR = "data/processed"

assets = ["TSLA", "BND", "SPY"]


def adf_test(series, title):

    print("=" * 70)
    print(title)

    result = adfuller(series.dropna())

    labels = [
        "ADF Statistic",
        "p-value",
        "# Lags Used",
        "# Observations"
    ]

    for value, label in zip(result[:4], labels):
        print(f"{label}: {value}")

    print("\nCritical Values")

    for key, value in result[4].items():
        print(f"{key}: {value}")

    if result[1] < 0.05:
        print("\nConclusion:")
        print("Reject the null hypothesis.")
        print("The series is stationary.")
    else:
        print("\nConclusion:")
        print("Fail to reject the null hypothesis.")
        print("The series is non-stationary.")


for asset in assets:

    print("\n")
    print("#" * 70)
    print(f"Analyzing {asset}")

    file_path = os.path.join(DATA_DIR, f"{asset}.csv")

    df = pd.read_csv(file_path)

    # Handle CSVs with two header rows
    if df.columns[0] == "Price":
        df = pd.read_csv(file_path, skiprows=[1])
        df.rename(columns={"Price": "Date"}, inplace=True)

    df["Date"] = pd.to_datetime(df["Date"])

    df["Close"] = pd.to_numeric(df["Close"], errors="coerce")

    df = df.dropna()

    # Daily returns
    df["Daily Return"] = df["Close"].pct_change()

    print("\nADF Test on Closing Prices")

    adf_test(
        df["Close"],
        f"{asset} Closing Price"
    )

    print("\nADF Test on Daily Returns")

    adf_test(
        df["Daily Return"],
        f"{asset} Daily Returns"
    )