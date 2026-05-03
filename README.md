# 🚀 EV Charging Data Platform

## 📌 Project Overview

This project demonstrates a **Data Engineering pipeline** that collects, processes, and prepares data from multiple sources in the EV (Electric Vehicle) domain.

The goal is to simulate a real-world data workflow, starting from data extraction to transformation and preparing the data for analytics and visualization.

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
* REST APIs (JSON data)
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
* Build data model (Data Warehouse)
* Create Power BI dashboard for insights
* Automate pipeline using workflow tools (Airflow / n8n)

---

## 🎯 Key Learnings

* Understanding API data structures (JSON, nested data)
* Designing a scalable data pipeline
* Separating raw and processed data
* Using Git professionally in data projects
* Moving from Data Analysis to Data Engineering mindset

---

## 👤 Author

Abdelrahman Eissa
Aspiring Data Engineer
