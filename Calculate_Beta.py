import streamlit as st
from pages.utils.model_train import calculate_beta

st.subheader("📘 Beta Calculation")

ticker = st.text_input("Stock Ticker", "TSLA")

benchmark = st.selectbox(
    "Choose Benchmark Index",
    options=["S&P 500 (^GSPC)", "Nifty 50 (^NSEI)", "Nasdaq (^IXIC)"]
)

benchmark_map = {
    "S&P 500 (^GSPC)": "^GSPC",
    "Nifty 50 (^NSEI)": "^NSEI",
    "Nasdaq (^IXIC)": "^IXIC"
}

beta_value = calculate_beta(ticker, benchmark_map[benchmark], "1y")

st.metric("Stock Beta (1-Year)", beta_value)
