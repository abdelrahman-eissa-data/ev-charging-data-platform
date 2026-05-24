import os
from dotenv import load_dotenv
import pandas as pd
from sqlalchemy import create_engine 

load_dotenv()

# ----------- Database Connection -----------

DB_USER = "postgres"
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "ev_charging_db"

engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# ----------- Helper Function: Get Latest CSV -----------

def get_latest_csv(folder_path):
    
    """
    Get the latest CSV file from a folder based on filename sorting.
    """

    if not os.path.exists(folder_path):
        raise FileNotFoundError(f"Folder not found: {folder_path}")

    files = []

    for file in os.listdir(folder_path):
        if file.endswith(".csv"):
            files.append(file)

    if not files:
        raise FileNotFoundError(f"No CSV files found in folder: {folder_path}")

    latest_file = sorted(files)[-1]

    return os.path.join(folder_path, latest_file)

# ----------- Helper Function: Load CSV to PostgreSQL -----------

def load_csv_to_table(csv_path, table_name):
    
    """
    Load a CSV file into a PostgreSQL table.
    """

    print(f"Loading file: {csv_path}")
    print(f"Target table: {table_name}")

    df = pd.read_csv(csv_path)

    df.to_sql(
        table_name,
        engine,
        if_exists="replace",
        index=False
    )

    print(f"Loaded {len(df)} rows into {table_name}")

# ----------- Get Latest Processed Files -----------

weather_csv = get_latest_csv("data/processed/weather")
charging_csv = get_latest_csv("data/processed/charging")
vehicle_csv = get_latest_csv("data/processed/vehicle")

# ----------- Load Data into PostgreSQL Staging Tables -----------

load_csv_to_table(weather_csv, "stg_weather")
load_csv_to_table(charging_csv, "stg_charging_stations")
load_csv_to_table(vehicle_csv, "stg_vehicle_sessions")

print("All processed CSV files loaded successfully into PostgreSQL.")
