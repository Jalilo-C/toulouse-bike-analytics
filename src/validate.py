import math
from datetime import datetime

def validate_station_infos(stations):
    # Checking existing data
    if not isinstance(stations, list) or not stations:
        raise ValueError("Stations must be a non-empty list")

    for station in stations:
        # Checking missing keys
        if "station_id" not in station:
            raise ValueError("Data error: missing primary key station_id")
        
        if "name" not in station:
            raise ValueError("Data error: missing name")

        if "lon" not in station:
            raise ValueError("Data error: missing lon")

        if "lat" not in station:
            raise ValueError("Data error: missing lat")

        # Getting keys data
        station_id = station["station_id"]

        name_data = station["name"]
        if not isinstance(name_data, list) or not name_data:
            raise ValueError("Data error: name must be a non-empty list")
        if not isinstance(name_data[0], dict):
            raise ValueError("Data error: invalid name structure")
        name = name_data[0].get("text")
        
        lat = station["lat"]
        lon = station["lon"]
        address = station.get("address")
        capacity = station.get("capacity")

        # Checking data types
        if not isinstance(station_id, str) or not station_id.strip():
            raise ValueError("Data error: station_id must be a non-empty string")

        if not isinstance(name, str) or not name.strip():
            raise ValueError("Data error: name must be a non-empty string")

        if not isinstance(lat, (int,float)) or isinstance(lat, bool) or not math.isfinite(lat):
            raise ValueError("Data error: lat must be a finite number")

        if not isinstance(lon, (int,float)) or isinstance(lon, bool) or not math.isfinite(lon):
            raise ValueError("Data error: lon must be a finite number")
            
        if address is not None:
            if not isinstance(address, str):
                raise ValueError("Data error: address must be a string")

        if capacity is not None:
            if not isinstance(capacity, int) or isinstance(capacity, bool):
                raise ValueError("Data error: capacity must be an int")

        # Checking data rules
        if lon<-180 or lon>180:
            raise ValueError("Value error: lon must be between -180 and 180")
        
        if lat<-90 or lat>90:
            raise ValueError("Value error: lat must be between -90 and 90")

        if capacity is not None:
            if capacity<0:
                raise ValueError("Value error: capacity must be a non-negative")

    return stations

def validate_station_status(stations):
    # Checking existing data
    if not isinstance(stations, list) or not stations:
         raise ValueError("Stations must be a non-empty list")

    for station in stations:
        # Checking missing keys
        if "station_id" not in station:
            raise ValueError("Data error: missing primary key station_id")

        # Getting keys data
        station_id = station["station_id"]
        num_vehicles_available = station.get("num_vehicles_available")
        num_vehicles_disabled = station.get("num_vehicles_disabled")
        num_docks_available = station.get("num_docks_available")
        num_docks_disabled = station.get("num_docks_disabled")
        is_renting = station.get("is_renting")
        is_returning = station.get("is_returning")
        last_reported = station.get("last_reported")

        # Checking data types
        if not isinstance(station_id, str) or not station_id.strip():
            raise ValueError("Data error: station_id must be a non-empty string")

        if num_vehicles_available is not None:
            if not isinstance(num_vehicles_available, int) or isinstance(num_vehicles_available, bool):
                raise ValueError("Data error: num_vehicles_available must be an int")

        if num_vehicles_disabled is not None:
            if not isinstance(num_vehicles_disabled, int) or isinstance(num_vehicles_disabled, bool):
                raise ValueError("Data error: num_vehicles_disabled must be an int")

        if num_docks_available is not None:
            if not isinstance(num_docks_available, int) or isinstance(num_docks_available, bool):
                raise ValueError("Data error: num_docks_available must be an int")

        if num_docks_disabled is not None:
            if not isinstance(num_docks_disabled, int) or isinstance(num_docks_disabled, bool):
                raise ValueError("Data error: num_docks_disabled must be an int")

        if is_renting is not None:
            if not isinstance(is_renting, bool):
                raise ValueError("Data error: is_renting must be a bool")

        if is_returning is not None:
            if not isinstance(is_returning, bool):
                raise ValueError("Data error: is_returning must be a bool")

        if last_reported is not None:
            if not isinstance(last_reported, str) or not last_reported.strip():
                raise ValueError(
                    "DATA Error : last_reported must be a non-empty string"
                )
            try:
                parsed_date = datetime.fromisoformat(
                    last_reported.replace("Z", "+00:00")
                )
            except ValueError:
                raise ValueError(
                    f"Invalid ISO 8601 timestamp: {last_reported}"
                )
            if parsed_date.tzinfo is None:
                raise ValueError(
                    "Invalid timestamp: timezone information is missing"
                )

        # Checking vehicle types (mechanical and electrical)
        vehicle_types = station.get("vehicle_types_available")

        if vehicle_types is not None:
            if not isinstance(vehicle_types, list):
                raise ValueError(
                    "Data error: vehicle_types_available must be a list"
                )

            for vehicle in vehicle_types:
                if not isinstance(vehicle, dict):
                    raise ValueError(
                        "Data error: each vehicle type must be a dictionary"
                    )

                vehicle_type_id = vehicle.get("vehicle_type_id")
                count = vehicle.get("count")

                if not isinstance(vehicle_type_id, str) or not vehicle_type_id.strip():
                    raise ValueError(
                        "Data error: vehicle_type_id must be a non-empty string"
                    )

                if not isinstance(count, int) or isinstance(count, bool):
                    raise ValueError(
                        f"Data error: count for {vehicle_type_id} must be an int"
                    )

                if count < 0:
                    raise ValueError(
                        f"Value error: count for {vehicle_type_id} must be non-negative"
                    )

        # Checking data rules
        if num_vehicles_available is not None:
            if num_vehicles_available<0:
                raise ValueError("Value error: num_vehicles_available must be a non-negative")

        if num_vehicles_disabled is not None:
            if num_vehicles_disabled<0:
                raise ValueError("Value error: num_vehicles_disabled must be a non-negative")

        if num_docks_available is not None:
            if num_docks_available<0:
                raise ValueError("Value error: num_docks_available must be a non-negative")

        if num_docks_disabled is not None:
            if num_docks_disabled<0:
                raise ValueError("Value error: num_docks_disabled must be a non-negative")

    return stations