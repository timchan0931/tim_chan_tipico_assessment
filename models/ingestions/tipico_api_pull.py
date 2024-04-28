import requests
import json
import csv
import pandas as pd

url = "https://sportsbook-nj.tipico.us/v1/pds/lbc/events/live?lang=en&licenseId=US-NJ&limit=5"

payload = {}
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0'}

response = requests.request("GET", url, headers=headers, data=payload)

data = response.json()

market_lst = list()
outcome_lst = list()
for item in data:
    for m in item['markets']:
        market_lst.append((m.get('id','NA')
                           ,m.get('name','NA')
                           ,m.get('type','NA')
                           ,m.get('parameters',[])
                           ,m.get('status','NA')
                           ,m.get('mostBalancedLine',False)
                           ,m.get('sgpEligable',False)))
        outcome_lst.append((m.get('id','NA'),m.get('name','NA')
                            ,m.get('isTraded','NA')
                            ,m.get('trueOdds',0.0)
                            ,m.get('formatDecimal',0.0)
                            ,m.get('formatAmerican',0.0)
                            ,m.get('status','NA')
                            ,m.get('trueOdds',0.0)))

market_headers= ['market_id','name','type','parameters','status','mostBalancedLine','spgEligable']
outcome_headers= ['outcome_id','name','isTraded','trueOdds','foramtDecimal','formatAmerican','status','trueOdds']
pd.DataFrame(market_lst).to_csv('markets.csv',index=False,quoting=csv.QUOTE_ALL,header=market_headers)
pd.DataFrame(outcome_lst).to_csv('outcomes.csv',index=False,quoting=csv.QUOTE_ALL,header=outcome_headers)