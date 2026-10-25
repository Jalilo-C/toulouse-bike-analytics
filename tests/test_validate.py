import pytest
from src.validate import validate_station_infos, validate_station_status

# Testing validate_station_infos
def test_valid_station_infos():
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

    result = validate_station_infos(stations)

    assert result == stations

def test_invalid_latitude():
    stations = [
        {
            "station_id": "1",
            "name": [{"language": "fr", "text": "Capitole"}],
            "lat": 180.6045,
            "lon": 1.4442,
            "capacity": 20,
            "address": "Place du Capitole"
        }
    ]

    with pytest.raises(ValueError, match="lat must be between"):
        validate_station_infos(stations)

def test_empty_name():
    stations = [
        {
            "station_id": "1",
            "name": [{"language": "fr", "text": ""}],
            "lat": 8.6045,
            "lon": 1.4442,
            "capacity": 20,
            "address": "Place du Capitole"
        }
    ]

    result = validate_station_infos(stations)

    assert result==stations

def test_negative_capacity():
    stations = [
        {
            "station_id": "1",
            "name": [{"language": "fr", "text": ""}],
            "lat": 8.6045,
            "lon": 1.4442,
            "capacity": -20,
            "address": "Place du Capitole"
        }
    ]

    with pytest.raises(ValueError, match="capacity must be a non-negative"):
        validate_station_infos(stations)

# Testing validate_station_status
def test_valid_station_status():
    stations = [
        {
            "station_id": "1",
            "num_vehicles_available": 8,
            "vehicle_types_available": [
                {
                    "vehicle_type_id": "mechanical",
                    "count": 3
                },
                {
                    "vehicle_type_id": "electrical",
                    "count": 5
                }
            ],
            "num_vehicles_disabled": 1,
            "num_docks_available": 12,
            "num_docks_disabled": 0,
            "is_installed": True,
            "is_renting": True,
            "is_returning": True,
            "last_reported": "2026-10-25T09:55:00Z"
        }
    ]

    result = validate_station_status(stations)

    assert result==stations

def test_negative_vehicles_available():
    stations = [
        {
            "station_id": "1",
            "num_vehicles_available": -3,
            "vehicle_types_available": [
                {
                    "vehicle_type_id": "mechanical",
                    "count": 3
                },
                {
                    "vehicle_type_id": "electrical",
                    "count": 5
                }
            ],
            "num_vehicles_disabled": 1,
            "num_docks_available": 12,
            "num_docks_disabled": 0,
            "is_installed": True,
            "is_renting": True,
            "is_returning": True,
            "last_reported": "2026-10-25T09:55:00Z"
        }
    ]

    with pytest.raises(ValueError, match="num_vehicles_available must be a non-negative"):
        validate_station_status(stations)

def test_invalid_vehicle_count():
    stations = [
        {
            "station_id": "1",
            "num_vehicles_available": 8,
            "vehicle_types_available": [
                {
                    "vehicle_type_id": "mechanical",
                    "count": 3
                },
                {
                    "vehicle_type_id": "electrical",
                    "count": "5"
                }
            ],
            "num_vehicles_disabled": 1,
            "num_docks_available": 12,
            "num_docks_disabled": 0,
            "is_installed": True,
            "is_renting": True,
            "is_returning": True,
            "last_reported": "2026-10-25T09:55:00Z"
        }
    ]
    
    with pytest.raises(ValueError, match="count for electrical must be an int"):
        validate_station_status(stations)