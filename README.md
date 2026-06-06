# EV Charging Data Platform

## Project Overview

This project is a Data Engineering portfolio project focused on building an end-to-end EV Charging Data Platform.

The project follows an ELT approach:

```text
Extract → Load → Transform
```

Python is used for data extraction, API integration, data simulation, and loading data into PostgreSQL.
SQL is used for data validation, cleaning, and transformation inside PostgreSQL.

The goal of this project is to demonstrate practical Data Engineering skills, including API extraction, raw and processed data layers, PostgreSQL staging tables, SQL transformations, data quality checks, Git/GitHub workflow, and later Data Warehouse modeling, dbt, Power BI, automation, Docker/Linux, and AWS.

---

## Current Project Status

This project is currently in progress.

Completed so far:

```text
✅ Project structure
✅ Git and GitHub version control
✅ Weather API extraction
✅ EV Charging Stations API extraction
✅ Simulated vehicle charging sessions
✅ Raw JSON storage
✅ Processed CSV storage
✅ PostgreSQL database setup
✅ PostgreSQL staging tables
✅ Python load script to PostgreSQL
✅ Environment variable configuration with .env
✅ SQL data quality checks
✅ SQL transform layer
✅ Clean charging stations table
✅ Clean vehicle sessions table
✅ Clean weather table
```

Next steps:

```text
⬜ Data Mart / Star Schema modeling
⬜ Dimension tables
⬜ Fact table
⬜ dbt implementation
⬜ Power BI dashboard
⬜ Pipeline automation
⬜ Docker / Linux workflow
⬜ AWS version with S3 and RDS
```

---

## Architecture

```text
Weather API
Charging Stations API
Vehicle Simulation
        ↓
Python Extract Layer
        ↓
Raw JSON + Processed CSV
        ↓
Python Load Layer
        ↓
PostgreSQL Staging Tables
        ↓
SQL Data Quality Checks
        ↓
SQL Transform Layer
        ↓
Clean Tables
        ↓
Data Mart / Star Schema
        ↓
Power BI Dashboard
```

---

## Data Sources

### Weather API

Weather data is extracted from an open weather API and stored as:

```text
data/raw/weather/        → JSON
data/processed/weather/  → CSV
```

### EV Charging Stations API

Charging station data is extracted from OpenChargeMap API and stored as:

```text
data/raw/charging/        → JSON
data/processed/charging/  → CSV
```

Sensitive API keys are stored in `.env` and are not committed to GitHub.

### Simulated Vehicle Charging Sessions

Vehicle charging session data is generated using Python.
The simulation is based on real charging station data and includes:

```text
session_id
vehicle_id
vehicle_type
battery_capacity_kwh
station_id
city
power_kw
battery_start_pct
battery_end_pct
battery_delta_pct
energy_kwh
cost_eur
duration_minutes
start_time
end_time
```

The simulated data is stored as:

```text
data/raw/vehicle/        → JSON
data/processed/vehicle/  → CSV
```

---

## Project Structure

```text
EV_data-engineering-project/
│
├── data/
│   ├── raw/
│   │   ├── charging/
│   │   ├── vehicle/
│   │   └── weather/
│   │
│   └── processed/
│       ├── charging/
│       ├── vehicle/
│       └── weather/
│
├── notebooks/
│   ├── charging/
│   ├── vehicle_simulator/
│   └── weather/
│
├── src/
│   ├── extract/
│   └── load/
│
├── sql/
│   ├── staging/
│   └── transform/
│
├── README.md
├── requirements.txt
└── .gitignore
```

---

## ELT Workflow

### 1. Extract Layer

Python scripts extract data from APIs and generate simulated vehicle charging sessions.

```text
src/extract/
```

This layer is responsible for:

```text
API requests
JSON parsing
DataFrame creation
Raw JSON export
Processed CSV export
Timestamped file creation
```

---

### 2. Load Layer

The load script reads the latest processed CSV files and loads them into PostgreSQL staging tables.

```text
src/load/load_to_postgres.py
```

The script loads data into:

```text
stg_weather
stg_charging_stations
stg_vehicle_sessions
```

Database credentials are managed through environment variables.

---

### 3. Staging Layer

SQL scripts for PostgreSQL staging tables are stored in:

```text
sql/staging/
```

The staging layer contains data after loading, before final cleaning and transformation.

Current staging tables:

```text
stg_weather
stg_charging_stations
stg_vehicle_sessions
```

---

### 4. Data Quality Checks

SQL validation queries are used to check:

```text
row counts
missing IDs
invalid power_kw values
invalid energy_kwh values
invalid duration values
battery percentage logic
sessions without matching station
```

Example:

```sql
SELECT COUNT(*)
FROM stg_charging_stations
WHERE power_kw IS NULL
   OR power_kw <= 0;
```

---

### 5. SQL Transform Layer

SQL transformations are stored in:

```text
sql/transform/
```

Current clean tables:

```text
clean_charging_stations
clean_vehicle_sessions
clean_weather
```

These tables are created from staging tables after applying cleaning rules and validation logic.

Example transformation:

```sql
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
```

Indexes are added for common joins and filters, for example:

```sql
CREATE INDEX IF NOT EXISTS idx_clean_charging_stations_station_id
ON clean_charging_stations(station_id);
```

---

## Technologies Used

```text
Python
Pandas
Requests
SQLAlchemy
python-dotenv
PostgreSQL
pgAdmin
SQL
Git
GitHub
Jupyter Notebook
```

Planned technologies:

```text
dbt
Power BI
Docker
Linux
AWS S3
AWS RDS PostgreSQL
Automation tools
```

---

## Data Engineering Concepts Demonstrated

This project demonstrates:

```text
API data extraction
Raw and processed data layers
JSON and CSV handling
Vehicle charging simulation
ELT pipeline design
PostgreSQL staging tables
Automated loading with Python
Environment variable management
Data quality checks
SQL transformations
Indexing for joins and filters
Git/GitHub workflow
Reproducible project structure
```

---

## Next Development Steps

### 1. Data Mart / Star Schema

Create analytical tables for reporting:

```text
dim_station
dim_vehicle
dim_date
fact_charging_sessions
```

### 2. dbt

Migrate SQL transformation logic into dbt models:

```text
models/staging/
models/intermediate/
models/marts/
```

dbt will be used for:

```text
modular SQL transformations
testing
documentation
lineage
```

### 3. Power BI

Build a Power BI dashboard using the final Data Mart tables.

Possible KPIs:

```text
total charging sessions
total energy charged
total charging cost
average charging duration
sessions by city
energy by vehicle type
charging duration by station power
weather impact on charging behavior
```

### 4. Automation

Automate the full pipeline:

```text
extract data
generate vehicle sessions
load to PostgreSQL
run transformations
refresh reporting layer
```

### 5. Docker / Linux / AWS

Later improvements:

```text
Dockerize PostgreSQL and the pipeline
Practice Linux shell workflow
Store raw/processed data in AWS S3
Use AWS RDS PostgreSQL as cloud database
```

---

## Author

Abdelrahman Eissa

Aspiring Data Engineer / Analytics Engineer with a background in Automotive Software Testing, Data Analytics, SQL, Python, PostgreSQL, and Power BI.
