import pprint
from datetime import datetime

from airflow.models import DAG
from airflow.operators.bash_operator import BashOperator


pp = pprint.PrettyPrinter(indent=4)

args = {
    # TODO use current date without harming dag functionality
    'start_date': datetime(2019, 6, 15),
    'owner': 'airflow',
}

dag = DAG(
    dag_id='proxyscraper_dag',
    default_args=args,
    schedule_interval='*/15 * * * *',
    catchup=False
)

collect_proxies = BashOperator(
    task_id='get_proxies',
    bash_command=\
    "cd /FIFA/fifa_data/ && python3 -m fifa_data.spiders.fate_proxy ",
    dag=dag
)
