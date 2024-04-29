
  
    

  create  table
    "dev"."timothy_chan"."outcome__dbt_tmp"
    
    
    
  as (
    

select distinct *
,SYSDATE as ads_dtm_created
,SYSDATE as ads_dtm_last_updated
from "dev"."timothy_chan"."outcome_raw_data"
  );
  