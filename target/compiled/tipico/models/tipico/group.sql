

select distinct *
,SYSDATE as ads_dtm_created
,SYSDATE as ads_dtm_last_updated
from "dev"."timothy_chan"."group_raw_data_test"