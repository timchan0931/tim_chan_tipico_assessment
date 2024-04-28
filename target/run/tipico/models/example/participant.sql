
  
    

  create  table
    "dev"."timothy_chan"."participant__dbt_tmp"
    
    
    
  as (
    

with participant as (
    select 
    35458 as id
    ,'George Washington ' as name
    ,'HOME' as position
    ,'GEO' as abbreviation
)
select *
from participant
  );
  