{{ config(materialized='table') }}

select distinct 
block_cashout
,longtermeventtype
,outrighttype
,cast(subgroupnamekey as varchar(255)) as subgroupnamekey
,subgroupidkey
,tiebreak
,best_of_sets
,SYSDATE as ads_dtm_created
,SYSDATE as ads_dtm_last_updated
from {{ref("event_dtls_raw_data")}}