import requests
import pandas as pd
import json
import xmltodict
import os
from dotenv import load_dotenv

load_dotenv()
SERVICEKEY = os.environ.get('SERVICEKEY')
months = []
results = []
pr = pd.period_range(start='2019-11',end='2022-08', freq='M')
for i in pr:
    months.append(str(i).replace('-',''))


results = []
pages = ['1','2']
for j in months:
    for h in pages:
        URL = os.environ.get('URL')
        params ={'serviceKey' : f'{SERVICEKEY}','pageNo' : h, 'numOfRows' : '9999', 'testYm' : j}
        response = requests.get(URL, params=params)

        result = response.text
    
        data_dict = xmltodict.parse(result)  #xml 을 dict 으로 변환.

        results.append(data_dict) #dict 를 results 에 append.


