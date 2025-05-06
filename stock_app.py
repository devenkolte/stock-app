import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from datetime import date
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Streamlit page config
st.set_page_config(page_title="Home", layout='wide')

# Google Sheets authentication function
def authenticate_google_sheets():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name('path_to_your_credentials.json', scope)
    client = gspread.authorize(creds)
    return client

# Fetch data from Google Sheets
def get_sheet_data(spreadsheet_name, sheet_name):
    client = authenticate_google_sheets()
    spreadsheet = client.open(spreadsheet_name)
    sheet = spreadsheet.worksheet(sheet_name)
    data = sheet.get_all_records()
    return pd.DataFrame(data)

# Function to generate the calculation list
def generate_list(cp, input_date, v, w, y):
    new_list = []
    cal1 = ((cp * 0.1538461538) + (v * 0.8461538462))
    cal2 = ((cp * 0.07407407407) + (w * 0.9259259259))
    t1 = cal1 - cal2
    t2 = ((t1 * 0.2) + (y * 0.8))
    t3 = t1 - t2
    new_list.extend([cp, cal1, cal2, t1, t2, t3, input_date])
    return new_list

# Display Title
st.title("Welcome to Stock Analysis App")

# Stock names for selection
names = ['Test', 'Sheet1', 'GAEL', 'GICRE', 'GLEN', 'GNFC', 'GODAG', 'GODIND', 'GRANULE', 'GRAPHITE', 
         'GPANEL', 'GSFC', 'GSPL', 'GUSGAS', 'HIKAL', 'HINDALCO', 'HINDCOPP', 'HINDPETRO', 'HINDZINC', 
         'IBULHSG', 'ICICIPRU', 'IEX', 'IIFL', 'INDHOTEL', 'INDCEM', 'INDIANB', 'INDOCO', 'INDUSTOW', 
         'INTELLECT', 'IRB', 'ISEC', 'ITC', 'ITI', 'JAMNAUTO', 'JBMA', 'JKPAPER', 'JSL', 'JSWENERGY', 
         'JUBLFOOD', 'JUBLINGRE', 'JUBLPHARMA', 'JYOTHYLAB', 'KALYANKJI', 'KANSAINE', 'KARIRVUSA', 'KEC']

work_btn = st.selectbox('Select the stock', options=names)

if work_btn:
    # Fetching data from Google Sheets
    sheet_data = get_sheet_data('Your_Spreadsheet_Name', work_btn)
    sheet_data = sheet_data.dropna(how='all')

    # Display the last 10 rows
    st.dataframe(sheet_data.tail(10))

    # Get the last row's values for calculation
    cal_d = sheet_data.iloc[-1]
    v = cal_d['Cal1']
    y = cal_d['Trend 2']
    w = cal_d['Cal2']

    # Sidebar inputs
    st.sidebar.subheader('Enter the values')
    closing_price = st.sidebar.number_input('Enter the closing price')
    input_date = st.sidebar.date_input('Enter the Date')

    cd_btn = st.sidebar.button('Add the values')
    if cd_btn:
        if input_date > date.today() or closing_price < 0.0:
            st.sidebar.error("Enter correct values")
        else:
            # Add new entry to the data
            new_entry = generate_list(closing_price, input_date, v, w, y)
            new_row_df = pd.DataFrame([new_entry], columns=["Closing Value", "Cal1", "Cal2", "Trend 1", "Trend 2", "Trend 3", "Date"])

            # Update the data (add new entry)
            updated_data = pd.concat([sheet_data, new_row_df], ignore_index=True)

            # Update the Google Sheet (you might need to modify the `sheet_name` and range accordingly)
            client = authenticate_google_sheets()
            spreadsheet = client.open('Your_Spreadsheet_Name')
            sheet = spreadsheet.worksheet(work_btn)
            sheet.update([updated_data.columns.values.tolist()] + updated_data.values.tolist())

            st.sidebar.success('Added successfully')

    # Visualization
    col1, col2 = st.columns(2)

    with col1:
        plt.plot(sheet_data['Trend 1'], label='Trend 1')
        plt.plot(sheet_data['Trend 2'], label='Trend 2')
        plt.plot(sheet_data['Trend 3'], label='Trend 3')
        plt.legend()
        st.pyplot(plt)

    with col2:
        fig = px.line(sheet_data, y=['Trend 1', 'Trend 2', 'Trend 3'], markers=False, hover_data={'Date': True})
        st.plotly_chart(fig)

    # Bar chart for the last 50 rows
    data_tail = sheet_data.tail(50)
    fig2 = go.Figure()

    fig2.add_trace(go.Bar(y=data_tail['Trend 1'], name='Trend 1'))
    fig2.add_trace(go.Bar(y=data_tail['Trend 2'], name='Trend 2'))
    fig2.add_trace(go.Bar(y=data_tail['Trend 3'], name='Trend 3'))

    fig2.add_trace(go.Scatter(
        y=data_tail['Trend 1'],
        mode='lines',
        line=dict(color='white', width=3, dash='dot'),
        yaxis='y',
    ))
    fig2.add_trace(go.Scatter(
        y=data_tail['Trend 2'],
        mode='lines',
        line=dict(color='white', width=3, dash='dot'),
        yaxis='y',
    ))
    fig2.add_trace(go.Scatter(
        y=data_tail['Trend 3'],
        mode='lines',
        line=dict(color='white', width=3, dash='dot'),
        yaxis='y',
    ))

    fig2.update_layout(barmode='group', height=800, width=1000)
    st.plotly_chart(fig2, use_container_width=True)
