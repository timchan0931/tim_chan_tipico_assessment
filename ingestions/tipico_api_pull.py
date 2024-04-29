import requests
import json
import csv
import pandas as pd

'''
The purpose of this script is to make an API call, save the response and store it in a Pandas Data Frame. 
This will
'''

url = "https://sportsbook-nj.tipico.us/v1/pds/lbc/events/live?lang=en&licenseId=US-NJ&limit=5"

payload = {}
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0'}

#Make a GET request to API URL and store the response in response 
response = requests.request("GET", url, headers=headers, data=payload)

#convert the response to JSON
data = response.json()

#Create lists to store data for each requirement
market_lst = list()
outcome_lst = list()
eventDetails_lst = list()
group_lst = list()
participant_lst = list()
specifier_lst = list()

for item in data:
    for p in item.get('participants','NA'):
                participant_lst.append({'id': p.get('id','NA')
                                        ,'name': p.get('name','NA')
                                        ,'position': p.get('position','NA')
                                        ,'abbreviation': p.get('abbreviation','NA')})
    for m in item['markets']:
        
        #Append each JSON object
        market_lst.append({ 'id': m.get('id','NA')
                           ,'startTime': item.get('startTime','2999-12-31 00:00:00')
                           ,'messageTime': item.get('messageTime','2999-12-31 00:00:00')
                           ,'matchState': item.get('matchState','NA')
                           ,'sportType': item.get('sportType','NA')
                           ,'name': m.get('name','NA')
                           ,'type': m.get('type','NA')
                           ,'parameters': m.get('parameters',[])
                           ,'status': m.get('status','NA')
                           ,'mostBalancedLine': m.get('mostBalancedLine',False)
                           ,'sgpEligable': m.get('sgpEligable',False)})
        for outcome in m.get('outcomes','NA'):
            outcome_lst.append({'id': outcome.get('id','NA')
                                ,'name': outcome.get('name','NA')
                                ,'isTraded': outcome.get('isTraded','NA')
                                ,'trueOdds': outcome.get('trueOdds',0.0)
                                ,'formatDecimal': outcome.get('formatDecimal',0.0)
                                ,'formatAmerican': outcome.get('formatAmerican',0.0)
                                ,'status': outcome.get('status','NA')
                                ,'trueOdds': outcome.get('trueOdds',0.0)})
    eventDetails_lst.append({'block_cashout': item.get('eventDetails','NA').get('block_cashout','NA')
                        ,'longTermEventType': item.get('eventDetails','NA').get('longTermEventType','NA')
                        ,'outrightType': item.get('eventDetails','NA').get('outrightType','NA')
                        ,'subgroupNameKey': item.get('eventDetails','NA').get('subgroupNameKey','NA')
                        ,'subgroupIdKey': item.get('eventDetails','NA').get('subgroupIdKey',-9999)
                        ,'tiebreak': item.get('eventDetails','NA').get('tiebreak','NA')
                        ,'best_of_sets': item.get('eventDetails','NA').get('best_of_sets','NA')})
    group_lst.append({'id': item.get('group','NA').get('id',-9999)
                        ,'name': item.get('group','NA').get('name','NA')
                        ,'parentGroupName': item.get('group','NA').get('parentGroup','NA').get('name','NA')
                        ,'parentGroupId': item.get('group','NA').get('parentGroup','NA').get('id','NA')})

            
market_headers= ['market_id','name','type','parameters','status','mostBalancedLine','spgEligable']
outcome_headers= ['outcome_id','name','isTraded','trueOdds','foramtDecimal','formatAmerican','status','trueOdds']
group_headers= ['group_id','name','parentGroupName','parentGroupId']

# pd.DataFrame(market_lst).to_csv('./seeds/markets.csv',index=False,quoting=csv.QUOTE_ALL,header=market_headers)
pd.DataFrame(outcome_lst).to_csv('./seeds/outcome_raw_data.csv',index=False,quoting=csv.QUOTE_ALL)


# pd.DataFrame(market_lst).to_json('./seeds/markets.json',index=False,orient='records',lines=False)
# pd.DataFrame(outcome_lst).to_json('./seeds/outcomes.json',index=False,orient='records',lines=False)
# pd.DataFrame(eventDetails_lst).to_json('./seeds/eventDetails.json',index=False,orient='records',lines=False)
# pd.DataFrame(group_lst).to_json('./seeds/group_raw_data.json',index=False,orient='records',lines=False)

pd.DataFrame(group_lst).to_csv('./seeds/group_raw_data_test.csv',header=group_headers,quoting=csv.QUOTE_ALL,index=False)
pd.DataFrame(eventDetails_lst).to_csv('./seeds/event_dtls_raw_data.csv',quoting=csv.QUOTE_ALL,index=False)
pd.DataFrame(participant_lst).to_csv('./seeds/participants_raw_data.csv',quoting=csv.QUOTE_ALL,index=False)
pd.DataFrame(specifier_lst).to_csv('./seeds/specifier_raw_data.csv',quoting=csv.QUOTE_ALL,index=False)
pd.DataFrame(market_lst).to_csv('./seeds/market_raw_data.csv',quoting=csv.QUOTE_ALL,index=False)    


# pd.DateOffset(outcome_lst).to_csv('./seeds/outcomes_raw_data_test.csv',index=False)
# pd.DataFrame(outcome_lst).to_csv('./seeds/outcomes_raw_data.csv',header=outcome_headers,index=False)