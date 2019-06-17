import pprint
from datetime import datetime

from airflow.models import DAG
from airflow.operators.bash_operator import BashOperator


args = {
    'start_date': datetime(2019, 6, 15),
    'owner': 'airflow',
}

dag = DAG(
    dag_id='sofifascraper_dag',
    default_args=args,
    schedule_interval='@once',
    catchup=False
)

collect_club_urls = BashOperator(
    task_id='get_cluburls',
    bash_command=\
    "cd /FIFA/fifa_data/ && python3 -m fifa_data.spiders.sofifa_club_urls ",
    dag=dag
)

# collect_team_urls = BashOperator(
#     task_id='get_teamurls',
#     bash_command=\
#     "cd /FIFA/fifa_data/ && python3 -m fifa_data.spiders.sofifa_team_urls ",
#     dag=dag
# )
# 
# collect_player_urls = BashOperator(
#     task_id='get_playerurls',
#     bash_command=\
#     "cd /FIFA/fifa_data/ && python3 -m fifa_data.spiders.sofifa_player_urls ",
#     dag=dag
# )
# 
# scrape_club_urls = BashOperator(
#     task_id='scrape_cluburls',
#     bash_command=\
#     "cd /FIFA/fifa_data/ && python3 -m fifa_data.spiders.sofifa_club_pages ",
#     dag=dag
# )
# 
# scrape_team_urls = BashOperator(
#     task_id='scrape_teamurls',
#     bash_command=\
#     "cd /FIFA/fifa_data/ && python3 -m fifa_data.spiders.sofifa_team_pages ",
#     dag=dag
# )
# 
# scrape_player_urls = BashOperator(
#     task_id='scrape_playerurls',
#     bash_command=\
#     "cd /FIFA/fifa_data/ && python3 -m fifa_data.spiders.sofifa_player_pages ",
#     dag=dag
# )

# collect_club_urls >> scrape_club_urls
# collect_team_urls >> scrape_team_urls
# collect_player_urls >> scrape_player_urls
