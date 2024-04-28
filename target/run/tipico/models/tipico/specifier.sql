
  
    

  create  table
    "dev"."timothy_chan"."specifier__dbt_tmp"
    
    
    
  as (
    

with specifier as (
    select 
    'OVER_UNDER' as key
    ,'5.5' as value
    ,'DOUBLE' as type
)
select *
from specifier
  );
  