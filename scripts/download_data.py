import os
import yfinance as yf

<<<<<<< HEAD
=======
# Create output directory
>>>>>>> 496ad33a97fc7c4f611fa6c58f128906edc5dcab
os.makedirs("data/processed", exist_ok=True)

tickers = ["TSLA", "BND", "SPY"]

for ticker in tickers:
<<<<<<< HEAD

=======
>>>>>>> 496ad33a97fc7c4f611fa6c58f128906edc5dcab
    print(f"Downloading {ticker}...")

    df = yf.download(
        ticker,
        start="2015-01-01",
        end="2025-12-31",
<<<<<<< HEAD
        auto_adjust=False,
        progress=False
    )

    # Flatten MultiIndex columns if present
    if hasattr(df.columns, "nlevels") and df.columns.nlevels > 1:
        df.columns = df.columns.get_level_values(0)

    # Convert index to Date column
    df.reset_index(inplace=True)

    # Add asset identifier
    df["Asset"] = ticker

    output = f"data/processed/{ticker}.csv"
    df.to_csv(output, index=False)

    print(f"Saved {output}")

print("Done!")
=======
        progress=False,
        auto_adjust=False
    )

    output_path = f"data/processed/{ticker}.csv"
    df.to_csv(output_path)

    print(f"Saved to {output_path}")

print("Download completed.")
>>>>>>> 496ad33a97fc7c4f611fa6c58f128906edc5dcab
