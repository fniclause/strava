#! /usr/bin/env python3
# coding: utf-8

import requests
import pandas as pd

import time
import datetime

from dateutil import parser
import calendar

import os
import config
import glob

import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


from function import log

########################### connect to strava to get API credential ###############
log('------------------------Beginning--------------------')
log('Launching Job A')
# get email & password
email_user = config.USER_EMAIL
password = config.USER_PASS

# access strava and authentificate
s=Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=s)
driver.get("http://www.strava.com/login")


css_selector = 'button[class="btn-accept-cookie-banner"]'
driver.find_element(by=By.CSS_SELECTOR, value=css_selector).click()

search_box = driver.find_element(By.ID,'email')

search_box.send_keys(email_user)

pass_box = driver.find_element(By.ID,'password')
pass_box.send_keys(password)

css_selector_2 = 'button[class="btn btn-primary"]'
cookie_to_click = driver.find_element(by=By.CSS_SELECTOR, value=css_selector_2)
try :
    cookie_to_click.click()
except NoSuchElementException:
    pass


#aller sur la page
url_auth='https://www.strava.com/oauth/authorize?client_id=78772&response_type=code&redirect_uri=http://localhost/exchange_token&approval_prompt=force&scope=profile:read_all,activity:read_all'
driver.get(url_auth)
#cliquer sur 'Authorize'
#id_ = 'button[id="authorize"]'
driver.find_element(By.ID, "authorize").click()
#prendre l'access token dans driver.current_url à http://localhost/exchange_token?state=&code=de6eb8529ce8ee0271941f2c5d0dd872d5feb376&scope=read,activity:read_all,profile:read_all
url_code = driver.current_url
#le mettre dans code
code = url_code.split("&")[1].replace("code=","")
driver.quit()

########################### API call to get strava_tokens ###############

import requests
import json
import config
# Make Strava auth API call with your
# client_code, client_secret and code
response = requests.post(url='https://www.strava.com/oauth/token',
                         data={
                             'client_id': config.client_ID,
                             'client_secret': config.client_secret,
                             'code': code,
                             'grant_type': 'authorization_code'
                         })
#Save json response as a variable
strava_tokens = response.json()
# Save tokens to file
with open('strava_tokens.json', 'w') as outfile:
    json.dump(strava_tokens, outfile)
# Open JSON file and print the file contents
# to check it's worked properly
with open('strava_tokens.json') as check:
    data = json.load(check)

#get access token
access_token = data['access_token']

########################### initialization of activities table #######################

url_init = f"https://www.strava.com/api/v3/athlete/activities?access_token={access_token}&per_page=200"
payload = {}
headers = {'Cookie': '_strava4_session=633nr333v5vqncotecis88kabfigqpff'}

response = requests.request("GET", url_init, headers=headers, data=payload)
activities_df = pd.json_normalize(response.json())

########### Initiate the timestamp
s = activities_df.iloc[-1]['start_date']
parsed_date = parser.parse(s)
timestamp = []
timestamp.append(calendar.timegm(parser.parse(s).timetuple()))

#### loop to get all activities
while True:
    url = f"https://www.strava.com/api/v3/athlete/activities?access_token={access_token}&before=" + str(
        timestamp[-1]) + "&per_page=200"
    response = requests.request("GET", url, headers=headers, data=payload)
    activities = pd.json_normalize(response.json())
    activities_df = pd.concat([activities_df, activities], ignore_index=True)

    s = activities_df.iloc[-1]['start_date']
    parsed_date = parser.parse(s)
    timestamp.append(calendar.timegm(parser.parse(s).timetuple()))

    if timestamp[-1] == timestamp[-2]:
        break



activities_df['type_bis']=activities_df['type']
activities_df['type']=activities_df['type'].replace('VirtualRide','Ride').replace('VirtualRun','Run')

from datetime import datetime, timezone
import calendar

from function import start_date, get_weekday, get_day, get_week, get_month, get_year, localize_time

#get local time
activities_df['start_date_local']=activities_df['start_date_local'].apply(start_date).apply(localize_time)

#get weekday, day, week, month and year
activities_df['weekday']=activities_df['start_date_local'].apply(get_weekday)
activities_df['day']=activities_df['start_date_local'].apply(get_day)
activities_df['week']=activities_df['start_date_local'].apply(get_week)
activities_df['month']=activities_df['start_date_local'].apply(get_month)
activities_df['year']=activities_df['start_date_local'].apply(get_year)

activities_df.to_csv(
    '/Users/florianniclause/code/fniclause/strava/data/activities.csv',
    index=False)
