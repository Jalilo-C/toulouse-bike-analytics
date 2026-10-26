import psycopg
from datetime import datetime, timezone
from src.load import load_station_infos, load_station_status
import os
from dotenv import load_dotenv

load_dotenv()

conn = psycopg.connect(
    host=os.environ["POSTGRES_HOST"],
    port=int(os.environ["POSTGRES_PORT"]),
    dbname=os.environ["POSTGRES_DB"],
    user=os.environ["POSTGRES_USER"],
    password=os.environ["POSTGRES_PASSWORD"]
)

stations = [
    {
        "station_id": "TEST_001",
        "name": "Station Test",
        "lat": 43.6045,
        "lon": 1.4442,
        "address": "Adresse Test",
        "capacity": 20
    }
]

collected_at = datetime(2026, 10, 26, 10, 0, tzinfo=timezone.utc)

status = [
    {
        "station_id": "TEST_001",
        "collected_at": collected_at,
        "mechanical_bikes_available": 3,
        "electric_bikes_available": 5,
        "total_bikes_available": 8,
        "bikes_disabled": 1,
        "docks_available": 12,
        "docks_disabled": 0,
        "is_renting": True,
        "is_returning": True,
        "source_last_updated": "2026-10-26T09:55:00Z",
        "last_reported": "2026-10-26T09:50:00Z"
    }
]

try:
    # Insert station information first (foreign key)
    load_station_infos(conn, stations)

    # First status insertion
    load_station_status(conn, status)

    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT COUNT(*)
            FROM station_status
            WHERE station_id = %s AND collected_at = %s
            """,
            ("TEST_001", collected_at)
        )

        count = cur.fetchone()[0]
        assert count == 1

    print("First insertion successful")

    # Insert the same snapshot again
    load_station_status(conn, status)

    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT COUNT(*)
            FROM station_status
            WHERE station_id = %s AND collected_at = %s
            """,
            ("TEST_001", collected_at)
        )

        count = cur.fetchone()[0]
        assert count == 1

    print("Idempotence verified: no duplicate inserted")

finally:
    conn.rollback()
    conn.close()
    print("Rollback executed and connection closed")
