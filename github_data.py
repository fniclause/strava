import requests
import json
import pandas as pd
import keys

import requests

url = 'https://api.github.com/graphql'
json = { 'query' : '{viewer { login contributionsCollection {contributionCalendar {weeks { contributionDays {date weekday contributionCount contributionLevel color}}}}}}' }
api_token = keys.github_token
headers = {'Authorization': 'token %s' % api_token}

r = requests.post(url=url, json=json, headers=headers)

data=r.json()['data']['viewer']['contributionsCollection']['contributionCalendar']

df = pd.json_normalize(data, record_path=['weeks','contributionDays'])

df.to_csv('./data/git_data_contribution.csv', index=False)