import pandas as pd
import os

DATA_DIR = "data/processed"
ASSETS = ["TSLA", "BND", "SPY"]

for asset in ASSETS:

    print("\n" + "="*70)
    print(f"Analyzing {asset}")

    file_path = os.path.join(DATA_DIR, f"{asset}.csv")

    df = pd.read_csv(file_path)

    # Convert Date column safely
    df["Date"] = pd.to_datetime(
        df["Date"],
        utc=True,
        errors="coerce"
    ).dt.tz_localize(None)

    print("\nDataset Shape:")
    print(df.shape)

    print("\nColumn Names:")
    print(df.columns.tolist())

    print("\nData Types:")
    print(df.dtypes)

    print("\nMissing Values:")
    print(df.isnull().sum())

    print("\nDuplicate Records:")
    print(df.duplicated().sum())

    # Remove duplicates if any
    df = df.drop_duplicates()

    print("\nDescriptive Statistics:")
    print(df.describe())

    # Save cleaned dataset
    output_file = os.path.join(
        DATA_DIR,
        f"{asset}_clean.csv"
    )

    df.to_csv(output_file, index=False)

    print(f"\nCleaned file saved: {output_file}")

print("\nData cleaning completed successfully.")