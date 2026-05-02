import requests
import pandas as pd
import json
import os
from datetime import datetime

# ----------- Setup Paths -----------
RAW_PATH = "data/raw/charging"
PROCESSED_PATH = "data/processed/charging"

os.makedirs(RAW_PATH, exist_ok=True)
os.makedirs(PROCESSED_PATH, exist_ok=True)

# ----------- Timestamp -----------
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")

# ----------- API Request -----------
url = "https://api.openchargemap.io/v3/poi/"

params = {
    "countrycode": "DE",
    "maxresults": 50,
    "key": "eb97944a-7353-4416-a680-1b14f2a089f1"
}

response = requests.get(url, params=params, timeout=30)

# ----------- Check Status -----------
if response.status_code != 200:
    raise Exception(f"API request failed with status {response.status_code}")

data = response.json()

# ----------- Debug / Inspect JSON -----------
print("Type:", type(data))
print("Number of stations:", len(data))

if len(data) > 0:
    print("First station keys:", data[0].keys())

# ----------- Save RAW JSON -----------
raw_file = f"{RAW_PATH}/charging_{timestamp}.json"

with open(raw_file, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"Raw JSON saved at: {raw_file}")

# ----------- Parse Nested JSON -----------
records = []

for station in data:
    address = station.get("AddressInfo", {})
    connections = station.get("Connections", [])

    power_kw = None
    connection_type_id = None

    if connections:
        power_kw = connections[0].get("PowerKW")
        connection_type_id = connections[0].get("ConnectionTypeID")

    records.append({
        "station_id": station.get("ID"),
        "station_name": address.get("Title"),
        "city": address.get("Town"),
        "postcode": address.get("Postcode"),
        "latitude": address.get("Latitude"),
        "longitude": address.get("Longitude"),
        "number_of_points": station.get("NumberOfPoints"),
        "power_kw": power_kw,
        "connection_type_id": connection_type_id
    })

# ----------- Transform to DataFrame -----------
df = pd.DataFrame(records)

# ----------- Basic Cleaning -----------
df["latitude"] = pd.to_numeric(df["latitude"], errors="coerce")
df["longitude"] = pd.to_numeric(df["longitude"], errors="coerce")
df["power_kw"] = pd.to_numeric(df["power_kw"], errors="coerce")

# ----------- Debug / Validate DataFrame -----------
print(df.head())
print(df.columns)
print(df.shape)
print(df.isna().sum())

# ----------- Save Processed CSV -----------
processed_file = f"{PROCESSED_PATH}/charging_{timestamp}.csv"

df.to_csv(processed_file, index=False)

print(f"Processed CSV saved at: {processed_file}")