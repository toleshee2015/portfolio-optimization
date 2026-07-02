import os
import pandas as pd
import matplotlib.pyplot as plt

# Directories
DATA_DIR = "data/processed"
OUTPUT_DIR = "data/eda"

os.makedirs(OUTPUT_DIR, exist_ok=True)

assets = ["TSLA", "BND", "SPY"]

for asset in assets:

    print("=" * 70)
    print(f"Analyzing {asset}")

    file_path = os.path.join(DATA_DIR, f"{asset}.csv")

    # Read data
    df = pd.read_csv(file_path)

    # Handle CSVs with an extra header row
    if df.columns[0] == "Price":
        df = pd.read_csv(file_path, skiprows=[1])
        df.rename(columns={"Price": "Date"}, inplace=True)

    # Convert Date
    df["Date"] = pd.to_datetime(df["Date"])

    # Convert Close to numeric
    df["Close"] = pd.to_numeric(df["Close"], errors="coerce")

    # Remove missing values
    df = df.dropna(subset=["Close"])

    # -------------------------------------------------------
    # Calculate Daily Returns
    # -------------------------------------------------------
    df["Daily Return"] = df["Close"].pct_change() * 100

    df = df.dropna()

    # -------------------------------------------------------
    # IQR Outlier Detection
    # -------------------------------------------------------
    Q1 = df["Daily Return"].quantile(0.25)
    Q3 = df["Daily Return"].quantile(0.75)

    IQR = Q3 - Q1

    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR

    outliers = df[
        (df["Daily Return"] < lower) |
        (df["Daily Return"] > upper)
    ]

    print(f"\nTotal Outliers: {len(outliers)}")

    # Save outliers
    outliers.to_csv(
        os.path.join(
            OUTPUT_DIR,
            f"{asset}_outliers.csv"
        ),
        index=False
    )

    # -------------------------------------------------------
    # Highest Returns
    # -------------------------------------------------------
    highest = df.nlargest(10, "Daily Return")

    print("\nTop 10 Highest Return Days")
    print(highest[["Date", "Daily Return"]])

    highest.to_csv(
        os.path.join(
            OUTPUT_DIR,
            f"{asset}_highest_returns.csv"
        ),
        index=False
    )

    # -------------------------------------------------------
    # Lowest Returns
    # -------------------------------------------------------
    lowest = df.nsmallest(10, "Daily Return")

    print("\nTop 10 Lowest Return Days")
    print(lowest[["Date", "Daily Return"]])

    lowest.to_csv(
        os.path.join(
            OUTPUT_DIR,
            f"{asset}_lowest_returns.csv"
        ),
        index=False
    )

    # -------------------------------------------------------
    # Plot Daily Returns with Outliers
    # -------------------------------------------------------
    plt.figure(figsize=(14,6))

    plt.plot(
        df["Date"],
        df["Daily Return"],
        label="Daily Return"
    )

    plt.scatter(
        outliers["Date"],
        outliers["Daily Return"],
        color="red",
        label="Outliers"
    )

    plt.axhline(upper, linestyle="--", label="Upper Limit")
    plt.axhline(lower, linestyle="--", label="Lower Limit")

    plt.title(f"{asset} Daily Returns with Outliers")
    plt.xlabel("Date")
    plt.ylabel("Daily Return (%)")

    plt.legend()

    plt.grid(True)

    plt.savefig(
        os.path.join(
            OUTPUT_DIR,
            f"{asset}_outlier_plot.png"
        )
    )

    plt.close()

print("\nOutlier analysis completed successfully!")