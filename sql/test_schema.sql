-- TEST 1: Insert a valid station
-- Expected: successful insertion
BEGIN TRANSACTION;

INSERT INTO station_infos (station_id, name, lat, lon, capacity)
VALUES ('1', 'station A', 20, -50.999, 15);

ROLLBACK;


-- TEST 2: Insert a station with an invalid latitude
-- Expected: CHECK constraint violation
BEGIN TRANSACTION;

INSERT INTO station_infos (station_id, name, lat, lon, capacity)
VALUES ('2', 'station B', -100, 120, 17);

ROLLBACK;


-- TEST 3: Insert a status for a non-existent station
-- Expected: FOREIGN KEY constraint violation
BEGIN TRANSACTION;

INSERT INTO station_status (station_id, collected_at, total_bikes_available)
VALUES ('999', '2026-10-22 12:00:00+00', 8);

ROLLBACK;


-- TEST 4: Insert two observations for the same station
-- Expected: both observations are stored successfully
BEGIN TRANSACTION;

INSERT INTO station_infos (station_id, name, lat, lon, capacity)
VALUES ('1', 'station A', 20, -50.999, 15);

INSERT INTO station_status (station_id, collected_at, total_bikes_available)
VALUES ('1', '2026-10-22 12:00:00+00', 8);

INSERT INTO station_status (station_id, collected_at, total_bikes_available)
VALUES ('1', '2026-10-22 14:00:00+00', 8);

SELECT station_id, collected_at, total_bikes_available
FROM station_status
WHERE station_id = '1'
ORDER BY collected_at;

ROLLBACK;


-- TEST 5: Prevent duplicate observations with ON CONFLICT
-- Expected: the original value (8) remains unchanged
BEGIN TRANSACTION;

INSERT INTO station_infos (station_id, name, lat, lon, capacity)
VALUES ('1', 'station A', 20, -50.999, 15);

INSERT INTO station_status (station_id, collected_at, total_bikes_available)
VALUES ('1', '2026-10-22 12:00:00+00', 8);

INSERT INTO station_status (station_id, collected_at, total_bikes_available)
VALUES ('1', '2026-10-22 12:00:00+00', 10)
ON CONFLICT (station_id, collected_at) DO NOTHING;

SELECT station_id, collected_at, total_bikes_available
FROM station_status
WHERE station_id = '1';

ROLLBACK;