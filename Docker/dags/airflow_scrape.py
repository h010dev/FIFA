from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime.today(),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=2)
}


with DAG('proxy_dag', default_args=default_args,
         schedule_interval='*/15 * * * *') as dag:
    proxy_task =
        BashOperator(
        task_id='get_proxies',
        bash_command=\
        "cd /FIFA/fifa_data/ && python3 -m fifa_data.spiders.fate_proxy",
        dag=dag)

# TODO 
""" look for a way to schedule dags to stop after certain time interval.
reference airflow.sensors.time_delta_sensor for more info."""

with DAG('useragent_dag', default_args=default_args,
         schedulele_interval='@weekly') as dag:
        BashOperator(
        task_id='get_useragents',
        bash_command=\
        "cd /FIFA/fifa_data/ && python3 -m fifa_data.spiders.user_agent_scraper",
        dag=dag)
