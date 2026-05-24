CREATE TABLE IF NOT EXISTS stg_weather (
    time TIMESTAMP,
    temperature_2m DOUBLE PRECISION,
    precipitation DOUBLE PRECISION,
    wind_speed_10m DOUBLE PRECISION
);

CREATE TABLE IF NOT EXISTS stg_charging_stations (
    station_id BIGINT,
    station_name TEXT,
    city TEXT,
    postcode TEXT,
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    number_of_points DOUBLE PRECISION,
    power_kw DOUBLE PRECISION,
    connection_type_id DOUBLE PRECISION
);

CREATE TABLE IF NOT EXISTS stg_vehicle_sessions (
    session_id TEXT,
    vehicle_id TEXT,
    vehicle_type TEXT,
    battery_capacity_kwh DOUBLE PRECISION,
    station_id BIGINT,
    city TEXT,
    power_kw DOUBLE PRECISION,
    battery_start_pct INTEGER,
    battery_end_pct INTEGER,
    battery_delta_pct INTEGER,
    energy_kwh DOUBLE PRECISION,
    cost_eur DOUBLE PRECISION,
    duration_minutes INTEGER,
    start_time TIMESTAMP,
    end_time TIMESTAMP
); 

