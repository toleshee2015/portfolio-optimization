import os
import pandas as pd
import matplotlib.pyplot as plt

DATA_DIR = "data/processed"
OUTPUT_DIR = "data/eda"

os.makedirs(OUTPUT_DIR, exist_ok=True)

assets = ["TSLA", "BND", "SPY"]

for asset in assets:

    print("=" * 70)
    print(f"Analyzing {asset}")

    file_path = os.path.join(DATA_DIR, f"{asset}.csv")

    df = pd.read_csv(file_path)

    # Handle CSVs with an extra header row
    if df.columns[0] == "Price":
        df = pd.read_csv(file_path, skiprows=[1])
        df.rename(columns={"Price": "Date"}, inplace=True)

    # Convert Date
    df["Date"] = pd.to_datetime(df["Date"], utc=True).dt.tz_localize(None)

    # Convert numeric columns
    numeric_cols = ["Open", "High", "Low", "Close", "Adj Close", "Volume"]

    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna()

    # =====================================================
    # 1. Closing Price
    # =====================================================
    plt.figure(figsize=(12,6))
    plt.plot(df["Date"], df["Close"])
    plt.title(f"{asset} Closing Price")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.grid(True)

    plt.savefig(
        os.path.join(OUTPUT_DIR, f"{asset}_closing_price.png")
    )

    plt.close()

    # =====================================================
    # 2. Daily Percentage Return
    # =====================================================
    df["Daily Return"] = df["Close"].pct_change() * 100

    plt.figure(figsize=(12,6))
    plt.plot(df["Date"], df["Daily Return"])
    plt.title(f"{asset} Daily Percentage Return")
    plt.xlabel("Date")
    plt.ylabel("Return (%)")
    plt.grid(True)

    plt.savefig(
        os.path.join(OUTPUT_DIR, f"{asset}_daily_return.png")
    )

    plt.close()

    # =====================================================
    # 3. Rolling Mean & Rolling Std
    # =====================================================
    window = 30

    df["Rolling Mean"] = df["Close"].rolling(window).mean()

    df["Rolling Std"] = df["Close"].rolling(window).std()

    plt.figure(figsize=(12,6))

    plt.plot(df["Date"], df["Close"], label="Close")

    plt.plot(df["Date"], df["Rolling Mean"], label="30-Day Mean")

    plt.plot(df["Date"], df["Rolling Std"], label="30-Day Std")

    plt.legend()

    plt.title(f"{asset} Rolling Statistics")

    plt.grid(True)

    plt.savefig(
        os.path.join(OUTPUT_DIR, f"{asset}_rolling_statistics.png")
    )

    plt.close()

    # =====================================================
    # 4. Outlier Detection (IQR)
    # =====================================================
    Q1 = df["Daily Return"].quantile(0.25)

    Q3 = df["Daily Return"].quantile(0.75)

    IQR = Q3 - Q1

    lower = Q1 - 1.5 * IQR

    upper = Q3 + 1.5 * IQR

    outliers = df[
        (df["Daily Return"] < lower) |
        (df["Daily Return"] > upper)
    ]

    print(f"\nOutliers detected: {len(outliers)}")

    outliers.to_csv(
        os.path.join(
            OUTPUT_DIR,
            f"{asset}_outliers.csv"
        ),
        index=False
    )

    # =====================================================
    # 5. Highest & Lowest Returns
    # =====================================================
    print("\nTop 5 Highest Returns")

    print(
        df.nlargest(
            5,
            "Daily Return"
        )[["Date", "Daily Return"]]
    )

    print("\nTop 5 Lowest Returns")

    print(
        df.nsmallest(
            5,
            "Daily Return"
        )[["Date", "Daily Return"]]
    )

print("\nEDA completed successfully!")