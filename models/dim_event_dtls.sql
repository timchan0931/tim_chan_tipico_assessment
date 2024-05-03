{{ config(materialized='incremental',unique_key = ['root_id'],
    merge_update_columns = ['start_time'
,'block_cashout'
,'long_term_event_type'
,'outright_type'
,'sub_group_name_key'
,'sub_group_id_key'
,'tie_break'
,'best_of_sets'
,'tm_last_updated']) }}

select distinct 
root_id
,block_cashout::INTEGER
,long_term_event_type
,UPPER(outright_type) as outright_type
,cast(sub_group_name_key as varchar(255)) as sub_group_name_key
,sub_group_id_key
,tie_break
,best_of_sets
,SYSDATE as tm_created
,SYSDATE as tm_last_updated
from {{source('tipico_data','stg_event_dtls')}}