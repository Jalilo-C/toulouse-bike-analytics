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
        return run_pipeline(logical_date)

    @task
    def quality_check(expected_count):
        from src.database import get_connection

        context = get_current_context()
        logical_date = context["logical_date"]

        with get_connection() as conn:
            with conn.cursor() as cur: 
                query_nb_stations_per_snapshot = """
                            SELECT COUNT(*)
                            FROM station_status
                            WHERE collected_at = %s
                        """

                cur.execute(query_nb_stations_per_snapshot, (logical_date,))
                nb_stations_per_snapshot = cur.fetchone()[0]

        print(f"NB stations per snapshot: {nb_stations_per_snapshot}")
        print(f"Expected count : {expected_count}")

        if nb_stations_per_snapshot == 0:
            raise ValueError("DATA Error: snapshot is empty")

        if nb_stations_per_snapshot!=expected_count:
            raise ValueError("DATA Error: station count mismatch")
    
    etl = run_etl()
    quality_check(etl)

toulouse_bike_pipeline()
