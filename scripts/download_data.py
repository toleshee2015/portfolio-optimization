import os
import yfinance as yf

os.makedirs("data/processed", exist_ok=True)

tickers = ["TSLA", "BND", "SPY"]

for ticker in tickers:

    print(f"Downloading {ticker}...")

    df = yf.download(
        ticker,
        start="2015-01-01",
        end="2025-12-31",
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