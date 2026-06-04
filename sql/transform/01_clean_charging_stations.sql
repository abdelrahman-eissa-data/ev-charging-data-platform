-- =====================================================
-- Clean Charging Stations
-- Project: EV Charging Data Platform
-- Layer: Transform
-- Source: stg_charging_stations
-- Target: clean_charging_stations
-- =====================================================

DROP TABLE IF EXISTS clean_charging_stations;

CREATE TABLE clean_charging_stations AS
SELECT
    station_id,
    station_name,
    city,
    postcode,
    latitude,
    longitude,
    number_of_points,
    power_kw,
    connection_type_id
FROM stg_charging_stations
WHERE station_id IS NOT NULL
  AND power_kw IS NOT NULL
  AND power_kw > 0;


-- =====================================================
-- Optional Performance Indexes
-- These indexes support common joins and filters.
-- =====================================================

CREATE INDEX IF NOT EXISTS idx_clean_charging_stations_station_id
ON clean_charging_stations(station_id);

CREATE INDEX IF NOT EXISTS idx_clean_charging_stations_city
ON clean_charging_stations(city);


-- =====================================================
-- Validation Queries
-- These queries are used to validate the transformation result.
-- =====================================================

-- Compare row counts before and after cleaning
SELECT COUNT(*) AS stg_charging_stations_rows
FROM stg_charging_stations;

SELECT COUNT(*) AS clean_charging_stations_rows
FROM clean_charging_stations;


-- Show invalid records in staging table
-- This may return rows because staging contains data as loaded
SELECT *
FROM stg_charging_stations
WHERE power_kw IS NULL
   OR power_kw <= 0;


-- Check invalid records after cleaning
-- Expected result: 0 rows
SELECT *
FROM clean_charging_stations
WHERE power_kw IS NULL
   OR power_kw <= 0;


-- Check whether PostgreSQL uses an index for station_id filtering
EXPLAIN ANALYZE
SELECT *
FROM clean_charging_stations
WHERE station_id = 487807;