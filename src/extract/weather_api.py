import requests
import pandas as pd
import json
import os
from datetime import datetime

# ----------- Setup Paths -----------
RAW_PATH = "data/raw/weather"
PROCESSED_PATH = "data/processed/weather"

os.makedirs(RAW_PATH, exist_ok=True)
os.makedirs(PROCESSED_PATH, exist_ok=True)

# ----------- Timestamp -----------
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")

# ----------- API Request -----------
url = "https://api.open-meteo.com/v1/forecast"

params = {
    "latitude": 52.52,
    "longitude": 13.41,
    "hourly": "temperature_2m,precipitation,wind_speed_10m"
}

response = requests.get(url, params=params)

# check status
if response.status_code != 200:
    raise Exception(f"API request failed with status {response.status_code}")

data = response.json()

# ----------- Debug -----------
print("Type:", type(data))
print("Top keys:", data.keys())
print("Hourly keys:", data["hourly"].keys())

# ----------- Save RAW JSON -----------
raw_file = f"{RAW_PATH}/weather_{timestamp}.json"

with open(raw_file, "w") as f:
    json.dump(data, f, indent=2)

print(f"Raw JSON saved at: {raw_file}")

# ----------- Transform to DataFrame -----------
hourly_data = data["hourly"]

df = pd.DataFrame(hourly_data)
print(df.head())
# ----------- Basic Cleaning -----------
df["time"] = pd.to_datetime(df["time"])

# ----------- Save Processed CSV -----------
processed_file = f"{PROCESSED_PATH}/weather_{timestamp}.csv"

df.to_csv(processed_file, index=False)

print(f"Processed CSV saved at: {processed_file}")