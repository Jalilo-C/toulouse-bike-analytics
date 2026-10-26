def load_station_infos(conn, stations):
    with conn.cursor() as cur:
        for station in stations:
            cur.execute(
                """
                INSERT INTO station_infos (station_id, name, lat, lon, address, capacity)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (station_id)
                DO UPDATE SET
                    name = EXCLUDED.name,
                    lat = EXCLUDED.lat,
                    lon = EXCLUDED.lon,
                    address = EXCLUDED.address,
                    capacity = EXCLUDED.capacity;
                """,
                (
                    station["station_id"], 
                    station["name"], 
                    station["lat"], 
                    station["lon"], 
                    station["address"], 
                    station["capacity"]
                )
            )

def load_station_status(conn, stations):
    with conn.cursor() as cur:
        for station in stations:
            cur.execute(
                """
                INSERT INTO station_status (
                                station_id, 
                                collected_at, 
                                mechanical_bikes_available, 
                                electric_bikes_available, 
                                total_bikes_available, 
                                bikes_disabled,
                                docks_available,
                                docks_disabled,
                                is_renting,
                                is_returning,
                                source_last_updated,
                                last_reported
                            )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (station_id, collected_at)
                DO NOTHING
                """,
                (
                    station["station_id"],
                    station["collected_at"],
                    station["mechanical_bikes_available"],
                    station["electric_bikes_available"],
                    station["total_bikes_available"],
                    station["bikes_disabled"],
                    station["docks_available"],
                    station["docks_disabled"],
                    station["is_renting"],
                    station["is_returning"],
                    station["source_last_updated"],
                    station["last_reported"]
                )
            )