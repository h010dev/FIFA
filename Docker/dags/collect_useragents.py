import pprint
from datetime import datetime

from airflow.models import DAG
from airflow.operators.bash_operator import BashOperator

pp = pprint.PrettyPrinter(indent=4)

args = {
    'start_date': datetime(2019, 6, 15),
    'owner': 'airflow',
}

dag = DAG(
    dag_id='useragentscraper_dag',
    default_args=args,
    schedule_interval='@once',
    catchup=False
)

collect_useragents = BashOperator(
    task_id='get_useragents',
    bash_command=\
    "cd /FIFA/fifa_data/ && python3 -m fifa_data.spiders.user_agent_scraper ",
    dag=dag
)
