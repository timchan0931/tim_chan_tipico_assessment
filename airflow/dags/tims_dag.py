from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': True,
    'start_date': datetime(2024, 5, 4),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=5),
    # Run every 10 minutes
    'schedule_interval': '*/10 * * * *',
    'catchup': False
}

dag = DAG('tipico',
          default_args=default_args,
          schedule_interval='*/10 * * * *')

# Pull Tipico Data from API and populate staging tables
pull_tipico_api_and_populate_stage = BashOperator(
    task_id='run_tipico_script',
    bash_command='/usr/local/bin/python3 /Users/tim/tipico_git/ingestions/tipico_api_pull.py' ,
    dag=dag
)

# Populate dim_event
dbt_dim_event = BashOperator(
    task_id='run_dbt_dim_event',
    bash_command='cd /Users/tim/tipico_git && dbt run --select dim_event' ,
    dag=dag
)

# Populate dim_participant
dbt_dim_participant = BashOperator(
    task_id='run_dbt_dim_participant',
    bash_command='cd /Users/tim/tipico_git && dbt run --select dim_participant' ,
    dag=dag
)

# Populate dim_event_dtls
dbt_dim_event_dtls = BashOperator(
    task_id='run_dbt_event_dtls',
    bash_command='cd /Users/tim/tipico_git && dbt run --select dim_event_dtls' ,
    dag=dag
)

# Populate dim_group
dbt_dim_group= BashOperator(
    task_id='run_dbt_group',
    bash_command='cd /Users/tim/tipico_git && dbt run --select dim_group' ,
    dag=dag
)

# Populate dim_outcome
dbt_dim_outcome= BashOperator(
    task_id='run_dbt_outcome',
    bash_command='cd /Users/tim/tipico_git && dbt run --select dim_outcome' ,
    dag=dag
)

# Populate dim_market
dbt_dim_market= BashOperator(
    task_id='run_dbt_market',
    bash_command='cd /Users/tim/tipico_git && dbt run --select dim_market' ,
    dag=dag
)
# Populate dim_specifier
dbt_dim_specifier= BashOperator(
    task_id='run_dbt_specifier',
    bash_command='cd /Users/tim/tipico_git && dbt run --select dim_specifier' ,
    dag=dag
)


# Run tasks in order
pull_tipico_api_and_populate_stage>>dbt_dim_market>>dbt_dim_event>>dbt_dim_participant>>dbt_dim_event_dtls>>dbt_dim_group>>dbt_dim_outcome>>dbt_dim_specifier