import pandas as pd
import requests
import json

import calplot

import streamlit as st


########################################################################################################################

st.markdown("# Florian Niclause")
st.markdown("## Data Engineer")
st.markdown("""
    I am specialized in Python, data and related topics. 
    
    You can find my [GitHub](https://github.com/fniclause).
    
    You can reach me on my  [Linkedin](https://www.linkedin.com/in/florian-niclause/).
""")

st.write("My First Streamlit Web App")


########################################################################################################################

#github contribution calplot

#df=pd.read_csv('./data/git_data_contribution.csv')


url = 'https://api.github.com/graphql'
json = { 'query' : '{viewer { login contributionsCollection {contributionCalendar {weeks { contributionDays {date weekday contributionCount contributionLevel color}}}}}}' }
api_token = st.secrets.github_token
headers = {'Authorization': 'token %s' % api_token}

r = requests.post(url=url, json=json, headers=headers)

data=r.json()['data']['viewer']['contributionsCollection']['contributionCalendar']

df = pd.json_normalize(data, record_path=['weeks','contributionDays'])

df['date'] = pd.to_datetime(df.date, format='%Y-%m-%d')
df.set_index('date', inplace = True)

fig, ax = calplot.calplot(data = df['contributionCount'],how = 'sum', cmap = 'YlGn', figsize = (16, 8), suptitle = "Contributions on Github by Month and Year",colorbar=False,vmin=0,vmax=5)

st.pyplot(fig)

#########################################################################################################################

# training, routine and stretching on one heatmap
from datetime import date, datetime, time, timedelta
import seaborn as sns
import matplotlib.pyplot as plt

df2=pd.read_csv('./data/activities_d.csv')
df2=df2.replace('Ride','Training').replace('Run','Training').replace('Swim','Training').replace('Yoga','Stretching').replace('WeightTraining','Morning Routine')

df2['start_date_local_'] =pd.to_datetime(df2.start_date_local_, format='%Y-%m-%d %H:%M:%S%z', utc=True).dt.strftime('%Y-%m-%d')
df2['start_date_local_'] =pd.to_datetime(df2.start_date_local_, format='%Y-%m-%d', utc=True)

from datetime import date, datetime, time
d=datetime.today() - timedelta(days=8)
d=pd.to_datetime(d, format='%Y-%m-%d', errors='ignore',utc=True)

df2=df2.loc[df2['start_date_local_'] > d]

df2['year'] = df2.start_date_local_.dt.year
df2['month'] = df2.start_date_local_.dt.month
df2['week'] = df2.start_date_local_.dt.isocalendar().week

df2['Weekday_name'] = df2.start_date_local_.dt.day_name()

pivoted_data = pd.pivot_table(df2[['start_date_local_','Weekday_name','moving_time_sum','type_']],
                              values='moving_time_sum',index=['type_'] , columns=['start_date_local_','Weekday_name'])

pivoted_data.columns = pivoted_data.columns.droplevel()

#pivoted_data[pivoted_data>0]=1

fig2, ax = plt.subplots()
sns.heatmap(pivoted_data, linewidths=5, cmap='Greens',linecolor='white', square=True,cbar=False,vmin=0,vmax=1)
st.write(fig2)