import streamlit as st
import pandas as pd
import requests
import plotly.express as px 
from matplotlib import pyplot as plt
from main import *
from datetime import datetime, date, time, timedelta, timezone
from rag import *

tickers = ['SBER', 'LKOH', 'YNDX', 'GAZP', 'MGNT', 'ROSN', 'FIVE', 'FIXP', 'MTSS', 'MOEX', 'TCSG', 'OZON', 'QIWI', 'AFLT', 'POSI', 'PIKK', 'SPBE', 'MVID', 'VKCO', 'VTBR'] 

if 'step' not in st.session_state:
    st.session_state.step = 1

if st.session_state.step == 1:
    st.header('agents4predictions')
    ticker = st.selectbox("Выберите тикер", tickers, index=None)
    date_start = st.date_input('Дата начала')
    date_end  = st.date_input('Дата конца')
    
    if st.button('Получить данные'):
        j = requests.get(f'http://iss.moex.com/iss/engines/stock/markets/shares/securities/{ticker}/candles.json?from={date_start}&till={date_end}&interval=10').json()
        data = [{k : r[i] for i, k in enumerate(j['candles']['columns'])} for r in j['candles']['data']]
        frame = pd.DataFrame(data)
        
        fig = px.line(frame, y='close', labels={'index': '10-min Interval', 'close': 'Close Price'})
        fig.update_layout(title=f'Close Price for {ticker}')
        st.plotly_chart(fig)
        st.write()
        
        res = get_data_from_api(url=link, ticker=ticker, cursor_number='999999999')
        texts = list([el['text'] for el in res])
        sum = run_chain(texts, ticker)        
        
        st.write(sum)
