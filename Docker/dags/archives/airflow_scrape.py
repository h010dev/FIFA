# from airflow import DAG
# from airflow.operators.bash_operator import BashOperator
# from airflow.operators.sensors import ExternalTaskSensor
# from datetime import datetime, timedelta
# 
# 
# default_args = {
#     'owner': 'airflow',
#     'depends_on_past': False,
#     'start_date': datetime.today(),
#     'email_on_failure': False,
#     'email_on_retry': False,
#     'retries': 1,
#     'retry_delay': timedelta(minutes=2)
# }
# 
# 
# dag = DAG(
#     dag_id='initialize_db',
#     description="Set up database for user agents and proxies.",
#     default_args=default_args,
#     schedule_interval='@once'
# )
# 
# waiting_dag = DAG(
#     dag_id='wait_for_initdb',
#     description='Wait for database initialization to complete',
#     default_args=default_args,
#     schedule_interval=None
# )
# 
# proxy_dag = DAG(
#     dag_id='collect_proxies',
#     description='Start collecting proxies every 15 minutes.',
#     default_args=default_args,
#     schedule_interval='*/15 * * * *'
# )
# 
# useragent_dag = DAG(
#     dag_id='collect_useragents',
#     description='Start collecting useragents every day.',
#     default_args=default_args,
#     schedule_interval='@daily'
# )
# 
# initdb_useragent = BashOperator(
#     task_id='useragent_initdb',
#     bash_command=\
#     "cd /FIFA/fifa_data/ && python3 -m user_agents.useragent_update ",
#     dag=dag
# )
# 
# initdb_proxy = BashOperator(
#     task_id='proxy_initdb',
#     bash_command=\
#     "cd /FIFA/fifa_data/ && python3 -m proxies.proxy_update ",
#     dag=dag
# )
# 
# wait_for_useragent_initdb = ExternalTaskSensor(
#     task_id='wait_for_useragent_database_initialization',
#     external_dag_id='initialize_db',
#     external_task_id='useragent_initdb',
#     dag=dag
# )
# 
# wait_for_proxy_initdb = ExternalTaskSensor(
#     task_id='wait_for_proxy_database_initialization',
#     external_dag_id='initialize_db',
#     external_task_id='proxy_initdb',
#     dag=dag
# )
# 
# collect_proxies = BashOperator(
#     task_id='get_proxies',
#     bash_command=\
#     "cd /FIFA/fifa_data/ && python3 -m fifa_data.spiders.fate_proxy ",
#     dag=dag
# )
# 
# collect_useragents = BashOperator(
#     task_id='get_useragents',
#     bash_command=\
#     "cd /FIFA/fifa_data/ && python3 -m fifa_data.spiders.user_agent_scraper ",
#     dag=dag
# )
# 
# #[initdb_useragent, initdb_proxy] >> collect_useragents
# #[initdb_useragent, initdb_proxy] >> collect_proxies
# 
# 
# initdb_useragent >> wait_for_useragent_initdb
# initdb_proxy >> wait_for_proxy_initdb
# [wait_for_proxy_initdb, wait_for_useragent_initdb] >> collect_useragents
# [wait_for_proxy_initdb, wait_for_useragent_initdb] >> collect_proxies
