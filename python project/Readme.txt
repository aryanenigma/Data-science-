📊 Real-Time Stock Analyzer with Streamlit
This project is a real-time stock and index analyzer built using Streamlit, yfinance, and Python. It fetches live stock data, applies basic analysis like Simple Moving Average (SMA), plots interactive charts, and allows users to export data to CSV or Excel.

🚀 Features
📈 Real-time stock price visualization (1-minute interval)

🧠 Calculates 10-period Simple Moving Average (SMA)

🖼 Matplotlib chart embedded in Streamlit UI

🔄 Auto-refresh-friendly architecture (via caching with TTL)

💾 Export stock data to CSV and Excel formats

✅ Supports NSE (Nifty 50), US stocks, and global indices

🧰 Tech Stack
Python 3.8+

Streamlit

yfinance

pandas

matplotlib

xlsxwriter

📦 Installation
Clone the repo

bash
Copy
Edit
git clone https://github.com/yourusername/stock-analyzer.git
cd stock-analyzer
Create a virtual environment (optional but recommended)

bash
Copy
Edit
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install dependencies

bash
Copy
Edit
pip install -r requirements.txt
Example requirements.txt:

txt
Copy
Edit
streamlit
yfinance
pandas
matplotlib
xlsxwriter
▶️ Run the App
bash
Copy
Edit
streamlit run app.py
Then open your browser to http://localhost:8501 to see the dashboard.

📤 Export Example
After fetching and visualizing data, scroll down to the 📤 Export Data section to:

📁 Download raw stock data as .csv

📊 Download full data as Excel .xlsx (with SMA)

🖼 Sample Screenshot
(Add your screenshot here)

📌 Sample Tickers
US Stocks: AAPL, MSFT, TSLA

Indian Index: ^NSEI (Nifty 50), ^BSESN (Sensex)

Crypto: BTC-USD, ETH-USD

Forex: EURUSD=X, INR=X

🛠️ To-Do / Future Features
⏱ Auto-refresh dashboard every 60 seconds

📈 Add more technical indicators (EMA, RSI, MACD)

📬 Email/notify when SMA crossover happens

📱 Deploy to Streamlit Cloud or Hugging Face Spaces

🤝 Contributing
Pull requests are welcome! For major changes, open an issue first to discuss what you'd like to add or improve.

📄 License
MIT

Let me know if you want a requirements.txt or a deployment guide for Streamlit Cloud or Docker.







 