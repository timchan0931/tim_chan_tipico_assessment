
  
    

  create  table
    "dev"."timothy_chan"."my_first_dbt_model__dbt_tmp"
    
    
    
  as (
    /*
    Welcome to your first dbt model!
    Did you know that you can also configure models directly within SQL files?
    This will override configurations stated in dbt_project.yml

    Try changing "table" to "view" below
*/

-- 

-- with source_data as (

--     select 
--     1 as id
--     ,'Dougherty K' as participants 
-- )
-- select *
-- from source_data

/*
    Uncomment the line below to remove records with null `id` values
*/

-- where id is not null
  );
  