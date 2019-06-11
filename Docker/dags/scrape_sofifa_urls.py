from airflow import DAG
from airflow.operators.bash_operator import BashOperator
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
    dag_id='collect_sofifa_urls',
    default_args=default_args,
    schedule_interval='*/5 * * * *',
    catchup=False
)

collect_club_urls = BashOperator(
    task_id='get_club_urls',
    bash_command=\
    "cd /FIFA/fifa_data/ && python3 -m fifa_data.spiders.sofifa_club_urls ",
    dag=dag
)

collect_team_urls = BashOperator(
    task_id='get_team_urls',
    bash_command=\
    "cd /FIFA/fifa_data/ && python3 -m fifa_data.spiders.sofifa_team_urls ",
    dag=dag
)

collect_club_urls
collect_team_urls
