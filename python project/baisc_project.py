import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.arima.model import ARIMA
import warnings
warnings.filterwarnings("ignore")

# ✅ Load correct stock data
url = "https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv"
df = pd.read_csv(url, parse_dates=["Date"])
df.columns = df.columns.str.strip()  # Remove whitespace

# ✅ Check available columns
print("Columns in CSV:", df.columns.tolist())

# ✅ Use 'AAPL.Close' instead of 'Close' for this dataset
close_col = 'AAPL.Close'

# Preview and basic info
print("\nFirst 5 rows:")
print(df.head())
print("\nMissing values:\n", df.isnull().sum())

# Set Date as index
df.set_index("Date", inplace=True)

# Plot Closing Price
plt.plot(df[close_col], label='Close Price')
plt.title("Stock Closing Price Over Time")
plt.xlabel("Date")
plt.ylabel("Price")
plt.grid(True)
plt.legend()
plt.show()

# Moving Average (20 days)
df['MA20'] = df[close_col].rolling(window=20).mean()
plt.figure(figsize=(12, 6))
plt.plot(df[close_col], label='Close Price')
plt.plot(df['MA20'], label='20-Day MA', color='orange')
plt.title("20-Day Moving Average")
plt.xlabel("Date")
plt.ylabel("Price")
plt.legend()
plt.grid(True)
plt.show()

# Daily Return
df['Daily Return'] = df[close_col].pct_change()
plt.figure(figsize=(10, 4))
df['Daily Return'].hist(bins=50, color='skyblue', edgecolor='black')
plt.title("Daily Return Distribution")
plt.xlabel("Daily Return")
plt.grid(True)
plt.show()

# Cumulative Return
df['Cumulative Return'] = (1 + df['Daily Return']).cumprod()
plt.figure(figsize=(12, 5))
plt.plot(df['Cumulative Return'], label='Cumulative Return', color='purple')
plt.title("Cumulative Returns Over Time")
plt.xlabel("Date")
plt.ylabel("Cumulative Growth")
plt.grid(True)
plt.legend()
plt.show()

# Bollinger Bands
df['STD20'] = df[close_col].rolling(window=20).std()
df['Upper Band'] = df['MA20'] + (df['STD20'] * 2)
df['Lower Band'] = df['MA20'] - (df['STD20'] * 2)

plt.figure(figsize=(12, 6))
plt.plot(df[close_col], label='Close')
plt.plot(df['Upper Band'], label='Upper Band', linestyle='--', color='red')
plt.plot(plt.figure(figsize=(12, 6)))
plt.plot(df['Lower Band'],label='Lower Band', linestyle='--', color='green')
plt.fill_between(df.index, df['Lower Band'], df['Upper Band'], color='gray', alpha=0.1)
plt.title("Bollinger Bands")
plt.legend()
plt.grid(True)
plt.show()

# Correlation Heatmap
plt.figure(figsize=(8, 6))
sns.heatmap(df.corr(), annot=True, cmap="coolwarm")
plt.title("Feature Correlation")
plt.show()

# ARIMA Forecast (next 10 days)
model = ARIMA(df[close_col].dropna(), order=(5, 1, 0))
model_fit = model.fit()
forecast = model_fit.forecast(steps=10)

print("\nForecasted Prices (Next 10 Days):")
print(forecast)

plt.figure(figsize=(12, 6))
plt.plot(df[close_col], label="Historical")
plt.plot(pd.date_range(df.index[-1], periods=10, freq='D')[1:], forecast, label="Forecast", color="red")
plt.title("ARIMA Forecast - Next 10 Days")
plt.xlabel("Date")
plt.ylabel("Price")
plt.legend()
plt.grid(True)
plt.show()
# 📊 Plot Buy/Sell Signals
plt.figure(figsize=(14, 6))
plt.plot(df[close_col], label='Close Price', alpha=0.5)
plt.plot(df['MA20'], label='20-Day MA', linestyle='--')
plt.plot(df['MA50'], label='50-Day MA', linestyle='--')

# Mark Buy Signals
plt.plot(df[df['Position'] == 1].index, 
         df[close_col][df['Position'] == 1], 
         '^', markersize=10, color='green', label='Buy')

# Mark Sell Signals
plt.plot(df[df['Position'] == -1].index, 
         df[close_col][df['Position'] == -1], 
         'v', markersize=10, color='red', label='Sell')

plt.title("Buy/Sell Signals - MA Crossover Strategy")
plt.xlabel("Date")
plt.ylabel("Price")
plt.legend()
plt.grid(True)
plt.show()
