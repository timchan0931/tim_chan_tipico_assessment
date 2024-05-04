-- Create dim_market model, insert/update data incrementally
{{ config(materialized='incremental',unique_key = ['root_id','market_id'],
    merge_update_columns = ['start_time'
,'message_time'
,'match_state'
,'sport_type'
,'"name"'
,'"type"'
,'parameters'
,'status'
,'most_balanced_line'
,'is_sgp_eligable'
,'tm_last_updated']) }}

select distinct 
root_id
,market_id
,"name"
,"type"
,parameters
,status
,case when most_balanced_line = true then 1 else 0 end as  most_balanced_line
,case when is_sgp_eligable = true then 1 else 0 end as is_sgp_eligable
,SYSDATE tm_created
,SYSDATE tm_updated
from {{source('tipico_data','stg_market')}}