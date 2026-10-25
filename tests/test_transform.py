from datetime import datetime, timezone
from src.transform import transform_station_infos, transform_station_status

# Testing transform_station_infos
def test_transform_station_infos():
    stations = [
        {
            "station_id": "1",
            "name": [{"language": "fr", "text": "Capitole"}],
            "lat": 43.6045,
            "lon": 1.4442,
            "capacity": 20,
            "address": "Place du Capitole"
        }
    ]

    result = transform_station_infos(stations)

    assert result==[
        {
            "station_id": "1",
            "name": "Capitole",
            "lat": 43.6045,
            "lon": 1.4442,
            "capacity": 20,
            "address": "Place du Capitole"
        }
    ]

def test_transform_empty_name():
    stations = [
        {
            "station_id": "1",
            "name": [{"language": "fr", "text": ""}],
            "lat": 43.6045,
            "lon": 1.4442,
            "capacity": 20,
            "address": "Place du Capitole"
        }
    ]

    result = transform_station_infos(stations)

    assert result==[
        {
            "station_id": "1",
            "name": None,
            "lat": 43.6045,
            "lon": 1.4442,
            "capacity": 20,
            "address": "Place du Capitole"
        }
    ]    

# Testing transform_station_status
def test_transform_station_status():
    collected_at = datetime(2026, 10, 25, 10, 0, tzinfo=timezone.utc)
    last_updated = "2026-10-25T09:55:00Z"

    stations = [
        {
            "station_id": "1",
            "num_vehicles_available": 8,
            "vehicle_types_available": [
                {"vehicle_type_id": "mechanical", "count": 3},
                {"vehicle_type_id": "electrical", "count": 5}
            ],
            "num_vehicles_disabled": 1,
            "num_docks_available": 12,
            "num_docks_disabled": 0,
            "is_renting": True,
            "is_returning": True,
            "last_reported": "2026-10-25T09:50:00Z"
        }
    ]

    result = transform_station_status(
        last_updated, stations, collected_at
    )

    assert result==[
        {
            "station_id": "1",
            "collected_at": collected_at,
            "mechanical_bikes_available": 3,
            "electric_bikes_available": 5,
            "total_bikes_available": 8,
            "bikes_disabled": 1,
            "docks_available": 12,
            "docks_disabled": 0,
            "is_renting": True,
            "is_returning": True,
            "source_last_updated": last_updated,
            "last_reported": "2026-10-25T09:50:00Z"
        }
    ]

def test_transform_status_missing_vehicle_types():
    collected_at = datetime(2026, 10, 25, 10, 0, tzinfo=timezone.utc)
    last_updated = "2026-10-25T09:55:00Z"
    
    stations = [
        {
            "station_id": "2",
            "num_vehicles_available": 0
        }
    ]

    result = transform_station_status(last_updated, stations, collected_at)

    assert result[0]["mechanical_bikes_available"] is None
    assert result[0]["electric_bikes_available"] is None
    assert result[0]["total_bikes_available"] == 0