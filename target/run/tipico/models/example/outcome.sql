
  
    

  create  table
    "dev"."timothy_chan"."outcome__dbt_tmp"
    
    
    
  as (
    

with outcome as (
    select 
    '7057b856-a383-3831-8a87-5ea76f9fa317' as id
    ,'Over 23.5' as name
    ,true as isTraded
    ,1.95 as formatDecimal
    ,1.80 as formatAmerican
    ,'ONGOING' as status
    ,1.80 as trueOdds
)
select *
from outcome
  );
  