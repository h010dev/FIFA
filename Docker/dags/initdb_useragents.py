from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.docker_operator import DockerOperator
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


with DAG(
        dag_id='initdb_useragents',
        description="Import user agents into database.",
        default_args=default_args,
        schedule_interval='@once'
        ) as dag:

    inituseragentdb_task = BashOperator(
        task_id='useragent_initdb',
        bash_command=\
        "cd /FIFA/fifa_data/ && python3 -m user_agents.useragent_update ",
    )
