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


# --------Echte Stationen laden ----------
charging_path = "data/processed/charging"
files = os.listdir(charging_path)
latest_file = sorted(files)[-1]

df_charging = pd.read_csv(f"{charging_path}/{latest_file}")

stations = df_charging[["station_id", "city", "power_kw"]].dropna().to_dict("records")


# -----------Sessions Loop--------------
sessions = []

for i in range(100):
   
    station = random.choice(stations)
    
    battery_start = random.randint(10, 40)
    battery_end = random.randint(battery_start + 20, 95)
    energy_kwh = (75 * (battery_end - battery_start)) / 100
    duration_minutes = round((energy_kwh / station["power_kw"]) * 60)
    
    start_time = datetime.now().replace(microsecond=0) - timedelta(
        days=random.randint(0, 30),
        hours=random.randint(0, 23),
        minutes=random.randint(0, 59)
    )
    end_time = start_time + timedelta(minutes=duration_minutes)

    session = {
        "vehicle_id":        f"EV_{i+1:03d}",
        "station_id":        station["station_id"],
        "city":              station["city"],
        "power_kw":          station["power_kw"],
        "battery_start_pct": battery_start,
        "battery_end_pct":   battery_end,
        "energy_kwh":        energy_kwh,
        "duration_minutes":  duration_minutes,
        "start_time":        start_time,
        "end_time":          end_time,
    }
    sessions.append(session)
df = pd.DataFrame(sessions)

# ----------- Save RAW JSON -----------
raw_file = f"{RAW_PATH}/vehicle_sessions_{timestamp}.json"
with open(raw_file, "w") as f:
    json.dump(sessions, f, indent=2, default=str)

print(f"JSON saved: {raw_file}")

# ----------- Save Processed CSV -----------
processed_file = f"{PROCESSED_PATH}/vehicle_sessions_{timestamp}.csv"
df.to_csv(processed_file, index=False)

print(f"CSV saved: {processed_file}")