import yfinance as yf
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from streamlit_autorefresh import st_autorefresh  # ✅ Add this

# Set page layout
st.set_page_config(page_title="📈 Stock Analyzer", layout="wide")

# Auto-refresh every 60 seconds
st_autorefresh(interval=60 * 1000, key="refresh")

st.title("📊 Real-Time Stock Dashboard with Technical Indicators")
st.markdown("Supports stocks like **AAPL, TSLA** or index **^NSEI (Nifty 50)**")

# User input
ticker = st.text_input("Enter Stock Ticker (e.g., AAPL, TSLA, ^NSEI):", "^NSEI").upper()

# Fetch data
@st.cache_data(ttl=60)
def fetch_stock_data(ticker_symbol, period='1d', interval='1m'):
    stock = yf.Ticker(ticker_symbol)
    return stock.history(period=period, interval=interval)

# Add indicators
def add_indicators(data):
    data['SMA_10'] = data['Close'].rolling(window=10).mean()
    data['EMA_10'] = data['Close'].ewm(span=10, adjust=False).mean()
    delta = data['Close'].diff()
    gain = delta.clip(lower=0).rolling(14).mean()
    loss = -delta.clip(upper=0).rolling(14).mean()
    rs = gain / loss
    data['RSI_14'] = 100 - (100 / (1 + rs))
    exp1 = data['Close'].ewm(span=12, adjust=False).mean()
    exp2 = data['Close'].ewm(span=26, adjust=False).mean()
    data['MACD'] = exp1 - exp2
    data['Signal'] = data['MACD'].ewm(span=9, adjust=False).mean()
    return data

# Plot functions
def plot_price(data, ticker_symbol):
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(data.index, data['Close'], label='Close Price', linewidth=2)
    ax.plot(data.index, data['SMA_10'], label='SMA 10', linestyle='--')
    ax.plot(data.index, data['EMA_10'], label='EMA 10', linestyle='--', color='green')
    ax.set_title(f"{ticker_symbol} - Price, SMA & EMA")
    ax.grid(True)
    ax.legend()
    st.pyplot(fig)

def plot_rsi(data):
    fig, ax = plt.subplots(figsize=(12, 2.5))
    ax.plot(data.index, data['RSI_14'], label='RSI 14', color='purple')
    ax.axhline(70, linestyle='--', color='red', alpha=0.5)
    ax.axhline(30, linestyle='--', color='green', alpha=0.5)
    ax.set_title("RSI Indicator")
    ax.grid(True)
    ax.legend()
    st.pyplot(fig)

def plot_macd(data):
    fig, ax = plt.subplots(figsize=(12, 2.5))
    ax.plot(data.index, data['MACD'], label='MACD', color='blue')
    ax.plot(data.index, data['Signal'], label='Signal Line', linestyle='--', color='orange')
    ax.set_title("MACD Indicator")
    ax.grid(True)
    ax.legend()
    st.pyplot(fig)

# MAIN
if ticker:
    st.info(f"Fetching live data for **{ticker}**...")
    data = fetch_stock_data(ticker)

    if data.empty:
        st.error("❌ No data. Check your internet or ticker.")
    else:
        st.success("✅ Data fetched successfully!")
        st.dataframe(data.tail(5))

        data = add_indicators(data)
        plot_price(data, ticker)
        plot_rsi(data)
        plot_macd(data)
# === EXPORT SECTION ===
from io import BytesIO

# === EXPORT SECTION ===
st.subheader("📤 Export Data")

# Remove timezone info
data_export = data.copy()
data_export.index = data_export.index.tz_localize(None)

# Convert to CSV
csv = data_export.to_csv(index=True).encode('utf-8')
st.download_button(
    label="📁 Download CSV",
    data=csv,
    file_name=f'{ticker}_data.csv',
    mime='text/csv'
)

# Convert to Excel
output = BytesIO()
with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
    data_export.to_excel(writer, sheet_name='Stock Data')

st.download_button(
    label="📊 Download Excel",
    data=output.getvalue(),
    file_name=f'{ticker}_data.xlsx',
    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
)

