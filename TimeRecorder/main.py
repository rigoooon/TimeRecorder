import streamlit as st
import time
from pys import time_recorder
import pandas as pd

st.set_page_config(
     page_title='StudyTime',
     layout="wide",
)

st.title('StudyTime')

latest_iteration = st.empty()
bar = st.progress(0)
for i in range(100):
    latest_iteration.text(f'Iteration {i+1}')
    bar.progress(i + 1)
    time.sleep(0.01) #0.1秒ごとにfor文が実行される

col1, col2, col3 = st.columns(3)
with col1:
    st.title('Today')
    result = time_recorder.get_today_record()
    st.title(time_recorder.dmod(result))

with col2:
    st.title('Week')
    result = time_recorder.get_this_week_record()
    st.title(time_recorder.dmod(result))

with col3:
    st.title('Month')
    result = time_recorder.get_this_month_record()
    st.title(time_recorder.dmod(result))

col4, col5, col6 = st.columns(3)
with col4:
    st.title('Difference from yesterday')
    st.title(time_recorder.get_difference())

with col5:
    st.title('Year')
    result = time_recorder.get_this_year_record()
    st.title(time_recorder.dmod(result))

with col6:
    st.title('All Records')
    result = time_recorder.get_all_records()
    st.title(time_recorder.dmod(result))

with st.expander("See week records"):
    df = pd.DataFrame.from_dict(time_recorder.get_weekly_record(), orient='index').rename(columns={0:'Total'})
    st.dataframe(df)