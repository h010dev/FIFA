import pprint
from datetime import datetime

from airflow.models import DAG, Variable
from airflow.operators.bash_operator import BashOperator


pp = pprint.PrettyPrinter(indent=4)

useragent_vars = Variable.get("USER_AGENT_SCRAPER", deserialize_json=True)
quantity = useragent_vars["quantity"]
duration = useragent_vars["duration"]
backup_frequency = useragent_vars["backup_frequency"]

args = {
    # TODO use current date without harming dag functionality
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

move_useragents = BashOperator(
    task_id='move_useragents',
    bash_command="cd /fifa_data && python3 redis_to_mongodb.py --keys='' "
    "--db='agents_proxies' --collection='user_agents'",
    dag=dag
)

collect_useragents >> move_useragents
