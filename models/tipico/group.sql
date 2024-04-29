{{ config(materialized='table') }}

select distinct *
,SYSDATE as ads_dtm_created
,SYSDATE as ads_dtm_last_updated
from {{ref("group_raw_data_test")}}