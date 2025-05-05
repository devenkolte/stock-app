import streamlit as st
import pandas as pd
#from streamlit_gsheets import GSheetsConnection
from st_gsheets_connection import GSheetsConnection
#from zmq.backend.cffi.socket import new_binary_data
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
  page_title="Home",
  layout='wide'  
)


def generate_list(cp, input_date, v, w, y):
  new_list = []
  cal1 = ((cp*0.1538461538) + (v*0.8461538462))
  cal2 = ((cp*0.07407407407) + (w*0.9259259259))
  t1 = cal1 - cal2
  t2 = ((t1*0.2) + (y*0.8))
  t3 = t1 - t2
  new_list.extend([cp,cal1,cal2,t1,t2,t3,input_date])
  return new_list

st.title("Welcome to Stock Analysis App")

#establishing a connection \
conn = st.connection("gsheets", type = GSheetsConnection)

#fetching the data

#fetching the list name
names = ['Test','Sheet1', 'GAEL', 'GICRE', 'GLEN', 'GNFC', 'GODAG', 'GODIND', 'GRANULE',
        'GRAPHITE', 'GPANEL', 'GSFC', 'GSPL', 'GUSGAS', 'HIKAL', 'HINDALCO', 'HINDCOPP',
        'HINDPETRO', 'HINDZINC', 'IBULHSG', 'ICICIPRU', 'IEX', 'IIFL', 'INDHOTEL', 'INDCEM',
        'INDIANB', 'INDOCO', 'INDUSTOW', 'INTELLECT', 'IRB', 'ISEC', 'ITC', 'ITI', 'JAMNAUTO',
        'JBMA', 'JKPAPER', 'JSL', 'JSWENERGY', 'JUBLFOOD', 'JUBLINGRE', 'JUBLPHARMA', 'JYOTHYLAB',
        'KALYANKJI', 'KANSAINE', 'KARIRVUSA', 'KEC', 'KNRCON', 'KPRMILL', 'KRBL', 'LATENTVIEW', 
        'LAURUSL', 'LXCHEM', 'M&MFIN', 'MAHLIFE', 'MMAHLOG', 'MANAPPURAM', 'MARICO', 'MAXHEALTH',
        'MHRIL', 'MOIL', 'NAM-INDIA', 'NATCOPHARMA', 'NAZARA', 'NIACL', 'NOCIL', 'NTPC', 'NYKAA',
        'Sheet4', 'NUVOCO', 'Sheet5', 'Sheet2', 'Sheet3', 'Aarti', 'Abcapital', 'ABFRL', 'ABSL',
        'Aegis', 'Amaraja', 'Ambuja', 'APLLTD', 'Apollo', 'Aptus', 'Asahiindia', 'Ashokley',
        'Asterdm', 'AUROP', 'Avantifeed', 'AWL', 'Balramchin', 'Bandhan', 'BOB', 'BEL', 'Berger',
        'Biocon', 'Boro', 'Boronew', 'BPCL', 'Brigade', 'BSE', 'BSOft', 'Campus', 'CANBK',
        'Canfin', 'Castrolind', 'CCL', 'Centuryply', 'CGPOWER', 'Chalet', 'Chmblefert',
        'Chemplast', 'Coal', 'Cochinshi', 'Crompton', 'Csbbank', 'CUB', 'DABUR', 'DBL',
        'Delhivery', 'Delta', 'Divyani', 'DLF', 'EIDPARRY', 'EIHOTEL', 'ELGI', 'EMAMI',
         'EPL', 'EXIDE', 'FACT', 'FDC', 'FEDERAL', 'FINCABLE', 'FINPIPE', 'FORTIS', 'FSL']


work_btn = st.selectbox('Select the stock',options=names)
if work_btn:
  data = conn.read(worksheet = work_btn, usecols = list(range(1,8)), ttl = 5)
  data = data.dropna(how = 'all')

  #Representing the data
  st.dataframe(data.tail(10))

  #data for calculation
  cal_d = data.iloc[-1]
  v = cal_d['Cal1']
  y = cal_d['Trend 2']
  w = cal_d['Cal2']

  #functions for sidebar
  st.sidebar.subheader('Enter the values')
  from datetime import date
  closing_price = st.sidebar.number_input('Enter the closing price')
  input_date = st.sidebar.date_input('Enter the Date')
  cd_btn = st.sidebar.button('Add the values')
  if cd_btn:
    if input_date > date.today() or closing_price < 0.0:
      st.sidebar.error("Enter correct values")
    else:
      df = pd.DataFrame(columns=["Closing Value", "Cal1", "Cal2", "Trend 1", "Trend 2", "Trend 3", "Date"])

      # Your new entry as a list
      new_entry = generate_list(closing_price, input_date, v, w, y)

      new_row_df = pd.DataFrame([new_entry], columns=df.columns)
      u_data = pd.concat([data, new_row_df], ignore_index=True)
      d = input_date
      st.sidebar.success('Added successfully')
      conn.update(worksheet='Test', data=u_data)


  

  #Visualization Starts
      
  col1, col2 = st.columns(2)
  with col1:
    plt.plot( data['Trend 1'], label='Trend 1')
    plt.plot( data['Trend 2'], label='Trend 2')
    plt.plot( data['Trend 3'], label='Trend 3')
    plt.legend()

    st.pyplot(plt)

  with col2:
    fig = px.line(data, y=['Trend 1', 'Trend 2', 'Trend 3'], markers=False, hover_data={'Date' : True})
    fig.print_grid()

    st.plotly_chart(fig)

  import plotly.graph_objects as go
  data_tail = data.tail(50)

  fig2 = go.Figure()

  fig2.add_trace(go.Bar(y=data_tail['Trend 1'], name='Trend 1'))
  fig2.add_trace(go.Bar(y=data_tail['Trend 2'], name='Trend 2'))
  fig2.add_trace(go.Bar(y=data_tail['Trend 3'], name='Trend 3'))

  fig2.add_trace(go.Scatter(
      y=data_tail['Trend 1'],
      mode='lines',
      line=dict(color='white', width=3, dash='dot'),
      yaxis='y',  # attaches to same y-axis
  ))
  fig2.add_trace(go.Scatter(
      y=data_tail['Trend 2'],
      mode='lines',
      line=dict(color='white', width=3, dash='dot'),
      yaxis='y',  # attaches to same y-axis
  ))
  fig2.add_trace(go.Scatter(
      y=data_tail['Trend 3'],
      mode='lines',
      line=dict(color='white', width=3, dash='dot'),
      yaxis='y',  # attaches to same y-axis
  ))


  fig2.update_layout(barmode='group',
                    height = 800,
                    width = 1000)
  #fig2 = px.bar(df.tail(50), y=['Trend 1', 'Trend 2', 'Trend 3'], barmode='group')
  st.plotly_chart(fig2,use_container_width=True)










  # Input from user
  #sr_no = st.sidebar.number_input("Enter Sr No to delete", min_value=1, max_value=len(data), step=1)
  # Delete button
  #d_btn = st.sidebar.button("Delete Selected Row")
  #if d_btn:
  #  updated_data = data.drop(data.index[sr_no]).reset_index(drop=True)

    # Update Google Sheet
  #  conn.update(worksheet='Test', data=updated_data)

   # st.success(f"Row {sr_no} deleted successfully!")

























#updated_data = data
# Convert the list into a one-row DataFrame and append
#new_entry_df = pd.DataFrame([new_entry])
#data = pd.concat([data,new_entry_df], ignore_index= True)
#st.dataframe(data)
#new_row = pd.DataFrame([new_entry], columns=df.columns)
#conn.update(worksheet = 'Test', data = data)


# Input form
#new data entries

#add new data to previous data
#updated_df = pd.concat([data, new_data], ignore_index= True)

#conn.update(worksheet = 'Test', data = updated_df)

#st.success('data added successfully')