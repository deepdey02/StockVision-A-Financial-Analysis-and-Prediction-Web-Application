import datetime
import dateutil
import pandas as pd
import plotly.graph_objects as go
import pandas_ta as pta

def plotly_table(dataframe):
    headerColor = "grey"
    rowEvenColor = "#FFFFFF"
    rowOddColor = "#fdfdfd"

    fig = go.Figure(data=[go.Table(
        header=dict(
            values=[f"<b>{str(i)[:10]}</b>" for i in dataframe.columns],
            line_color="#000000",
            fill_color="#060606",
            align="center",
            font=dict(color="white", size=15),
            height=35
        ),
        cells=dict(
            values=[[f"<b>{str(i)}</b>" for i in dataframe.index]] +
                   [dataframe[i] for i in dataframe.columns],
            line_color="white",
            fill_color=[rowOddColor, rowEvenColor],
            align="left",
            font=dict(color="black", size=15)
        )
    )])

    fig.update_layout(
        height=400,
        margin=dict(l=0, r=0, t=0, b=0)
    )
    return fig

def filter_data(dataframe, num_period):
    last_idx = dataframe.index[-1]

    if num_period == '1mo':
        date = last_idx - dateutil.relativedelta.relativedelta(months=1)

    elif num_period == '5d':
        date = last_idx - dateutil.relativedelta.relativedelta(days=5)

    elif num_period == '6mo':
        date = last_idx - dateutil.relativedelta.relativedelta(months=6)

    elif num_period == '1y':
        date = last_idx - dateutil.relativedelta.relativedelta(years=1)

    elif num_period == '5y':
        date = last_idx - dateutil.relativedelta.relativedelta(years=5)

    elif num_period == 'ytd':
        date = datetime.datetime(last_idx.year, 1, 1)

    else:
        date = dataframe.index[0]

    # ---- Normalise timezone in DATE --------------------------
    if hasattr(date, 'tzinfo') and date.tzinfo is not None:
        try:
            date = date.tz_convert(None)   # pandas Timestamp
        except:
            date = date.replace(tzinfo=None)   # python datetime
    # -----------------------------------------------------------

    df_reset = dataframe.reset_index()

    # ---- Normalize timezone in DataFrame Date column ----------
    df_reset['Date'] = pd.to_datetime(df_reset['Date'])
    df_reset['Date'] = df_reset['Date'].dt.tz_localize(None)
    # ------------------------------------------------------------

    return df_reset[df_reset['Date'] > date]


def close_chart(dataframe, num_period=False):
    if num_period:
        dataframe = filter_data(dataframe, num_period)

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=dataframe['Date'],
        y=dataframe['Open'],
        mode='lines',
        name='Open',
        line=dict(width=2, color="#000000")
    ))

    fig.add_trace(go.Scatter(
        x=dataframe['Date'],
        y=dataframe['Close'],
        mode='lines',
        name='Close',
        line=dict(width=2, color='black')
    ))

    fig.add_trace(go.Scatter(
        x=dataframe['Date'],
        y=dataframe['High'],
        mode='lines',
        name='High',
        line=dict(width=2, color="#FFFFFF")
    ))

    fig.add_trace(go.Scatter(
        x=dataframe['Date'],
        y=dataframe['Low'],
        mode='lines',
        name='Low',
        line=dict(width=2, color='red')
    ))

    fig.update_xaxes(rangeslider_visible=True)

    fig.update_layout(
        height=500,
        margin=dict(l=0, r=20, t=20, b=0),
        plot_bgcolor='white',
        paper_bgcolor='#e1efff',
        legend=dict(
            xanchor='right',
            yanchor='top'
        )
    )
    return fig


def candlestick(dataframe, num_period):
    dataframe = filter_data(dataframe, num_period)

    fig = go.Figure()

    fig.add_trace(go.Candlestick(
        x=dataframe['Date'],
        open=dataframe['Open'],
        high=dataframe['High'],
        low=dataframe['Low'],
        close=dataframe['Close'],
        name='Candlestick'
    ))

    # enable rangeslider for consistency with other charts
    fig.update_layout(
        showlegend=False,
        height=500,
        margin=dict(l=0, r=20, t=20, b=0),
        plot_bgcolor='white',
        paper_bgcolor='#e1efff',
    )
    fig.update_xaxes(rangeslider_visible=True)
    return fig


def RSI(dataframe, num_period):
    dataframe['RSI'] = pta.rsi(dataframe['Close'])

    dataframe = filter_data(dataframe, num_period)

    fig = go.Figure()

    # RSI Line
    fig.add_trace(go.Scatter(
        x=dataframe['Date'],
        y=dataframe['RSI'],
        name='RSI',
        marker_color='orange',
        line=dict(width=2, color='orange')
    ))

    # Overbought line (70)
    fig.add_trace(go.Scatter(
        x=dataframe['Date'],
        y=[70] * len(dataframe),
        name='Overbought',
        marker_color='red',
        line=dict(width=2, color='red', dash='dash')
    ))

    # Oversold line (30)
    fig.add_trace(go.Scatter(
        x=dataframe['Date'],
        y=[30] * len(dataframe),
        name='Oversold',
        marker_color='#79da84',
        line=dict(width=2, color='#79da84', dash='dash')
    ))

    fig.update_layout(
        yaxis=dict(range=[0, 100]),
        height=200,
        plot_bgcolor='white',
        paper_bgcolor='#e1efff',
        margin=dict(l=0, r=0, t=0, b=0),
        legend=dict(orientation="h", y=1.02, x=1, xanchor="right")
    )

    return fig


def Moving_average(dataframe, num_period):
    # use standard rolling
    dataframe['SMA_50'] = dataframe['Close'].rolling(window=50).mean()
    dataframe = filter_data(dataframe, num_period)

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=dataframe['Date'], y=dataframe['Open'],
        mode='lines',
        name='Open',
        line=dict(width=2, color="#D8DEE3")
    ))

    fig.add_trace(go.Scatter(
        x=dataframe['Date'], y=dataframe['Close'],
        mode='lines',
        name='Close',
        line=dict(width=2, color='black')
    ))

    fig.add_trace(go.Scatter(
        x=dataframe['Date'], y=dataframe['High'],
        mode='lines',
        name='High',
        line=dict(width=2, color="#eaeef2")
    ))

    fig.add_trace(go.Scatter(
        x=dataframe['Date'], y=dataframe['Low'],
        mode='lines',
        name='Low',
        line=dict(width=2, color='red')
    ))

    fig.add_trace(go.Scatter(
        x=dataframe['Date'], y=dataframe['SMA_50'],
        mode='lines',
        name='SMA 50',
        line=dict(width=2, color='purple')
    ))

    fig.update_xaxes(rangeslider_visible=True)

    fig.update_layout(
        height=500,
        margin=dict(l=20, r=20, t=20, b=20),
        plot_bgcolor='white',
        paper_bgcolor='#e1efff',
        legend=dict(yanchor="top", xanchor="right")
    )

    return fig


def MACD(dataframe, num_period):
    macd_df = pta.macd(dataframe['Close'])
    # adapt to how pandas_ta returns columns
    # common column names: 'MACD', 'MACDs_12_26_9', 'MACDh_12_26_9'
    dataframe['MACD'] = macd_df.get('MACD')
    dataframe['MACD Signal'] = macd_df.get('MACDs_12_26_9')
    dataframe['MACD Hist'] = macd_df.get('MACDh_12_26_9')

    dataframe = filter_data(dataframe, num_period)

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=dataframe['Date'],
        y=dataframe['MACD'],
        name='MACD',
        marker_color='orange',
        line=dict(width=2, color='orange')
    ))

    fig.add_trace(go.Scatter(
        x=dataframe['Date'],
        y=dataframe['MACD Signal'],
        name='Signal',
        marker_color='red',
        line=dict(width=2, color='red', dash='dash')
    ))

    # (optional) histogram coloring if you want to display bars:
    # fig.add_trace(go.Bar(x=dataframe['Date'], y=dataframe['MACD Hist'],
    #                      marker=dict(color=['red' if v < 0 else 'green' for v in dataframe['MACD Hist']]),
    #                      name='MACD Hist'))

    fig.update_layout(
        height=200,
        plot_bgcolor='white',
        paper_bgcolor='#e1efff',
        margin=dict(l=0, r=0, t=0, b=0),
        legend=dict(orientation='h', yanchor="top", xanchor="right", x=1)
    )

    return fig

def Moving_average_forecast(forecast):
    fig = go.Figure()

    # Past Close Price (last 30 days)
    fig.add_trace(go.Scatter(
        x=forecast.index[-30:],
        y=forecast['Close'].iloc[-30:],
        mode='lines',
        name='Close Price',
        line=dict(width=2, color='black')
    ))

    # Future Forecast Price (next 30 days)
    fig.add_trace(go.Scatter(
        x=forecast.index[-31:],
        y=forecast['Close'].iloc[-31:],
        mode='lines',
        name='Future Close Price',
        line=dict(width=2, color='red')
    ))

    fig.update_xaxes(rangeslider_visible=True)
    fig.update_layout(
        height=500,
        margin=dict(l=0, r=20, t=20, b=0),
        plot_bgcolor='white',
        paper_bgcolor="#205da2",
        legend=dict(
            yanchor="top",
            xanchor="right"
        )
    )

    return fig
