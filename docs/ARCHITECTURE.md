# System Architecture
**By Teniola Adam Olaleye**

## What is this project?

We built a web app that shows NYC taxi data. Users can see charts, filter by borough and time, and understand taxi patterns in the city.

## How the system works

Our app has 3 main parts that talk to each other:

```
[User's Browser]  <-->  [Flask Server]  <-->  [SQLite Database]
   (Frontend)            (Backend)            (Data Storage)
```

### The Frontend (Gael's part)
- HTML page that users see
- CSS for making it look nice (yellow taxi theme)
- JavaScript that fetches data and shows charts

When someone clicks a filter, JavaScript sends a request to our Flask server.

### The Backend (Kevin's part)
- Flask app running on localhost:5000
- Has 4 API endpoints:
  - /summary - gives overall stats
  - /trips - returns trip data (can filter by borough/hour)
  - /average-fare-by-hour - for the fare chart
  - /top-zones - uses Michaella's algorithm

The backend takes requests, runs SQL queries, and sends back JSON.

### The Database (My part)
- SQLite database file (taxi_data.db)
- 2 tables: zones and trips

Why 2 tables? Because if we stored "Manhattan" with every trip, we'd waste tons of space. Instead we just store a zone_id number and look up the name when needed. This is database normalization.

### Data Processing (Rajveer's part)
- Python script that cleans the raw parquet file
- Removes bad data (negative fares, crazy durations)
- Creates new features like trip_duration_minutes
- Loads clean data into database

## Data Flow

1. Rajveer cleans raw data → saves to database
2. User opens website
3. Frontend asks backend for data
4. Backend queries database
5. Backend sends JSON back
6. Frontend shows charts

## Database Design

I made 2 tables:

**zones table:**
- zone_id (primary key)
- zone_name 
- borough
- service_zone

**trips table:**
- trip_id
- pickup/dropoff times
- pickup/dropoff zone IDs (link to zones)
- distance, fare, tips, etc
- derived features (duration, fare_per_mile, hour)

I added indexes on pickup_hour and borough because those are what users filter by most. Indexes make queries way faster.

## Why we made these choices

| Choice | Why |
|--------|-----|
| SQLite | Simple to set up, no server needed, good enough for our data size |
| Flask | We know Python, its easy to make APIs |
| 2 tables | Normalization - saves space, prevents inconsistent data |
| Indexes | Makes filtering fast even with lots of data |

## Folder Structure

```
nyc-taxi-explorer/
├── backend/
│   ├── app.py           (Kevin)
│   └── algorithms/
│       └── top_zones.py (Michaella)
├── frontend/
│   ├── index.html       (Gael)
│   ├── css/style.css
│   └── js/app.js
├── database/
│   └── schema.sql       (Me - Teniola)
├── data_processing/
│   └── data_cleaner.py  (Rajveer)
└── data/
    ├── raw/             (original files go here)
    └── processed/       (cleaned data)
```

Each person owns their own files so we dont step on each other.

## Things I'd do differently next time

- Maybe use PostgreSQL if we had more data
- Add caching so we dont hit database every time
- Deploy it online instead of just localhost

But for this project SQLite works fine and keeps things simple.
