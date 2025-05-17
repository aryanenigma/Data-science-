import yfinance as yf
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
def fetch_stock_data(ticker_symbol, period='1d', interval='1m'):
    stock = yf.Ticker(ticker_symbol)
    data = stock.history(period=period, interval=interval)
    return data

# Function to perform basic analysis
def analyze_data(data):
    print("\n🔍 Summary Statistics:")
    print(data.describe())

    # Calculate simple moving average
    data['SMA_10'] = data['Close'].rolling(window=10).mean()

    return data

# Function to plot stock price and SMA
def plot_data(data, ticker_symbol):
    plt.figure(figsize=(12, 6))
    plt.plot(data['Close'], label='Close Price', linewidth=2)
    plt.plot(data['SMA_10'], label='SMA 10', linestyle='--')
    plt.title(f"{ticker_symbol} - Real-Time Price with SMA")
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# === MAIN PROGRAM =

if __name__ == "__main__":
    ticker = input("Enter the stock ticker symbol (e.g., AAPL, TSLA, ^NSEI): ").upper()
    print(f"\n📈 Fetching real-time data for {ticker}...")

    stock_data = fetch_stock_data(ticker)

    if stock_data.empty:
        print("⚠️ No data fetched. Check the ticker or your internet connection.")
    else:
        print(stock_data.tail())  # Show last few rows for confirmation
        stock_data = analyze_data(stock_data)
        plot_data(stock_data, ticker)
    st.title("📊 Real-Time Stock Analyzer with SMA")
st.markdown("Supports stocks like **AAPL, TSLA** or indices like **^NSEI (Nifty 50)**")

# User input
ticker = st.text_input("Enter Stock Ticker (e.g., AAPL, TSLA, ^NSEI):", "^NSEI").upper()

# Function to fetch stock data
@st.cache_data(ttl=60)  # Cache data for 60 seconds to auto-refresh periodically
def fetch_stock_data(ticker_symbol, period='1d', interval='1m'):
    stock = yf.Ticker(ticker_symbol)
    return stock.history(period=period, interval=interval)

# Function to analyze and add SMA
def analyze_data(data):
    data['SMA_10'] = data['Close'].rolling(window=10).mean()
    return data

# Function to plot data
def plot_data(data, ticker_symbol):
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(data.index, data['Close'], label='Close Price', linewidth=2)
    ax.plot(data.index, data['SMA_10'], label='SMA 10', linestyle='--', color='orange')
    ax.set_title(f"{ticker_symbol} - Price with SMA")
    ax.set_xlabel("Time")
    ax.set_ylabel("Price")
    ax.grid(True)
    ax.legend()
    st.pyplot(fig)

# MAIN APP LOGIC
if ticker:
    st.info(f"Fetching live data for **{ticker}**...")
    data = fetch_stock_data(ticker)

    if data.empty:
        st.error("❌ No data fetched. Check your internet or ticker symbol.")
    else:
        st.success("✅ Data fetched successfully!")
        st.dataframe(data.tail(10))  # Show latest 10 rows

        data = analyze_data(data)
        plot_data(data, ticker)
