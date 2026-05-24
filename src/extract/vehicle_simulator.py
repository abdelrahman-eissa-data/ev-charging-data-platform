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

for i in range(100):

    station = random.choice(stations)
    vehicle = random.choice(fleet)

    battery_capacity = vehicle["battery_capacity"]

    battery_start = random.randint(10, 40)
    battery_end = random.randint(battery_start + 20, 95)

    battery_delta_pct = battery_end - battery_start
    energy_kwh = round((battery_capacity * battery_delta_pct) / 100, 2)

    PRICE_PER_KWH = 0.45
    cost_eur = round(energy_kwh * PRICE_PER_KWH, 2)

    duration_minutes = round((energy_kwh / station["power_kw"]) * 60)

    start_time = datetime.now().replace(microsecond=0) - timedelta(
        days=random.randint(0, 30),
        hours=random.randint(0, 23),
        minutes=random.randint(0, 59)
    )

    end_time = start_time + timedelta(minutes=duration_minutes)

    session = {
        "session_id": f"S_{i+1:04d}",
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

# ----------- Save RAW JSON -----------
raw_file = os.path.join(RAW_PATH, f"vehicle_sessions_{timestamp}.json")

with open(raw_file, "w", encoding="utf-8") as f:
    json.dump(sessions, f, indent=2, default=str, ensure_ascii=False)

print(f"JSON saved: {raw_file}")

# ----------- Save Processed CSV -----------
processed_file = os.path.join(PROCESSED_PATH, f"vehicle_sessions_{timestamp}.csv")

df.to_csv(processed_file, index=False)

print(f"CSV saved: {processed_file}")
