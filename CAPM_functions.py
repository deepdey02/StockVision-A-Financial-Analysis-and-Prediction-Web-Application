import plotly.express as px
import numpy as np

#fucntion to plot interactive plotly chart
def interactive_plot(df):
    fig = px.line()
    for i in df.columns[1:]:
        fig.add_scatter(x=df[df.columns[0]], y=df[i], mode='lines', name=i)
    fig.update_layout(width = 450, margin = dict(l=20, r=20, t=50, b=20), legend = dict(orientation = 'h', yanchor = 'bottom', y=1.02, xanchor='right', x=1))
    return fig

# function to normalize the prices based on the initial price
def normalize(df_2):
    df = df_2.copy()
    for i in df.columns[1:]:
        df[i] = df[i]/df[i][0]
    return df 

# function to calculate daily returns
def daily_returns(df):
    df_daily_returns = df.copy()
    for i in df.columns[1:]:
        for j in range(1, len(df)):
            df_daily_returns[i][j] = (df_daily_returns[i][j] - df_daily_returns[i][j-1]) / df_daily_returns[i][j-1]*100
        df_daily_returns[i][0] = 0
    return df_daily_returns

# function to calculate beta values
def calculate_beta(stocks_daily_returns, stock):
    b, a = np.polyfit(stocks_daily_returns['SP500'], stocks_daily_returns[stock], 1)
    return b, a
   