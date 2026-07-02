import os
import yfinance as yf

os.makedirs("data/processed", exist_ok=True)

tickers = ["TSLA", "BND", "SPY"]

df = yf.download(
    tickers,
    start="2015-01-01",
    end="2025-12-31",
    group_by="ticker",
    progress=False
)

df.to_csv("data/processed/portfolio_data.csv")

print("Portfolio data downloaded successfully!")