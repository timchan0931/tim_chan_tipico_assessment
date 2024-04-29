
  
    

  create  table
    "dev"."timothy_chan"."group__dbt_tmp"
    
    
    
  as (
    

select distinct *
,SYSDATE as ads_dtm_created
,SYSDATE as ads_dtm_last_updated
from "dev"."timothy_chan"."group_raw_data_test"
  );
  