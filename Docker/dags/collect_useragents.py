from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.docker_operator import DockerOperator
from datetime import datetime, timedelta


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
    dag_id='collect_useragents',
    description='Start collecting useragents every day.',
    default_args=default_args,
    schedule_interval='*/5 * * * *',
    catchup=False
)

collect_useragents = BashOperator(
    task_id='get_useragents',
    bash_command=\
    "cd /FIFA/fifa_data/ && python3 -m fifa_data.spiders.user_agent_scraper ",
    dag=dag
)
