### Assessment Details
- Name: Timothy Chan
- Position: Data Engineer (Hoboken, NJ)

### Instructions
Run the following commands to start up Airflow
Note: I am using Airflow 2.6.1
- Run: tipico_ddls.sql on Redshift database under dev.timothy_chan
- Run: git clone git@github.com:timchan0931/tim_chan_tipico_assessment.git
- Run: cd tipico_git/airflow
- Run: airflow standalone

Run the following commands to run the dbt models and data ingestion standalone (outside of airflow)
Note: Before running dbt run, please make sure you are in /tipico_git.  The Airflow dag, navigates one directory back to (tipico_git/) before running the dbt commands.
- Navigate to directory that you cloned my repo in
- Run: python3 ingestions/tipico_api_pull.py
- Run: dbt run
