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
,case when traded_ind = true then 1 else 0 end as traded_ind
,true_odds
,format_decimal
,format_american
,status
,SYSDATE as tm_created
,SYSDATE as tm_last_updated
from stg_outcome