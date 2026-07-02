import os
import yfinance as yf

# Create output directory
os.makedirs("data/processed", exist_ok=True)

tickers = ["TSLA", "BND", "SPY"]

for ticker in tickers:
    print(f"Downloading {ticker}...")

    df = yf.download(
        ticker,
        start="2015-01-01",
        end="2025-12-31",
        progress=False,
        auto_adjust=False
    )

    output_path = f"data/processed/{ticker}.csv"
    df.to_csv(output_path)

    print(f"Saved to {output_path}")

print("Download completed.")
