# 🚀 EV Charging Data Platform

## 📌 Project Overview

This project demonstrates an end-to-end **Data Engineering pipeline** that collects, processes, and prepares data from multiple sources in the Electric Vehicle (EV) domain.

The goal is to simulate a real-world data workflow, starting from data extraction to transformation, and preparing the data for analytics and visualization.

---

## ⚙️ Architecture

```
APIs (Weather & Charging)
        ↓
Extract (Python scripts)
        ↓
Raw Data (JSON - Data Lake Layer)
        ↓
Transform (Pandas)
        ↓
Processed Data (CSV)
        ↓
(Next: Database + Visualization + Automation)
```

---

## 🔗 Data Sources

* 🌦️ Weather API (Open-Meteo)
* ⚡ EV Charging Stations API (OpenChargeMap)
* 🚗 (Planned) Simulated Vehicle Data

---

## 🛠️ Tech Stack

* Python (requests, pandas)
* REST APIs (JSON)
* Git & GitHub (Version Control)
* Data Pipeline Design

---

## 📂 Project Structure

```
ev-charging-data-platform/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── src/
│   ├── extract/
│   ├── transform/
│   └── load/
│
├── notebooks/
│
├── README.md
└── .gitignore
```

---

## 🔄 What I Implemented

* Extracted data from multiple APIs using Python
* Stored raw data (JSON) for traceability (Data Lake approach)
* Transformed data into structured format using Pandas
* Saved processed data for further analysis
* Structured the project using a clean Data Engineering architecture
* Applied Git best practices (excluding data using `.gitignore`)

---

## 🚧 Next Steps

* Add simulated vehicle data (streaming-like data)
* Load data into PostgreSQL or SQLite
* Build a data model (Data Warehouse)
* Create a Power BI dashboard for insights
* Automate the pipeline using workflow tools (Airflow / n8n)

---

## 🎯 Key Learnings

* Understanding API data structures (JSON, nested data)
* Designing scalable data pipelines
* Separating raw and processed data layers
* Using Git professionally in data projects
* Transitioning from Data Analysis to Data Engineering

---

## 👤 Author

**Abdelrahman Eissa**
Aspiring Data Engineer
