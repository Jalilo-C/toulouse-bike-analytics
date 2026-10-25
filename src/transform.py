def transform_station_infos(stations):
    transformed_stations = []

    for station in stations:
        name = station["name"][0]["text"].strip()
        new_station = {
            "station_id": station["station_id"],
            "name": name if name else None,
            "lat": station["lat"],
            "lon": station["lon"],
            "address": station.get("address"),
            "capacity": station.get("capacity")
        }

        transformed_stations.append(new_station)

    return transformed_stations

def transform_station_status(last_updated, stations, collected_at):
    transformed_stations = []

    for station in stations:
        mechanical_bikes_available = None
        electric_bikes_available = None

        for vehicle in station.get("vehicle_types_available") or []:
            if vehicle["vehicle_type_id"]=="mechanical":
                mechanical_bikes_available = vehicle["count"]
            elif vehicle["vehicle_type_id"]=="electrical":
                electric_bikes_available = vehicle["count"]

        new_station = {
            "station_id": station["station_id"],
            "collected_at": collected_at,
            "mechanical_bikes_available": mechanical_bikes_available,
            "electric_bikes_available": electric_bikes_available,
            "total_bikes_available": station.get("num_vehicles_available"),
            "bikes_disabled": station.get("num_vehicles_disabled"),
            "docks_available": station.get("num_docks_available"),
            "docks_disabled": station.get("num_docks_disabled"),
            "is_renting": station.get("is_renting"),
            "is_returning": station.get("is_returning"),
            "source_last_updated": last_updated,
            "last_reported": station.get("last_reported")
        }

        transformed_stations.append(new_station)
        
    return transformed_stations