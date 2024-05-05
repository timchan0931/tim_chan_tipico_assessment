### Assessment Details
- Name: Timothy Chan
- Position: Data Engineer (Hoboken, NJ)

### Instructions
Run the following commands to start up Airflow
- Run: unzip chan_timothy_tipico_assessment.zip
- Run: cd tipico_git/airflow
- Run: airflow standalone

Run the following commands to run the dbt models and data ingestion standalone (outside of airflow)
- Navigate to directory that you unzipped chan_timothy_tipico_assessment.zip in
- Run: python3 ingestions/tipico_api_pull.py
- Run: dbt run
