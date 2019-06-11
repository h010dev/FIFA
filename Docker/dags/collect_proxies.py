from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.sensors import ExternalTaskSensor
from airflow.operators.dagrun_operator import TriggerDagRunOperator
from datetime import datetime, timedelta
from initialize_databases import initdb_useragent, initdb_proxy


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2019, 6, 10),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=2)
}

dag = DAG(
    dag_id='collect_proxies',
    default_args=default_args,
    schedule_interval='*/5 * * * *',
    catchup=False
)

collect_proxies = BashOperator(
    task_id='get_proxies',
    bash_command=\
    "cd /FIFA/fifa_data/ && python3 -m fifa_data.spiders.fate_proxy ",
    dag=dag
)
