### Assessment Details
- Name: Timothy Chan
- Position: Data Engineer (Hoboken, NJ)

### Instructions
Run the following commands to start up Airflow
- unzip chan_timothy_tipico_assessment.zip
- cd tipico_git/airflow
- airflow standalone

Run the following commands to run the dbt models and data ingestion standalone (outside of airflow)
- /usr/bin/python3 /User/tim/tipico_git/ingestions/tipico_api_pull.py
- dbt run
