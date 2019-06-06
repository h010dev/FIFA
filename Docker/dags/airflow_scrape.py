from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2019, 6, 5),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=2)
}

dag = DAG('airflow_scrape', default_args=default_args, \
          schedule_interval=timedelta(days=1))

t1 = BashOperator(
    task_id='get_useragents',
    bash_command=\
    "cd /FIFA/fifa_data/ && python3 -m fifa_data.spiders.user_agent_scraper",
    dag=dag)

t2 = BashOperator(
    task_id='get_proxies',
    bash_command=\
    "cd /FIFA/fifa_data/ && python3 -m fifa_data.spiders.fate_proxy",
    dag=dag)
