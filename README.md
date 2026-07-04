# EV Charging Data Platform

## Project Overview

This project is a Data Engineering portfolio project focused on building an end-to-end EV Charging Data Platform.

The project follows an ELT approach:

```text
Extract → Load → Transform
```

Python is used for data extraction, API integration, data simulation, and loading data into PostgreSQL.
SQL is used for data validation, cleaning, transformation, and Data Warehouse modeling inside PostgreSQL.

The goal of this project is to demonstrate practical Data Engineering skills, including API extraction, raw and processed data layers, PostgreSQL staging tables, SQL transformations, data quality checks, PostgreSQL Data Warehouse modeling, Star Schema design, Git/GitHub workflow, and later dbt, Power BI, automation, Docker/Linux, and AWS.

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
✅ Scaled vehicle charging simulation for analytics reporting
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
✅ PostgreSQL Data Warehouse modeling
✅ Data Mart / Star Schema modeling
✅ Dimension tables
✅ Fact table
✅ Primary key and foreign key relationships
✅ Data Mart validation queries
✅ PostgreSQL ERD generated
```

Next steps:

```text
⬜ Power BI dashboard
⬜ dbt implementation
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

The weather dataset includes:

```text
time
temperature_2m
precipitation
wind_speed_10m
```

---

### EV Charging Stations API

Charging station data is extracted from the OpenChargeMap API and stored as:

```text
data/raw/charging/        → JSON
data/processed/charging/  → CSV
```

Sensitive API keys are stored in `.env` and are not committed to GitHub.

The charging station dataset includes:

```text
station_id
station_name
city
postcode
latitude
longitude
number_of_points
power_kw
connection_type_id
```

---

### Simulated Vehicle Charging Sessions

Vehicle charging session data is generated using Python.

The simulation is based on real charging station data and includes a scalable number of charging sessions for analytics reporting.

The simulated vehicle charging sessions include:

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
├── docs/
│   └── images/
│       └── postgresql_dwh_erd.png
│
├── notebooks/
│   ├── charging/
│   ├── vehicle_simulator/
│   └── weather/
│
├── src/
│   ├── extract/
│   │   ├── charging_api.py
│   │   ├── vehicle_simulator.py
│   │   └── weather_api.py
│   │
│   └── load/
│       └── load_to_postgres.py
│
├── sql/
│   ├── staging/
│   │   ├── 01_create_staging_tables.sql
│   │   └── 02_data_quality_checks.sql
│   │
│   ├── transform/
│   │   ├── 01_clean_charging_stations.sql
│   │   ├── 02_clean_vehicle_sessions.sql
│   │   └── 03_clean_weather.sql
│   │
│   └── marts/
│       ├── 01_dim_station.sql
│       ├── 02_dim_vehicle.sql
│       ├── 03_dim_date.sql
│       ├── 04_fact_charging_sessions.sql
│       └── 05_validate_data_mart.sql
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
Vehicle charging session simulation
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

The staging layer keeps the data close to the source structure and is used for initial validation and quality checks.

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

## PostgreSQL Data Warehouse Modeling

The project includes a PostgreSQL-based Data Warehouse structure with multiple layers designed for a production-oriented analytics workflow.

The Data Warehouse is organized into three main layers:

```text
Staging Layer
      ↓
Clean / Transformation Layer
      ↓
Data Mart / Star Schema Layer
```

---

### 1. Staging Layer

The staging layer stores loaded data from APIs and simulated charging sessions with a structure close to the original source data.

Current staging tables:

```text
stg_weather
stg_charging_stations
stg_vehicle_sessions
```

This layer is used for initial data quality checks and validation before applying transformations.

---

### 2. Clean / Transformation Layer

The clean layer applies SQL-based cleaning rules and validation logic.

Current clean tables:

```text
clean_weather
clean_charging_stations
clean_vehicle_sessions
```

This layer removes invalid records, standardizes the data, and prepares reliable datasets for analytical modeling.

---

### 3. Data Mart / Star Schema Layer

The final Data Mart is designed as a Star Schema for Power BI reporting.

Final Data Mart tables:

| Table                    | Type            | Description                                                                                                                    |
| ------------------------ | --------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| `fact_charging_sessions` | Fact Table      | Contains charging session events and measurable metrics such as energy, cost, duration, battery percentage, and charging power |
| `dim_station`            | Dimension Table | Contains charging station attributes such as station name, city, location, number of charging points, and power                |
| `dim_vehicle`            | Dimension Table | Contains vehicle master data such as vehicle ID, vehicle type, and battery capacity                                            |
| `dim_date`               | Dimension Table | Contains a complete calendar table for time-based analysis and Power BI time intelligence                                      |

---

### Star Schema Relationships

The fact table is connected to the dimension tables through primary key and foreign key relationships:

```text
fact_charging_sessions.vehicle_id     → dim_vehicle.vehicle_id
fact_charging_sessions.station_id     → dim_station.station_id
fact_charging_sessions.start_date_id  → dim_date.date_id
fact_charging_sessions.end_date_id    → dim_date.date_id
```

This structure supports efficient analytical queries and enables interactive reporting in Power BI.

---

### Data Mart Validation

A dedicated validation script is included:

```text
sql/marts/05_validate_data_mart.sql
```

The validation checks include:

```text
row counts for fact and dimension tables
referential integrity between fact and dimensions
missing vehicle relationships
missing station relationships
missing start date relationships
missing end date relationships
invalid measure values
calendar continuity checks
business summary metrics
```

Expected validation results for relationship and data quality checks are `0`.

---

### PostgreSQL Data Warehouse ERD

The following ERD documents the PostgreSQL Data Warehouse structure of the project.

It shows the complete database model, including:

```text
Staging Layer:
stg_weather
stg_charging_stations
stg_vehicle_sessions

Clean / Transformation Layer:
clean_weather
clean_charging_stations
clean_vehicle_sessions

Data Mart / Star Schema Layer:
dim_station
dim_vehicle
dim_date
fact_charging_sessions
```

The final reporting model for Power BI is based only on the Star Schema tables:

```text
dim_station
dim_vehicle
dim_date
fact_charging_sessions
```

![PostgreSQL Data Warehouse ERD](docs/images/postgresql_dwh_erd.png)

This ERD shows the full PostgreSQL Data Warehouse structure, while Power BI will only use the final Data Mart tables for reporting.

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
Power BI
dbt
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
Scaled simulation dataset for analytics reporting
ELT pipeline design
PostgreSQL staging tables
Automated loading with Python
Environment variable management
Data quality checks
SQL transformations
Indexing for joins and filters
PostgreSQL Data Warehouse modeling
Staging, clean, and mart layers
Star Schema modeling
Fact and dimension tables
Primary key and foreign key relationships
Referential integrity validation
Data Mart validation queries
Power BI-ready semantic model preparation
Git/GitHub workflow
Reproducible project structure
```

---

## Next Development Steps

### 1. Power BI Dashboard

Build a Power BI dashboard using the final Data Mart tables:

```text
dim_station
dim_vehicle
dim_date
fact_charging_sessions
```

Possible KPIs:

```text
total charging sessions
total energy charged
total charging cost
average charging duration
average charging power
sessions by city
energy by vehicle type
charging duration by station power
weekend vs weekday charging behavior
monthly charging trend
```

---

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
automated testing
documentation
lineage
```

---

### 3. Automation

Automate the full pipeline:

```text
extract data
generate vehicle sessions
load to PostgreSQL
run transformations
run data mart validation
refresh reporting layer
```

---

### 4. Docker / Linux / AWS

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
