- =====================================================
-- Data Quality Checks for Staging Tables
-- Project: EV Charging Data Platform
-- Layer: PostgreSQL Staging
-- =====================================================


-- 1) Check row counts in all staging tables

SELECT COUNT(*) AS weather_rows
FROM stg_weather;

SELECT COUNT(*) AS charging_station_rows
FROM stg_charging_stations;

SELECT COUNT(*) AS vehicle_session_rows
FROM stg_vehicle_sessions;


-- 2) Check invalid charging station power values

SELECT COUNT(*) AS invalid_power_rows
FROM stg_charging_stations
WHERE power_kw IS NULL
   OR power_kw <= 0;


-- 3) Show invalid charging station records

SELECT *
FROM stg_charging_stations
WHERE power_kw IS NULL
   OR power_kw <= 0;


-- 4) Check missing station_id in charging stations

SELECT COUNT(*) AS missing_station_id_rows
FROM stg_charging_stations
WHERE station_id IS NULL;


-- 5) Check missing session_id in vehicle sessions

SELECT COUNT(*) AS missing_session_id_rows
FROM stg_vehicle_sessions
WHERE session_id IS NULL;


-- 6) Check invalid energy values in vehicle sessions

SELECT COUNT(*) AS invalid_energy_rows
FROM stg_vehicle_sessions
WHERE energy_kwh IS NULL
   OR energy_kwh <= 0;


-- 7) Check invalid charging duration values

SELECT COUNT(*) AS invalid_duration_rows
FROM stg_vehicle_sessions
WHERE duration_minutes IS NULL
   OR duration_minutes <= 0;


-- 8) Check invalid battery percentage logic

SELECT COUNT(*) AS invalid_battery_rows
FROM stg_vehicle_sessions
WHERE battery_start_pct IS NULL
   OR battery_end_pct IS NULL
   OR battery_delta_pct IS NULL
   OR battery_start_pct < 0
   OR battery_end_pct > 100
   OR battery_end_pct <= battery_start_pct;


-- 9) Check invalid cost values

SELECT COUNT(*) AS invalid_cost_rows
FROM stg_vehicle_sessions
WHERE cost_eur IS NULL
   OR cost_eur < 0;


-- 10) Check vehicle sessions without matching charging station

SELECT COUNT(*) AS sessions_without_matching_station
FROM stg_vehicle_sessions v
LEFT JOIN stg_charging_stations c
    ON v.station_id = c.station_id
WHERE c.station_id IS NULL;


-- 11) Check weather timestamp null values

SELECT COUNT(*) AS missing_weather_time_rows
FROM stg_weather
WHERE time IS NULL;


-- 12) Quick overview of vehicle sessions

SELECT
    COUNT(*) AS total_sessions,
    COUNT(DISTINCT vehicle_id) AS unique_vehicles,
    COUNT(DISTINCT station_id) AS used_stations,
    ROUND(SUM(energy_kwh)::numeric, 2) AS total_energy_kwh,
    ROUND(SUM(cost_eur)::numeric, 2) AS total_cost_eur,
    ROUND(AVG(duration_minutes)::numeric, 2) AS avg_duration_minutes
FROM stg_vehicle_sessions;