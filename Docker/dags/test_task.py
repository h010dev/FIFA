from datetime import datetime, timedelta
from airflow.operators import DummyOperator
from airflow.utils.trigger_rule import TriggerRule
from airflow.models import TaskInstance
from airflow import DAG
import pprint

pp = pprint.PrettyPrinter(indent=4)

def dummy_success(context):
    pp.pprint(context)

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2019, 6, 14),
    'retries': 1,
    'retry_delay': timedelta(minutes=2),
}

dag = DAG(
    dag_id='dummy_dag',
    default_args=default_args,
    schedule_interval='@once',
    catchup=False
)

task_1 = DummyOperator(
    task_id='dummy_task_1',
    trigger_rule=TriggerRule.ALL_SUCCESS,
    on_success_callback=dummy_success,
    dag=dag
)
