-- Create dim_event model, insert/update data incrementally
{{ config(materialized='incremental',unique_key = ['root_id'],
    merge_update_columns = ['start_time',
'message_time',
'match_state',
'sport_type',
'status',
'market_count',
'"name"',
'"type"',
'last_modified_time']) }}

SELECT distinct 
root_id,
start_time,
message_time,
match_state,
sport_type,
status,
market_count,
"name",
"type",
last_modified_time,
SYSDATE as tm_created,
SYSDATE as tm_updated
from {{source('tipico_data','stg_event')}}