
  
    

  create  table
    "dev"."timothy_chan"."group__dbt_tmp"
    
    
    
  as (
    

with group_data as (
    select 
    3686 as id
    ,'Argentina - Primera Nacional' as name
    ,207 as parent_group_country_id
    ,'Argentina' as parent_group_country_name
    ,11 as parent_group_sports_id
    ,'Soccer' as parent_group_sports_name
)
select *
from group_data
  );
  