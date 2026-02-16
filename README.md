# NYC Yellow Taxi Data Explorer

A web dashboard to explore NYC taxi trip patterns. Built for the Urban Mobility Data summative assignment.

## Team

| Name | Role |
|------|------|
| Teniola Adam Olaleye | Team Lead, Database Design |
| Rajveer Singh Jolly | Data Cleaning |
| Michaella Kamikazi Karangwa | Algorithm Implementation |
| Kevin Manzi | Backend API |
| Gael Kamunuga Mparaye | Frontend |

## What it does

- Shows taxi trip statistics (total trips, avg fare, etc)
- Filter data by borough and hour of day
- Charts showing:
  - Trips by hour
  - Top pickup zones
  - Average fare throughout the day

## Tech Stack

- Backend: Python + Flask
- Database: SQLite
- Frontend: HTML, CSS, JavaScript
- Charts: Chart.js

## Project Structure

```
nyc-taxi-explorer/
├── backend/
│   ├── app.py              # Flask API
│   └── algorithms/
│       └── top_zones.py    # Manual sorting algorithm
├── frontend/
│   ├── index.html
│   ├── css/style.css
│   └── js/app.js
├── database/
│   └── schema.sql          # Table definitions
├── data_processing/
│   ├── data_cleaner.py     # Cleans raw data
│   └── load_to_database.py
└── data/
    ├── raw/                # Put original files here
    └── processed/
```

## Setup Instructions

### 1. Install Python stuff

```bash
# Make a virtual environment (optional but recommended)
python -m venv venv
venv\Scripts\activate   # Windows
# source venv/bin/activate  # Mac/Linux

# Install packages
pip install flask flask-cors pandas pyarrow
```

### 2. Add your data files

Put these in the `data/raw/` folder:
- yellow_tripdata_*.parquet
- taxi_zone_lookup.csv
- taxi_zones.geojson (optional)

### 3. Clean the data and setup database

```bash
python data_processing/data_cleaner.py
python data_processing/load_to_database.py
```

### 4. Start the backend

```bash
cd backend
python app.py
```

Server runs at http://localhost:5000

### 5. Open the frontend

Just open `frontend/index.html` in your browser.

Or run a simple server:
```bash
cd frontend
python -m http.server 8080
```
Then go to http://localhost:8080

## API Endpoints

| Endpoint | What it does |
|----------|--------------|
| GET /summary | Returns total trips, avg fare, etc |
| GET /trips?borough=X&hour=Y | Filtered trip data |
| GET /average-fare-by-hour | Avg fare for each hour |
| GET /top-zones?n=10 | Top N busiest pickup zones |

## Database

Two tables:
- **zones** - zone id, name, borough (from lookup csv)
- **trips** - all the trip data plus derived features

See `database/schema.sql` for details.

## Video Walkthrough

[Link will be added]

---

Built by Team NYC Taxi Explorer
