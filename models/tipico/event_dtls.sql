{{ config(materialized='table') }}

select distinct 
case when block_cashout = true then 1 else 0 end as block_cashout
,long_term_event_type
,outright_type
,cast(sub_group_name_key as varchar(255)) as sub_group_name_key
,sub_group_id_key
,tie_break
,best_of_sets
,SYSDATE as tm_created
,SYSDATE as tm_last_updated
from {{ref("event_dtls_raw_data")}}