import os
import pandas as pd
import matplotlib.pyplot as plt

# Directories
DATA_DIR = "data/processed"
OUTPUT_DIR = "data/eda"

os.makedirs(OUTPUT_DIR, exist_ok=True)

assets = ["TSLA", "BND", "SPY"]

# Rolling window size (30 trading days ≈ 1 month)
WINDOW = 30

for asset in assets:

    print("=" * 70)
    print(f"Rolling Analysis: {asset}")

    file_path = os.path.join(DATA_DIR, f"{asset}.csv")

    # Read data
    df = pd.read_csv(file_path)

    # Handle CSVs saved with an extra header row
    if df.columns[0] == "Price":
        df = pd.read_csv(file_path, skiprows=[1])
        df.rename(columns={"Price": "Date"}, inplace=True)

    # Convert Date column
    df["Date"] = pd.to_datetime(df["Date"])

    # Convert Close column to numeric
    df["Close"] = pd.to_numeric(df["Close"], errors="coerce")

    # Remove missing values
    df = df.dropna(subset=["Close"])

    # Calculate rolling statistics
    df["Rolling Mean"] = df["Close"].rolling(window=WINDOW).mean()
    df["Rolling Std"] = df["Close"].rolling(window=WINDOW).std()

    # Plot Close Price and Rolling Mean
    plt.figure(figsize=(12, 6))
    plt.plot(df["Date"], df["Close"], label="Close Price")
    plt.plot(df["Date"], df["Rolling Mean"], label=f"{WINDOW}-Day Rolling Mean")
    plt.title(f"{asset} Closing Price with Rolling Mean")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(OUTPUT_DIR, f"{asset}_rolling_mean.png"))
    plt.close()

    # Plot Rolling Standard Deviation
    plt.figure(figsize=(12, 6))
    plt.plot(df["Date"], df["Rolling Std"])
    plt.title(f"{asset} {WINDOW}-Day Rolling Standard Deviation")
    plt.xlabel("Date")
    plt.ylabel("Standard Deviation")
    plt.grid(True)
    plt.savefig(os.path.join(OUTPUT_DIR, f"{asset}_rolling_std.png"))
    plt.close()

    # Save results
    output_csv = os.path.join(
        OUTPUT_DIR,
        f"{asset}_rolling_statistics.csv"
    )

    df.to_csv(output_csv, index=False)

    print(f"Saved {output_csv}")

print("\nRolling analysis completed successfully.")