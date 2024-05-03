{{ config(materialized='table') }}

select distinct *
,SYSDATE as tm_created
,SYSDATE as tm_last_updated
from stg_participant