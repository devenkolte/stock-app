import streamlit as st
import stock_app as sa
import pandas as pd

name = st.sidebar.text_input('Enter Name')
button = st.sidebar.button('Click to Add')
df = pd.DataFrame(columns = ['Closing Value', 'Cal1', 'Cal2', 'Trend 1', 'Trend 2', 'Trend 3', 'Date'])
if button:
    sa.conn.create(worksheet = name, data = df)
    st.success('Worksheet Created')
#st.write(sa.worksheet_names)

