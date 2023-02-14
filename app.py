## SWAPNIL BISWAS  SCAAI

## importing all the necessary libraries

import nsepy as nse
from datetime import date

import pandas as pd
import numpy as np
import streamlit as st

import plotly.express as px
import plotly.graph_objs as go

from stocknews import StockNews

## *********************************************************** ##

## TITLE OF THE WEBSITE
st.title("STOCKET")

## making user-interactive for the user to choose its equity options
ticker = st.sidebar.text_input('SYMBOL')
start_date = st.sidebar.date_input('Start Date')
end_date = st.sidebar.date_input('End Date')


## extracting the live data from the NSE website
Stock_symbol = ticker

stock_data = nse.get_history(Stock_symbol, start = start_date, end = end_date)
stock_data


## making the margin topics tabs
portfolio_info, pricing_data, visualizations, tutorial, news, technical_analysis, model,ChatGPT = st.tabs(["Portfolio information", "Pricing Data", "Portfolio Analysis", "How to Read Charts", "Top 10 Stock News", "Technical Analysis Dashboard", "ML MODEL","CHAT_GPT"])

with portfolio_info:
    ## Getting the live status of the given portfolio
    Quote = st.button("Status of the portfolio")
    st.write(Quote)

    if Quote:
        quote = nse.live.get_quote(Stock_symbol)
        st.subheader("Status of the Market Portfolio")
        pd.DataFrame(quote['data']).T 

## showing the price movements of the given portfolio
with pricing_data:
    st.header("Price Movements")
    
    ## calculating the percentage change
    st.subheader('Percentage Change')
    Percentage_change = stock_data['% Change'] = ((stock_data['Close'] - stock_data['Prev Close']) / stock_data['Prev Close']) * 100
    stock_data.dropna(inplace=True)
    st.write(Percentage_change)
    
    ## calculating the annual change
    st.subheader('Annual Return')
    ## we are taking 261 since the market is close on weekends so whole year - weekends
    annual_return = stock_data['% Change'].mean()*261*100
    st.write('Annual Return is: ',annual_return, '%')

    ## calculating the standard deviation
    st.subheader("Standard Deviation")
    stdev = np.std(stock_data['% Change'])*np.sqrt(261)
    st.write('Standard Deviation is: ', stdev*100,'%')



## making detailed analysis of the given portfolio
with visualizations:
    ## Making visulaizations for the proper analysis of the given market portfolio

    ## creating the line plot for the open price of the given symbol
    fig = px.line(stock_data, x = stock_data.index , y = stock_data['Open'], title='Open price of the given stock')
    st.plotly_chart(fig)

    ## creating the line plot for the closing price of the given symbol
    fig = px.line(stock_data, x = stock_data.index , y = stock_data['Close'], title='Closing price of the given stock')
    st.plotly_chart(fig)

    ## creating the line plot for the closing price of the given symbol
    fig = px.line(stock_data, x = stock_data.index , y = stock_data['High'], title='Highest price of the given stock')
    st.plotly_chart(fig)


    ## investigating on the moving avergae of our market portfolios
    window = 50
    ts = stock_data['Close']
    
    ## making the moving average
    ts_moving_avg = ts.rolling(window = window).mean()

    ## making the plots on the moving average of our given stocks
    stock_data['Price'] = stock_data['SMA_50'] = stock_data['Close'].rolling(window=50).mean()
    fig = px.line(stock_data, x = stock_data.index, y = stock_data['Price'], title='50-day SMA', labels={"50-dat SMA"})
    fig.update_traces(line = dict(color='green'))
    st.plotly_chart(fig)

    ## calculating the 200 day moving average of the given ticker
    stock_data['Price'] = stock_data['SMA_200'] = stock_data['Close'].rolling(window=200).mean()
    fig = px.line(stock_data, x = stock_data.index, y = stock_data['Price'], title='200-day SMA', labels={"50-dat SMA"})
    st.plotly_chart(fig)

    # plotting the EXPONENTIAL MOVING AVERAGE GRAPH(EMA)

    ## the adjust is kept as 'false' in order to calculate the fixed number of periods regardless of any missing values

    stock_data['Price'] = stock_data['EMA_50'] = stock_data['Close'].ewm(span=50, adjust = False).mean()
    fig = px.line(stock_data, x = stock_data.index, y = stock_data['Price'], title='50-day EMA', labels={"50-dat EMA"})
    fig.update_traces(line = dict(color='red'))
    st.plotly_chart(fig)

    ## plotting the PCR of the opening prices of stock chart

    stock_data['Price'] = stock_data['PCR'] = stock_data['Open'].pct_change(periods=50)*100
    fig = px.line(stock_data, x = stock_data.index, y = stock_data['Price'], title='PCR of 50days', labels={"50-dat EMA"})
    fig.update_traces(line = dict(color='red'))
    st.plotly_chart(fig)

    ## creating the candle stivk plot for the given stock symbol
    st.subheader('CandleStick chart for the given equity portfolio')
    fig = go.Figure(data=[go.Candlestick(x=stock_data.index,
                open = stock_data['Open'],
                high = stock_data['High'],
                low = stock_data['Low'],
                close = stock_data['Close'])])
    st.plotly_chart(fig)



## making a tutorial for the basics of finance for the user
with tutorial:
    st.subheader("What is opening price")
    st.text("The opening price of a stock on the stock market is the price of the first trade that occurred when the market opened for trading. The opening price is determined by supply and demand, with the price being established by the first buyer and seller in the market.")

    st.subheader("What is closing price")
    st.text("The stock market opening and closing prices depend on the particular stock exchange. Generally, the opening price is the price at the beginning of the trading session, while the closing price is the price of the last transaction in the trading session")

    st.subheader("What is highest price")
    st.text("The opening and closing prices will be reported during the trading session on the day that the stock is listed. Generally, the highest price will be recorded at the end of the trading session; however, there can be fluctuations during the day.")
    
    st.subheader("How to read a Candle Stick Chart")
    st.text("A candle stick chart is a graphical representation of the open, high, low, and closing prices of a security over a given time period. To read a candle stick chart, the price movement over a given time period is indicated by the shape, color and size of the depiction. The open is indicated by the body of the candle, the high price is indicated by the high end of the wick, the low price is indicated by the low end of the wick and the close is indicated by the lower/upper part of the body of the candle.")



## making the technical analysis dashboard for the user with having more than 100 indicators features
import pandas_ta as ta
with technical_analysis:
    st.subheader("Technical Analysis Dashboard")

    stock_data = pd.DataFrame()
    stock_data = nse.get_history(Stock_symbol, start = start_date, end = end_date)
    ind_list = stock_data.ta.indicators(as_list = True)
    ##st.write(ind_list)

    technical_indicator = st.selectbox("Technical Indicator", options = ind_list)
    method = technical_indicator
    indicator=pd.DataFrame(getattr(ta, method)(low=stock_data['Low'], high=stock_data['High'], close=stock_data['Close'], open=stock_data['Open'], volume=stock_data['Volume']))
    indicator['Close'] = stock_data['Close']
    figW_ind_new = px.line(indicator)
    st.plotly_chart(figW_ind_new)
    st.write(indicator)



## making the whole economics news dashboard
with news:
    st.header(f'News of Market')
    sn = StockNews(ticker, save_news=False)
    df_news = sn.read_rss()
    for i in range(10):
        st.subheader(f'News {i+1}')
        st.write(df_news['published'][i])
        st.write(df_news['title'][i])
        st.write(df_news['summary'][i])
        title_sentiment = df_news['sentiment_title'][i]
        st.write(f'Title Sentiment {title_sentiment}')
        news_sentiment = df_news['sentiment_summary'][i]
        st.write(f'News Sentiment {news_sentiment}')


## implementing the LSTM model for the given equity
import tensorflow as tf
import math
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from sklearn.metrics import accuracy_score 

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import LSTM

with model:

    stock_data = nse.get_history(Stock_symbol, start = start_date, end = end_date)
    stock_data.reset_index(inplace = True)

    ## taking the closing price for the training of the model
    df = stock_data.reset_index()['Close']

    scaler=MinMaxScaler(feature_range=(0,1))
    df=scaler.fit_transform(np.array(df).reshape(-1,1))

    ## splitting of the dataset
    training_size=int(len(df)*0.65)
    test_size=len(df)-training_size
    train_data,test_data=df[0:training_size,:],df[training_size:len(df),:1]

def create_dataset(dataset, time_step=1):
	dataX, dataY = [], []
	for i in range(len(dataset)-time_step-1):
		a = dataset[i:(i+time_step), 0]   ###i=0, 0,1,2,3-----99   100 
		dataX.append(a)
		dataY.append(dataset[i + time_step, 0])
	return np.array(dataX), np.array(dataY)


time_step = 100
X_train, y_train = create_dataset(train_data, time_step)
X_test, ytest = create_dataset(test_data, time_step)

# reshape input to be [samples, time steps, features] which is required for LSTM
X_train =X_train.reshape(X_train.shape[0],X_train.shape[1] , 1)


model=Sequential()
model.add(LSTM(50,return_sequences=True,input_shape=(100,1)))
model.add(LSTM(50,return_sequences=True))
model.add(LSTM(50))
model.add(Dense(1))
model.compile(loss='mean_squared_error',optimizer='adam')

model.fit(X_train,y_train,validation_data=(X_test,ytest),epochs=30,batch_size=64,verbose=1)

st.title("LSTM Model in Streamlit")

st.write("This app demonstrates how to implement an LSTM model in Streamlit.")

if st.button("Predict"):
    prediction = model.predict(X_train[-1].reshape(1, X_train.shape[1], X_train.shape[2]))
    prediction = scaler.inverse_transform(prediction)
    st.write("Prediction:", prediction)



## implementing the PYCHAT GPT dashboard
from pyChatGPT import ChatGPT
session_token = 'eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..BKkL09tGyaHAPros.P4DbCROV3ruFZ2kra5dkpBN6_FI3I9GUsAgqCrL7C6lied3ekjFfJRta19s5cvqo8GPT9VOSzKTd0dbh4qroRsveOEZ-pYN0VOawT0S_2oR1ILowdKbN1a_RDLw0gd3o6TWLZVmhfeeEJgjR0GwvaczxkX7UDETvJmJxUySNlkb4InVhQjczK7Ko1zfdCxy-KfpWOYRMhZh97k-vLBNlgSnp6xdMPhMCbwAD-Ix4wFEu_NwHmu2Vkr-PhS1leqAt6ogwlrakscj0IygL7HEXTYPKhZPNzBXQ9Dog56euAi3wRLQbB6psByvsWIAcmEBQLZwIRK8npLzX7_I0-eH_IMPjvq8lT5r84MMHQufT6ZlUcNTsKVJ7thQcqrumyduXJvyWkA_HnS3BLjqSmnPMKPMquU7ta__I99NOVEpm09mBksNsuYR9nI34Bw9jAosN4BVBP2oxtZSMrg-gCedKLcAUVxgtDiJqrnkvZVwFI7bePyoxtsitTltZTMSxM_em20__338fIGGD1UawxyRKtlNOUI23ecr_MFQLXn374ElyvrJoo7JEJJjkGPFBl45OhCuQ6v5WAITuBfYNzCoX60cLjNRB0WCvykqpHUmwMxKVfFi322NvlWaX3GoY5dL6S3qfnR6k1kQtJ0IH-0-JgiQVX8iidkJ_nF4XeeqvywHMRqI9t2i53hOLZsM36nMG8imKTj_6wjqykhDE2pE0xjNaVQvNDAFd48F99qzVtfkE0vbJq0gE2E_zjeqK-vA8ZKdLfqY6N__HalXaQXNHbbJYVOV8lFqEOxrPq24MKW1gCEc5w5dos7R_MO297-NqPLIgoyPHl3wTdaik7yxtPeuiYY2DAb8KXJYu_otji0WwZdrp39pTWiGqk8rhJu975yI-WSacjaJUipuv1pa2YALedcKIOWB9f637XSnhatCt0qEO2lDu7bfyeSyM-Mj4Ru1YbgKiqbo6FlPOxVt3fGBKyaJCQ9dxsNpUzsVE-5KOuu_ofrX0Rmk7tav1qJAA_d9tWW2ZHgCpiWJTiSn2fEmvnyLkqccVa7nWavnFKlVQLlOL_OuwTAz963V_YCpMhj8UDcljBTE9Ot3GUwPkNjjvSldpTBNDBIl0DAXSeNhtHsCoDe-IWEYNjwEob8pTKD12cuTFfoguQNf3HLev6hc1HddjilU45EoFaJdvNM2HFtBTY65v5PDfCY4kOOlitKfzGuhVXgI03tHU8_L4obkbvdYWmQgheW2hXAX1cFe9KrWUm2oAM53brJui7ZqPKmlN3KH8Fak4NeIJVUAZTlnfttqS0PEprfFvEfoFogsfHWm6uoNS0HRNlmRzj5LqGxAJGx8G7edAvRxTyrzM0TdBU1qE5O_h88th75fvIufTD-_uUf5UCEsVXOmrYVB5r3ekGEcfTqs6DAXmWNHVlOe7vIbo6OBnTm5PtbXINh5cGsd8HvzJghXYbb7yKa8_EWq1pCmc0WCgyuceI4GuJ3usiGt7nbnorBjjnWyk7MIeAaWBlDu-NRgD1F6x-1Y_9Eg0Sl7BeTgFj2ZNbVWT3CgYDBzA4NLzwB7CQz-7_mjXrtGgMnUU1qOlTkOuFZuDHU8H2t0J1oUc87_ZzHp63ACgwEOM0e4tHDAHGc7QOEnPqbdTk6vy1VRKauqMUOWTve7GtJyaCPMCYBMiLZV3IVz7OeRM8NfrOcVemyyW_WtrlPEWY3S7xBMwN25dD-OW3XJZNT_0mDzxbcCeBlrUIx11iQOQgljw8IPYAF7xn3duqniBPdoYYKTg2qlnXYYHIiHfaHuC3J5wty4m5hcfDPFu8vzlX6WKtS72qymVkolSQQsEQskBv-bHqWQqSUkAo6P7M2uPwpcRvUCFYnIRjGbLIWva9Mhz16ZInt3ebf-8H7DjuKaXw83DA8CdQxyLwkXKOKQG0xpppPF73mfoECHpuPdYFTC5_PzeIyi8nDACyhrAaviWVgE8UByP6kiXxvdscDoB0QJ2oabw1qEUexfqshLEJwQyDnfg2YQfIBkMGfUMb3HtFOwCPIUsztinKRlJpGUgbnKDtx9JGoPtjmD5f_sFFYmGKX80wB9rSpcUCECUhWxAavKepWQqKyQx_f1xnEb1ciZof0B1c_OmvgLTe9k2-HaZngC5PO74GTESwU47oB12oGhqvfAVCNEo2ReqxVqwK31CjGyRU5MzAFoTYTMNFPSBdyYQei88mXgZNETOVYYIxaoZZcqRYeXL2wlB4_TmtB_eS3VIekqQSK5wi6jkreEKRzQXR9SV3rXVnrVGpZnT-q7V_Wi-KRzPnLPEGQe9qEN3Fb9nXkPSH-vUWey9wx46lj28HsJuQ2zt7GhUptMPxsSDPwYKz2grTm-4ZkZrf9dJJVhIT5DU7ZEVoIOq5WbMFZz0E60UK-F3K7fFbfunajdZ4CsZjNyY248GkcATH6JfJb6FXgtibdeJSMTwviYZH_5CYoGWiIm3jk9WzJ92yxretZDNoFIbsBSj5jZdiyd_UpT6gnF3d9-jeGf14_4Om9p50H_Cj-xiKnjmHY6oZImr2qc-KCQqMxiutxYbtgZ876ce7PjIBw0mT7LLOP3stA.HEMM2rF_8TYI69Udn1xPPQ'
api = ChatGPT(session_token)
buy = api.send_message(f'3 Reasons to buy {ticker} stock')
sell = api.send_message(f'3 Reasons to sell {ticker} stock')

with ChatGPT:
    buy_reason, sell_reason, SWOT_analysis = st.tabs(['3 Reasons to buy', '3 Reasons to sell', 'SWOT_ANALYSIS'])

    with buy_reason:
        st.subheader(f'3 Reasons to buy {ticker} Stock')
        st.write(buy['message'])
    
    with sell_reason:
        st.subheader(f'3 Reasons to buy {ticker} Stock')
        st.write(buy['message'])
    
    with SWOT_analysis:
        st.subheader(f'SWOT Analysis of {ticker}')
        st.write(SWOT_analysis['message'])
    

## *************************************************************** ##