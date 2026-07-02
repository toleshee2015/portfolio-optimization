import yfinance as yf

df = yf.download(
    "BND",
    start="2015-01-01",
    end="2025-12-31",
    progress=False,
    auto_adjust=False
)

print(df.head())
print(df.shape)