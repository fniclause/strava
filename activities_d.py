#! /usr/bin/env python3
# coding: utf-8

import pandas as pd
import numpy as np

import warnings

warnings.filterwarnings("ignore")
# For connect to google sheet
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from df2gspread import df2gspread as d2g


activities_df = pd.read_csv(
    '/Users/florianniclause/code/fniclause/strava/data/activities.csv')

df_daily = activities_df.groupby(['type', 'start_date_local'],
                                 as_index=False).agg({
                                     'distance': ['sum', 'mean', 'min', 'max'],
                                     'moving_time':
                                     ['sum', 'mean', 'min', 'max'],
                                     'total_elevation_gain':
                                     ['sum', 'mean', 'min', 'max']
                                 }).sort_values(by='start_date_local',
                                                ascending=False)

df_daily.columns = ['_'.join(col) for col in df_daily.columns]

df_daily.to_csv(
    '/Users/florianniclause/code/fniclause/strava/data/activities_d.csv',
    index=False)

# Configure the connection
scope = ['https://spreadsheets.google.com/feeds']

# Give the path to the Service Account Credential json file
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    'service_account_GS.json', scope)
# Authorise your Notebook
gc = gspread.authorize(credentials)

# The sprad sheet ID, which can be taken from the link to the sheet
spreadsheet_key = '1vNnbAl7kMQHeL-UbkL8hTY93Z_3areu195dUuV7ooMA'
#

# Set the sheet name you want to upload data to and the start cell where the upload data begins
wks_name = 'day'
cell_of_start_df = 'A1'
# upload the dataframe of the clients we want to delete
d2g.upload(df_daily,
           spreadsheet_key,
           wks_name,
           credentials=credentials,
           col_names=True,
           row_names=False,
           start_cell=cell_of_start_df,
           clean=True)
