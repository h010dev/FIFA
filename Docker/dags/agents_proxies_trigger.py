import pprint
from datetime import datetime

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.dagrun_operator import TriggerDagRunOperator
from airflow.utils.trigger_rule import TriggerRule


pp = pprint.PrettyPrinter(indent=4)


def conditionally_trigger(context, dag_run_obj):
    """This function decides whether or not to Trigger the remote DAG"""
    c_p = context['params']['condition_param']
    print("Controller DAG : conditionally_trigger = {}".format(c_p))
    if context['params']['condition_param']:
        dag_run_obj.payload = {'message': context['params']['message']}
        pp.pprint(dag_run_obj.payload)
        return dag_run_obj
    return None


# Define the DAG
dag = DAG(
    dag_id='initdb_controller_dag',
    default_args={
        "owner": "airflow",
        # TODO use current date without harming dag functionality
        "start_date": datetime(2019, 6, 15),
        "depends_on_past": False
    },
    schedule_interval='@once',
    catchup=False
)

# Define the single task in this controller example DAG
trigger_useragent = TriggerDagRunOperator(
    task_id='trigger_useragentscraper',
    trigger_dag_id='useragentscraper_dag',
    python_callable=conditionally_trigger,
    params={'condition_param': True, 'message': 'triggering ua scraper'},
    trigger_rule=TriggerRule.ALL_SUCCESS,
    dag=dag
)

trigger_proxy = TriggerDagRunOperator(
    task_id='trigger_proxyscraper',
    trigger_dag_id='proxyscraper_dag',
    python_callable=conditionally_trigger,
    params={'condition_param': True, 'message': 'triggering proxy scraper'},
    trigger_rule=TriggerRule.ALL_SUCCESS,
    dag=dag
)

trigger_sofifa = TriggerDagRunOperator(
    task_id='trigger_sofifacraper',
    trigger_dag_id='sofifascraper_dag',
    python_callable=conditionally_trigger,
    params={'condition_param': True, 'message': 'triggering sofifa scraper'},
    trigger_rule=TriggerRule.ALL_SUCCESS,
    # TODO add a time delay to wait for n amount of proxies/agents to be
    # collected
    dag=dag
)

# Custom task to start before trigger

initdb_useragent = BashOperator(
    task_id='useragent_initdb',
    bash_command=\
    "cd /FIFA/fifa_data/ && python3 -m user_agents.useragent_update ",
    dag=dag
)

initdb_proxy = BashOperator(
    task_id='proxy_initdb',
    bash_command=\
    "cd /FIFA/fifa_data/ && python3 -m proxies.proxy_update ",
    dag=dag
)

[initdb_useragent, initdb_proxy] >> trigger_useragent
[initdb_useragent, initdb_proxy] >> trigger_proxy
[initdb_useragent, initdb_proxy] >> trigger_sofifa
