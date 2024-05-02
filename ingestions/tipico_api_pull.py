import boto3.s3
import requests
import csv
import pandas as pd
import boto3
from botocore.exceptions import ClientError
import zipfile
import psycopg2
import logging
from sqlalchemy import create_engine

def create_redshift_tables(df,table_name,schema):
     # Define the Redshift connection parameters
    dbname = 'dev'
    schema = 'timothy_chan'
    host = 'manual-dwh-candidatetests.258845600139.us-east-1.redshift-serverless.amazonaws.com'
    port = '5439'
    user = 'timothy_chan'
    password = 'POr0410!!__djif24r2fdsmbj'

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
def parse_json_response(response,region,filename,bucket,key):
    #Create lists to store data for each requirement
    market_lst = list()
    outcome_lst = list()
    eventDetails_lst = list()
    group_lst = list()
    participant_lst = list()
    specifier_lst = list()

    for item in response:
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
            print(market_id)
            market_lst.append({'root_id': item.get('id','NA')
                            ,'market_id': m.get('id','NA')
                            ,'start_Time': item.get('startTime','2999-12-31 00:00:00')
                            ,'message_Time': item.get('messageTime','2999-12-31 00:00:00')
                            ,'match_State': item.get('matchState','NA')
                            ,'sport_Type': item.get('sportType','NA')
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
                            ,'event_name': item.get('eventName','NA')
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

    # Create a Pandas DataFrame from all the lists and convert them to a CSV file. Don't include the index and quote all columns
    # pd.DataFrame(outcome_lst).to_csv('./seeds/outcome_raw_data.csv',index=False,quoting=csv.QUOTE_ALL)
    create_redshift_tables(pd.DataFrame(market_lst),'market_raw_data','timothy_chan')
    create_redshift_tables(pd.DataFrame(outcome_lst),'outcome_raw_data','timothy_chan')
    # pd.DataFrame(group_lst).to_csv('./seeds/group_raw_data.csv',quoting=csv.QUOTE_ALL,index=False)
    # pd.DataFrame(eventDetails_lst).to_csv('./seeds/event_dtls_raw_data.csv',quoting=csv.QUOTE_ALL,index=False)
    create_redshift_tables(pd.DataFrame(eventDetails_lst),'event_dtls_raw_data','timothy_chan')
    # pd.DataFrame(participant_lst).to_csv('./seeds/participants_raw_data.csv',quoting=csv.QUOTE_ALL,index=False)
    create_redshift_tables(pd.DataFrame(participant_lst),'participants_raw_data','timothy_chan')
    # pd.DataFrame(specifier_lst).to_csv('./seeds/specifier_raw_data.csv',quoting=csv.QUOTE_ALL,index=False)
    # create_redshift_tables(pd.DataFrame(specifier_lst),'specifier','timothy_chan') 
    # pd.DataFrame(market_lst).to_csv('./seeds/market_raw_data.csv',quoting=csv.QUOTE_ALL,index=False)
  

    # Zip up all the CSVs
    with zipfile.ZipFile('tipico_data_pull.zip',mode='w') as tipico_data_pull:
         tipico_data_pull.write('./seeds/market_raw_data.csv')
         tipico_data_pull.write('./seeds/group_raw_data.csv')
         tipico_data_pull.write('./seeds/event_dtls_raw_data.csv')
         tipico_data_pull.write('./seeds/participants_raw_data.csv')
         tipico_data_pull.write('./seeds/specifier_raw_data.csv')
         tipico_data_pull.write('./seeds/outcome_raw_data.csv')

    # Upload zip to S3 bucket
    s3_client = boto3.client(service_name='s3',region_name=region)
    s3_client.upload_file(Filename=filename,Bucket=bucket,Key=key)

def main():
    #API URL
    url = "https://trading-api.tipico.us/v1/pds/lbc/events/live?licenseId=US-NJ&lang=en&limit=25"

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
                parse_json_response(response.json(),region='us-east-2',filename='tipico_data_pull.zip',bucket='tims-dwh-2',key='tipico/tipico_data_pull.zip')
        else:
                print('Unsupported content type:', content_type)
    else:
        print('Request failed with status code:', response.status_code)

if __name__ == "__main__":
    main()