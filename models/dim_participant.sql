{{ config(materialized='incremental',unique_key = ['root_id','participant_id'],
    merge_update_columns = ["name"
,"position"
,'abbreviation'
,'tm_last_updated']) }}

select distinct 
root_id
,participant_id
,"name"
,"position"
,abbreviation
,SYSDATE as tm_created
,SYSDATE as tm_last_updated
from stg_participant