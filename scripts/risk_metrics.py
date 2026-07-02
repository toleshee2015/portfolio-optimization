import os
import numpy as np
import pandas as pd

# Directories
DATA_DIR = "data/processed"
OUTPUT_DIR = "data/risk_metrics"

os.makedirs(OUTPUT_DIR, exist_ok=True)

assets = ["TSLA", "BND", "SPY"]

# Annual risk-free rate (2%)
risk_free_rate = 0.02

for asset in assets:

    print("=" * 80)
    print(f"Analyzing {asset}")

    file_path = os.path.join(DATA_DIR, f"{asset}.csv")

    df = pd.read_csv(file_path)

    # Handle files with an extra header row
    if df.columns[0] == "Price":
        df = pd.read_csv(file_path, skiprows=[1])
        df.rename(columns={"Price": "Date"}, inplace=True)

    # Convert data types
    df["Date"] = pd.to_datetime(df["Date"])
    df["Close"] = pd.to_numeric(df["Close"], errors="coerce")

    df = df.dropna()

    # -------------------------------------------------
    # Daily Returns
    # -------------------------------------------------
    df["Daily Return"] = df["Close"].pct_change()

    df = df.dropna()

    # -------------------------------------------------
    # Value at Risk (95%)
    # -------------------------------------------------
    confidence_level = 0.05

    VaR = np.percentile(
        df["Daily Return"],
        confidence_level * 100
    )

    # -------------------------------------------------
    # Sharpe Ratio
    # -------------------------------------------------
    daily_rf = risk_free_rate / 252

    excess_returns = df["Daily Return"] - daily_rf

    sharpe_ratio = (
        np.sqrt(252)
        * excess_returns.mean()
        / excess_returns.std()
    )

    # -------------------------------------------------
    # Statistics
    # -------------------------------------------------
    average_return = df["Daily Return"].mean()

    volatility = df["Daily Return"].std()

    maximum_return = df["Daily Return"].max()

    minimum_return = df["Daily Return"].min()

    # -------------------------------------------------
    # Save Results
    # -------------------------------------------------
    summary = pd.DataFrame({

        "Asset":[asset],

        "Average Daily Return":[average_return],

        "Volatility":[volatility],

        "Value at Risk (95%)":[VaR],

        "Sharpe Ratio":[sharpe_ratio],

        "Maximum Return":[maximum_return],

        "Minimum Return":[minimum_return]

    })

    summary.to_csv(

        os.path.join(
            OUTPUT_DIR,
            f"{asset}_risk_metrics.csv"
        ),

        index=False

    )

    print(summary)

print("\nRisk analysis completed successfully.")