import os
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# Directory containing cleaned data
DATA_DIR = "data/processed"

assets = ["TSLA", "BND", "SPY"]

for asset in assets:

    print("=" * 70)
    print(f"Processing {asset}")

    file_path = os.path.join(DATA_DIR, f"{asset}.csv")

    df = pd.read_csv(file_path)

    # --------------------------------------------------
    # Fix the CSV if it contains multiple header rows
    # --------------------------------------------------
    if df.columns[0] == "Price":
        df = pd.read_csv(file_path, skiprows=[1])
        df.rename(columns={"Price": "Date"}, inplace=True)

    # --------------------------------------------------
    # Convert Date column
    # --------------------------------------------------
    df["Date"] = pd.to_datetime(df["Date"], utc=True).dt.tz_localize(None)

    # --------------------------------------------------
    # Convert numeric columns
    # --------------------------------------------------
    numeric_columns = [
        "Open",
        "High",
        "Low",
        "Close",
        "Adj Close",
        "Volume"
    ]

    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # --------------------------------------------------
    # Check missing values
    # --------------------------------------------------
    print("\nMissing Values")
    print(df.isnull().sum())

    # --------------------------------------------------
    # Handle missing values
    # --------------------------------------------------

    # Forward fill
    df = df.ffill()

    # Backward fill (for remaining missing values)
    df = df.bfill()

    # Remove rows that still contain missing values
    df = df.dropna()

    print("\nMissing Values After Cleaning")
    print(df.isnull().sum())

    # --------------------------------------------------
    # Remove duplicates
    # --------------------------------------------------
    df = df.drop_duplicates()

    # --------------------------------------------------
    # Normalize numerical columns
    # --------------------------------------------------
    scaler = MinMaxScaler()

    df[numeric_columns] = scaler.fit_transform(df[numeric_columns])

    # --------------------------------------------------
    # Save processed data
    # --------------------------------------------------
    output_file = os.path.join(
        DATA_DIR,
        f"{asset}_processed.csv"
    )

    df.to_csv(output_file, index=False)

    print(f"\nSaved {output_file}")

print("\nPreprocessing completed successfully!")