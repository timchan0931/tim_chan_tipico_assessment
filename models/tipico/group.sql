{{ config(
    materialized='table',
    unique_key='group_id',
    strategy='merge',
    merge_update_keys=['name','parentgroupname','parentgroupid'],
    merge_behavior={
        'when_matched': 'update',
        'when_not_matched': 'insert'
    }
) }}

select distinct *
,SYSDATE as tm_created
,SYSDATE as tm_last_updated
from {{ref("group_raw_data")}}