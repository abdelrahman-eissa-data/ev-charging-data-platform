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

