#Importing libraries 

from datetime import datetime
import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
import datetime
import pandas_datareader.data as web
import CAPM_functions as CAPM_functions

st.set_page_config(page_title="CAPM Return Calculator", 
                   page_icon=":chart_with_upwards_trend",
                     layout="wide")

st.title("Capital Asset Pricing Model")

#getting user input 

col1, col2 = st.columns([1,1])
with col1:
   stocks_list = st.multiselect("Choose 4 stocks",('TSLA','AAPL','MSFT','AMZN','NFLX','GOOGL','META','NVDA','JPM'),default=['TSLA','AAPL','MSFT'],key='stocks')
with col2:
   year = st.number_input("Enter the number of years", min_value=1, max_value=10, value=1)

# downloading data for selected stocks SP500 as market index
try:
    # -------------------------
    # DOWNLOAD MARKET DATA
    # -------------------------

    end = datetime.date.today()
    start = datetime.date(datetime.date.today().year - year,
                          datetime.date.today().month,
                          datetime.date.today().day)

    SP500 = web.DataReader(['sp500'], 'fred', start, end)
    SP500.reset_index(inplace=True)
    SP500.columns = ['Date', 'SP500']
    SP500['Date'] = pd.to_datetime(SP500['Date']).dt.normalize()

    # -------------------------
    # DOWNLOAD STOCK DATA
    # -------------------------

    stocks_df = pd.DataFrame()

    for stock in stocks_list:
        data = yf.download(stock, period=f'{year}y')
        if data.empty:
            st.error(f"Failed to download data for {stock}.")
            continue
        stocks_df[stock] = data['Close']

    stocks_df.reset_index(inplace=True)
    stocks_df['Date'] = pd.to_datetime(stocks_df['Date']).dt.normalize()

    # -------------------------
    # MERGE STOCKS + SP500
    # -------------------------

    stocks_df = pd.merge(stocks_df, SP500, on='Date', how='inner')

    # Display dataframe
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("### Dataframe head")
        st.dataframe(stocks_df.head(), use_container_width=True)
    with col2:
        st.markdown("### Dataframe tail")
        st.dataframe(stocks_df.tail(), use_container_width=True)

    # -------------------------
    # PLOTS
    # -------------------------

    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("### Interactive stock prices chart")
        fig = CAPM_functions.interactive_plot(stocks_df)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### Price of all the stock normalized")
        norm_fig = CAPM_functions.interactive_plot(
            CAPM_functions.normalize(stocks_df)
        )
        st.plotly_chart(norm_fig, use_container_width=True)

    # -------------------------
    # DAILY RETURNS
    # -------------------------

    stocks_daily_returns = CAPM_functions.daily_returns(stocks_df)

    # -------------------------
    # CALCULATE BETA & ALPHA
    # -------------------------

    beta = {}
    alpha = {}

    for col in stocks_daily_returns.columns:
        if col not in ['Date', 'SP500']:
            b, a = CAPM_functions.calculate_beta(stocks_daily_returns, col)
            beta[col] = b
            alpha[col] = a

    beta_df = pd.DataFrame({
        "Stock": beta.keys(),
        "Beta Value": [round(v, 2) for v in beta.values()]
    })

    with col1:
        st.markdown("### Calculated Beta Values")
        st.dataframe(beta_df, use_container_width=True)

    # -------------------------
    # CAPM RETURN CALCULATION
    # -------------------------

    rf = 0  # risk-free rate
    rm = stocks_daily_returns['SP500'].mean() * 252

    return_value = [
        round(rf + (b * (rm - rf)), 2) for b in beta.values()
    ]

    return_df = pd.DataFrame({
        "Stock": list(beta.keys()),
        "Return Value": return_value
    })

    with col2:
        st.markdown("### Calculated Return using CAPM")

        st.dataframe(return_df, use_container_width=True)
except:
    st.write('Please select valid inputs')
  