-- =====================================================
-- Clean Weather Data
-- Project: EV Charging Data Platform
-- Layer: Transform
-- Source: stg_weather
-- Target: clean_weather
-- =====================================================

DROP TABLE IF EXISTS clean_weather;

CREATE TABLE clean_weather AS
SELECT
    time,
    temperature_2m,
    COALESCE(precipitation, 0) AS precipitation,
    wind_speed_10m
FROM stg_weather
WHERE time IS NOT NULL
  AND temperature_2m IS NOT NULL;


-- =====================================================
-- Optional Performance Indexes
-- These indexes support time-based analysis and joins.
-- =====================================================

CREATE INDEX IF NOT EXISTS idx_clean_weather_time
ON clean_weather(time);


-- =====================================================
-- Validation Queries
-- These queries are used to validate the transformation result.
-- =====================================================

-- Show all column names in stg_weather
SELECT column_name
FROM information_schema.columns
WHERE table_schema = 'public'
  AND table_name = 'stg_weather'
ORDER BY ordinal_position;

-- Compare row counts before and after cleaning
SELECT COUNT(*) AS stg_weather_rows
FROM stg_weather;

SELECT COUNT(*) AS clean_weather_rows
FROM clean_weather;


-- Check missing timestamps after cleaning
-- Expected result: 0 rows
SELECT *
FROM clean_weather
WHERE time IS NULL;


-- Check missing temperature values after cleaning
-- Expected result: 0 rows
SELECT *
FROM clean_weather
WHERE temperature_2m IS NULL;


-- Quick weather overview
SELECT
    MIN(time) AS min_time,
    MAX(time) AS max_time,
    ROUND(AVG(temperature_2m)::numeric, 2) AS avg_temperature,
    ROUND(AVG(precipitation)::numeric, 2) AS avg_precipitation,
    ROUND(AVG(wind_speed_10m)::numeric, 2) AS avg_wind_speed
FROM clean_weather;


-- Check whether PostgreSQL uses an index for time filtering
EXPLAIN ANALYZE
SELECT *
FROM clean_weather
WHERE time >= '2026-05-10 00:00:00';