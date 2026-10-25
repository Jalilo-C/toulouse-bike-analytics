-- Stores general information about each bike-sharing station.
-- Each row represents one unique station.
CREATE TABLE station_infos(
    station_id TEXT,
    name TEXT,
    lat NUMERIC(9,6),
    lon NUMERIC(9,6),
    address TEXT,
    capacity INTEGER,

    CONSTRAINT pk_station_infos PRIMARY KEY (station_id),
    CONSTRAINT ck_lon CHECK (lon>=-180 AND lon<=180),
    CONSTRAINT ck_lat CHECK (lat>=-90 AND lat<=90),
    CONSTRAINT ck_capacity CHECK (capacity>=0)
);

-- Stores the history of bike and dock availability for each station.
-- Each row represents a station's status at a specific collection time.
CREATE TABLE station_status(
    station_id TEXT NOT NULL,
    collected_at TIMESTAMPTZ NOT NULL,
    mechanical_bikes_available INTEGER,
    electric_bikes_available INTEGER,
    total_bikes_available INTEGER,
    bikes_disabled INTEGER,
    docks_available INTEGER,
    docks_disabled INTEGER,
    is_renting BOOLEAN,
    is_returning BOOLEAN,
    source_last_updated TIMESTAMPTZ,
    last_reported TIMESTAMPTZ,

    CONSTRAINT pk_station_status PRIMARY KEY (station_id, collected_at),
    CONSTRAINT fk_station_id FOREIGN KEY (station_id)
    REFERENCES station_infos(station_id),
    CONSTRAINT ck_no_negative_value CHECK (
        mechanical_bikes_available>=0 AND
        electric_bikes_available>=0 AND
        total_bikes_available>=0 AND
        bikes_disabled>=0 AND
        docks_available>=0 AND
        docks_disabled>=0
    )
);
