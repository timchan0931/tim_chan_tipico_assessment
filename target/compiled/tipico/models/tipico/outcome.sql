

select distinct *
,SYSDATE as ads_dtm_created
,SYSDATE as ads_dtm_last_updated
from "dev"."timothy_chan"."outcome_raw_data"