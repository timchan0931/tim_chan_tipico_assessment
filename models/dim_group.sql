-- Create dim_group model, insert/update data incrementally
{{ config(materialized='incremental',unique_key = ['root_id','group_id'],
    merge_update_columns = ['start_time',
'"name"'
,'parent_group_name'
,'parent_group_id'
'last_modified_time']) }}

SELECT 
root_id
,group_id
,"name"
,parent_group_name
,parent_group_id
,SYSDATE as tm_created
,SYSDATE as tm_updated
from {{source('tipico_data','stg_group')}}