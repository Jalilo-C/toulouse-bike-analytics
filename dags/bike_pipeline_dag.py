from airflow.sdk import dag, task
from datetime import timedelta
import pendulum
from airflow.sdk import get_current_context

@dag (
    dag_id = "toulouse_bikes_pipeline",
    start_date = pendulum.datetime(2026, 10, 29, tz="UTC"),
    schedule="*/15 * * * *",
    catchup = False,
    default_args = {
        "retries": 2,
        "retry_delay": timedelta(minutes=2)
    },
    max_active_runs = 1,
    tags = ["toulouse", "data engineering"]
)
def toulouse_bike_pipeline():

    @task
    def run_etl():
        from src.main import run_pipeline
        context = get_current_context()
        logical_date = context["logical_date"]
        run_pipeline(logical_date)

    run_etl()

toulouse_bike_pipeline()
