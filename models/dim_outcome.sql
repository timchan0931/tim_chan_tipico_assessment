-- Create dim_market model, insert/update data incrementally
{{ config(materialized='incremental',unique_key = ['root_id','market_id','outcome_id'],
    merge_update_columns = ['start_time'
,'message_time'
,'match_state'
,'sport_type'
,'"name"'
,'traded_ind'
,'true_odds'
,'format_decimal'
,'format_american'
,'status'
,'tm_last_updated']) }}


select distinct 
root_id
,market_id
,outcome_id
,"name"
,traded_ind
,true_odds
,format_decimal
,format_american
,status
,SYSDATE as tm_created
,SYSDATE as tm_updated
from {{source('tipico_data','stg_outcome')}}