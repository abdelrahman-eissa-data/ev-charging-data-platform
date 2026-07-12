import random
from datetime import datetime, timedelta
import json
import pandas as pd
import os

# ----------- Setup Paths -----------
RAW_PATH = "data/raw/vehicle"
PROCESSED_PATH = "data/processed/vehicle"

os.makedirs(RAW_PATH, exist_ok=True)
os.makedirs(PROCESSED_PATH, exist_ok=True)

# ----------- Timestamp -----------
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")

# ----------- Load Latest Charging Data -----------
charging_path = "data/processed/charging"

# Check if charging folder exists
if not os.path.exists(charging_path):
    raise FileNotFoundError(f"Charging folder not found: {charging_path}")

# Get only CSV files
files = []

for file in os.listdir(charging_path):
    if file.endswith(".csv"):
        files.append(file)

# Check if CSV files exist
if not files:
    raise FileNotFoundError("No charging CSV files found. Please run charging_api.py first.")

# Select latest charging CSV file
latest_file = sorted(files)[-1]

# Build full file path
charging_file_path = os.path.join(charging_path, latest_file)

# Read charging CSV
df_charging = pd.read_csv(charging_file_path)

print(f"Loaded charging file: {charging_file_path}")

# ----------- Validate Charging Data -----------
required_columns = ["station_id", "city", "power_kw"]

for column in required_columns:
    if column not in df_charging.columns:
        raise ValueError(f"Missing required column in charging data: {column}")

# Convert power_kw to numeric
df_charging["power_kw"] = pd.to_numeric(df_charging["power_kw"], errors="coerce")

# Remove invalid rows
df_charging = df_charging.dropna(subset=["station_id", "city", "power_kw"])
df_charging = df_charging[df_charging["power_kw"] > 0]

# Convert charging stations to list of dictionaries
stations = df_charging[["station_id", "city", "power_kw"]].to_dict("records")

if not stations:
    raise ValueError("No valid charging stations found after cleaning.")

print(f"Number of valid charging stations: {len(stations)}")

# ----------- Vehicle Master Data -----------
vehicle_models = [
    {"type": "Tesla Model 3", "battery_capacity": 75},
    {"type": "VW ID.4", "battery_capacity": 82},
    {"type": "BMW iX3", "battery_capacity": 74},
    {"type": "Renault Zoe", "battery_capacity": 52},
]

fleet = []

for i in range(25):
    model = random.choice(vehicle_models)

    fleet.append({
        "vehicle_id": f"EV_{i+1:03d}",
        "vehicle_type": model["type"],
        "battery_capacity": model["battery_capacity"]
    })

# ----------- Generate Vehicle Charging Sessions -----------
sessions = []

# Fixed analysis period for stable Power BI reporting
NUMBER_OF_SESSIONS = 20000
START_DATE = datetime(2025, 1, 1)
END_DATE = datetime(2026, 6, 30, 23, 59, 59)

total_seconds = int((END_DATE - START_DATE).total_seconds())

PRICE_PER_KWH = 0.45

for i in range(NUMBER_OF_SESSIONS):

    station = random.choice(stations)
    vehicle = random.choice(fleet)

    battery_capacity = vehicle["battery_capacity"]

    # Generate random start time within fixed analysis period
    random_seconds = random.randint(0, total_seconds)
    start_time = START_DATE + timedelta(seconds=random_seconds)
    start_time = start_time.replace(microsecond=0)

    # Date-based simulation logic
    month = start_time.month
    is_weekend = start_time.weekday() >= 5

    # Seasonal behavior:
    # Winter months have slightly higher energy demand
    if month in [11, 12, 1, 2]:
        season_multiplier = random.uniform(1.10, 1.25)

    # Summer months are more stable / slightly lower
    elif month in [6, 7, 8]:
        season_multiplier = random.uniform(0.95, 1.05)

    # Spring and autumn
    else:
        season_multiplier = random.uniform(1.00, 1.10)

    # Weekend charging behavior
    if is_weekend:
        weekday_multiplier = random.uniform(1.05, 1.20)
    else:
        weekday_multiplier = random.uniform(0.90, 1.05)

    battery_start = random.randint(10, 40)
    battery_end = random.randint(battery_start + 20, 95)

    battery_delta_pct = battery_end - battery_start

    # Base energy calculation
    energy_kwh = (battery_capacity * battery_delta_pct) / 100

    # Apply realistic behavioral multipliers
    energy_kwh = energy_kwh * season_multiplier * weekday_multiplier
    energy_kwh = round(energy_kwh, 2)

    cost_eur = round(energy_kwh * PRICE_PER_KWH, 2)

    duration_minutes = round((energy_kwh / station["power_kw"]) * 60)

    # Avoid zero-minute sessions if power_kw is very high
    duration_minutes = max(duration_minutes, 1)

    end_time = start_time + timedelta(minutes=duration_minutes)

    session = {
        "session_id": f"S_{i+1:05d}",
        "vehicle_id": vehicle["vehicle_id"],
        "vehicle_type": vehicle["vehicle_type"],
        "battery_capacity_kwh": vehicle["battery_capacity"],
        "station_id": station["station_id"],
        "city": station["city"],
        "power_kw": station["power_kw"],
        "battery_start_pct": battery_start,
        "battery_end_pct": battery_end,
        "battery_delta_pct": battery_delta_pct,
        "energy_kwh": energy_kwh,
        "cost_eur": cost_eur,
        "duration_minutes": duration_minutes,
        "start_time": start_time,
        "end_time": end_time,
    }

    sessions.append(session)

# ----------- Convert to DataFrame -----------
df = pd.DataFrame(sessions)

# ----------- Basic Validation -----------
print(df.head())
print(df.columns)
print(df.shape)

print("Vehicle session simulation completed successfully.")
print(f"Rows generated: {len(df)}")
print(f"Date range: {df['start_time'].min()} to {df['start_time'].max()}")
print(f"Number of vehicles: {df['vehicle_id'].nunique()}")
print(f"Number of stations used: {df['station_id'].nunique()}")
print(f"Number of cities: {df['city'].nunique()}")

# ----------- Save RAW JSON -----------
raw_file = os.path.join(RAW_PATH, f"vehicle_sessions_{timestamp}.json")

with open(raw_file, "w", encoding="utf-8") as f:
    json.dump(sessions, f, indent=2, default=str, ensure_ascii=False)

print(f"JSON saved: {raw_file}")

# ----------- Save Processed CSV -----------
processed_file = os.path.join(PROCESSED_PATH, f"vehicle_sessions_{timestamp}.csv")

df.to_csv(processed_file, index=False)

print(f"CSV saved: {processed_file}")
