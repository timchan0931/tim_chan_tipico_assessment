import requests
import pandas as pd
from botocore.exceptions import ClientError
import psycopg2
import logging
from sqlalchemy import create_engine
import configparser

def create_redshift_tables(df,table_name,schema):
    # Read database crentials from config.ini
    config = configparser.ConfigParser()
    config.read('/Users/tim/tipico_git/ingestions/config.ini')

    # Read from config.ini to get database details
    dbname = config['database']['dbname']
    schema = config['database']['schema']
    host = config['database']['host']
    port = config['database']['port']
    user = config['database']['user']
    password = config['database']['password']

    # Establish a connection to Redshift using psycopg2
    conn = psycopg2.connect(
        dbname=dbname,
        host=host,
        port=port,
        user=user,
        password=password
    )

    logging.basicConfig()
    logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

    # Create a SQLAlchemy engine to be used by pandas. Use echo parameter to show SQL query
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{dbname}',echo=True)
    
    # Truncate staging table, so we don't need to drop it
    cursor = conn.cursor()
    cursor.execute(f"""TRUNCATE {schema}.{table_name}""")

    # Insert data from dataframe to table
    df.to_sql(table_name,engine,index=False,if_exists='append',schema=schema)

    conn.close()

'''
Parameters:
-response: JSON response
-region: AWS region
-filename: File to upload to S3
-bucket: S3 bucket to upload file to
-key: S3 object key
'''
def parse_json_response(response):
    #Create lists to store data for each requirement
    market_lst = list()
    outcome_lst = list()
    eventDetails_lst = list()
    group_lst = list()
    participant_lst = list()
    specifier_lst = list()
    event_lst = list()

    # Iterate through JSON response and extract fields that we need
    for item in response:
        event_lst.append({ 'root_id': item.get('id',-1),
                            'start_Time': item.get('startTime','2999-12-31 00:00:00')
                            ,'message_Time': item.get('messageTime','2999-12-31 00:00:00')
                            ,'match_State': item.get('matchState','NA')
                            ,'sport_Type': item.get('sportType','NA')
                            ,'status': item.get('status','NA')
                            ,'market_count': item.get('marketCount','NA')
                            ,'type': item.get('eventType','NA')
                            ,'name': item.get('eventName','NA')
                            ,'last_modified_time': item.get('lastModifiedTime','2999-12-31 00:00:00')})
        # Iterate through participants[] and append each JSON object to participant_lst
        for p in item.get('participants','NA'):
                    participant_lst.append({ 'root_id': item.get('id','NA')
                                            ,'participant_id': p.get('id','NA')
                                            ,'name': p.get('name','NA')
                                            ,'position': p.get('position','NA')
                                            ,'abbreviation': p.get('abbreviation','NA')})
        for m in item['markets']:
            # Iterate through markets[] and append each JSON object to market_lst
            market_id = m.get('id','NA')
            market_lst.append({'root_id': item.get('id','NA')
                            ,'market_id': m.get('id','NA')
                            ,'name': m.get('name','NA')
                            ,'type': m.get('type','NA')
                            ,'parameters': str(m.get('parameters','[]'))
                            ,'status': m.get('status','NA')
                            ,'most_Balanced_Line': m.get('mostBalancedLine',False)
                            ,'is_sgp_Eligable': m.get('sgpEligable',False)})
            # Iterate through outcomes[] and append each JSON object to outcome_lst
            for outcome in m.get('outcomes','NA'):
                outcome_lst.append({'root_id': item.get('id','NA')
                                    ,'market_id': market_id,
                                    'outcome_id': outcome.get('id','NA')
                                    ,'name': outcome.get('name','NA')
                                    ,'traded_ind': outcome.get('isTraded','NA')
                                    ,'true_Odds': outcome.get('trueOdds',0.0)
                                    ,'format_Decimal': outcome.get('formatDecimal',0.0)
                                    ,'format_American': outcome.get('formatAmerican',0.0)
                                    ,'status': outcome.get('status','NA')
                                    ,'true_Odds': outcome.get('trueOdds',0.0)})
        # Iterate through eventDetails[] and append each JSON object to eventDetails_lst
        eventDetails_lst.append({'root_id': item.get('id','NA')
                            ,'block_cashout': item.get('eventDetails','NA').get('block_cashout','NA')
                            ,'long_Term_Event_Type': item.get('eventDetails','NA').get('longTermEventType','NA')
                            ,'outright_Type': item.get('eventDetails','NA').get('outrightType','NA')
                            ,'sub_group_Name_Key': item.get('eventDetails','NA').get('subgroupNameKey','NA')
                            ,'sub_group_Id_Key': item.get('eventDetails','NA').get('subgroupIdKey',-9999)
                            ,'tie_break': item.get('eventDetails','NA').get('tiebreak','NA')
                            ,'best_of_sets': item.get('eventDetails','NA').get('best_of_sets','NA')})
        # Iterate through group[] and append each JSON object to group_lst
        group_lst.append({'root_id': item.get('id','NA')
                            ,'group_id': item.get('group','NA').get('id',-9999)
                            ,'name': item.get('group','NA').get('name','NA')
                            ,'parent_Group_Name': item.get('group','NA').get('parentGroup','NA').get('name','NA')
                            ,'parent_Group_Id': item.get('group','NA').get('parentGroup','NA').get('id','NA')})
        
    # Call create_redshift_tables() to populate stage tables
    create_redshift_tables(pd.DataFrame(event_lst),'stg_event','timothy_chan')
    create_redshift_tables(pd.DataFrame(eventDetails_lst),'stg_event_dtls','timothy_chan')
    create_redshift_tables(pd.DataFrame(participant_lst),'stg_participant','timothy_chan')
    create_redshift_tables(pd.DataFrame(outcome_lst),'stg_outcome','timothy_chan')
    create_redshift_tables(pd.DataFrame(market_lst),'stg_market','timothy_chan')
    create_redshift_tables(pd.DataFrame(group_lst),'stg_group','timothy_chan')
    

def pull_tipico_data():
    #API URL
    url = "https://trading-api.tipico.us/v1/pds/lbc/events/live?licenseId=US-NJ&lang=en&limit=50"

    payload = {}
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0'}

    #Make a GET request to API URL and store the response in response 
    response = requests.request("GET", url, headers=headers, data=payload)
    # Only parse JSON Object if status is OK
    print(response.status_code)
    if response.status_code == 200:
        content_type = response.headers['Content-Type']
        # For now, we are only expecting to get a JSON array/object from the API response
        if 'application/json' in content_type:
                #Parse json response, zip it up and upload to S3 for storing
                parse_json_response(response.json())
        else:
                print('Unsupported content type:', content_type)
    else:
        print('Request failed with status code:', response.status_code)

def main():
    pull_tipico_data()


if __name__ == "__main__":
   main()