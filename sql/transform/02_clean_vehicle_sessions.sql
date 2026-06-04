-- =====================================================
-- Clean Vehicle Sessions
-- Project: EV Charging Data Platform
-- Layer: Transform
-- Source: stg_vehicle_sessions
-- Target: clean_vehicle_sessions
-- =====================================================

DROP TABLE IF EXISTS clean_vehicle_sessions;

CREATE TABLE clean_vehicle_sessions AS
SELECT
    session_id,
    vehicle_id,
    vehicle_type,
    battery_capacity_kwh,
    station_id,
    city,
    power_kw,
    battery_start_pct,
    battery_end_pct,
    battery_delta_pct,
    energy_kwh,
    cost_eur,
    duration_minutes,
    start_time,
    end_time
FROM stg_vehicle_sessions
WHERE session_id IS NOT NULL
  AND vehicle_id IS NOT NULL
  AND station_id IS NOT NULL
  AND energy_kwh IS NOT NULL
  AND energy_kwh > 0
  AND duration_minutes IS NOT NULL
  AND duration_minutes > 0
  AND battery_start_pct IS NOT NULL
  AND battery_end_pct IS NOT NULL
  AND battery_delta_pct IS NOT NULL
  AND battery_start_pct >= 0
  AND battery_end_pct <= 100
  AND battery_end_pct > battery_start_pct
  AND cost_eur IS NOT NULL
  AND cost_eur >= 0;


-- =====================================================
-- Optional Performance Indexes
-- These indexes support joins and time-based analysis.
-- =====================================================

CREATE INDEX IF NOT EXISTS idx_clean_vehicle_sessions_session_id
ON clean_vehicle_sessions(session_id);

CREATE INDEX IF NOT EXISTS idx_clean_vehicle_sessions_vehicle_id
ON clean_vehicle_sessions(vehicle_id);

CREATE INDEX IF NOT EXISTS idx_clean_vehicle_sessions_station_id
ON clean_vehicle_sessions(station_id);

CREATE INDEX IF NOT EXISTS idx_clean_vehicle_sessions_start_time
ON clean_vehicle_sessions(start_time);


-- =====================================================
-- Validation Queries
-- These queries are used to validate the transformation result.
-- =====================================================

-- Show all column names in stg_vehicle_sessions
SELECT column_name
FROM information_schema.columns
WHERE table_schema = 'public'
  AND table_name = 'stg_vehicle_sessions'
ORDER BY ordinal_position;


-- Compare row counts before and after cleaning
SELECT COUNT(*) AS stg_vehicle_sessions_rows
FROM stg_vehicle_sessions;

SELECT COUNT(*) AS clean_vehicle_sessions_rows
FROM clean_vehicle_sessions;


-- Check invalid records after cleaning
-- Expected result: 0 rows
SELECT *
FROM clean_vehicle_sessions
WHERE energy_kwh IS NULL
   OR energy_kwh <= 0
   OR duration_minutes IS NULL
   OR duration_minutes <= 0
   OR battery_end_pct <= battery_start_pct;


-- Check whether PostgreSQL uses an index for station_id filtering
EXPLAIN ANALYZE
SELECT *
FROM clean_vehicle_sessions
WHERE station_id = 487807;