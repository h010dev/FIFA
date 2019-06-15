 # from airflow import DAG
 # from airflow.operators.bash_operator import BashOperator
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
 # initdb_useragent
 # initdb_proxy
