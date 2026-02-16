# Team Task Breakdown
**From: Teniola (Team Leader)**

Hey team, heres what everyone needs to do. I set up the folder structure and database schema already. Check your files - I left TODO comments where you need to write code.

---

## Rajveer - Data Cleaning

Your file: `data_processing/data_cleaner.py`

**What to do:**
1. Load the parquet file with pandas
2. Load taxi_zone_lookup.csv
3. Merge them together (match PULocationID to zone info)
4. Remove bad rows:
   - negative distance or fare (doesnt make sense)
   - trips under 1 min or over 3 hours (probably errors)
   - missing pickup/dropoff locations
5. Create 3 new columns:
   - `trip_duration_minutes` = dropoff time minus pickup time
   - `fare_per_mile` = total_amount / distance (watch out for division by zero!)
   - `pickup_hour` = just the hour from pickup time (0-23)
6. Save cleaned data and log what you removed

Make sure you print out how many rows you removed and why. We need this for the documentation.

---

## Michaella - Top Zones Algorithm

Your file: `backend/algorithms/top_zones.py`

**The rules (IMPORTANT):**
- NO using sort() or sorted()
- NO using Counter
- NO using pandas groupby
- You have to count and sort manually

**What to do:**
1. Write a function that counts pickups per zone using a dictionary
   - Loop through trips, for each zone_id add 1 to its count
2. Write selection sort to sort zones by count (highest first)
   - Find the biggest, swap it to front, repeat
3. Return top N zones

Write comments explaining the time complexity. Like O(n) for counting, O(n^2) for selection sort.

This is to show we actually understand algorithms not just calling libraries.

---

## Kevin - Flask API

Your file: `backend/app.py`

**Endpoints to build:**

1. `GET /summary`
   - Query database for total trips, average fare, average distance
   - Return as JSON

2. `GET /trips?borough=Manhattan&hour=8`
   - Filter trips by borough and/or hour
   - Join with zones table to get zone names
   - Limit to like 100 results so its not too slow

3. `GET /average-fare-by-hour`
   - Group by pickup_hour, calculate AVG(total_amount)
   - Return array of hours and their average fares

4. `GET /top-zones?n=10`
   - Call Michaella's algorithm (import it from algorithms folder)
   - Return zone names and their pickup counts

Test each endpoint in browser or Postman before saying its done.

---

## Gael - Frontend Dashboard

Your files: `frontend/index.html`, `frontend/css/style.css`, `frontend/js/app.js`

**What to do:**
1. Make the filter dropdowns work
   - When user picks borough/hour and clicks Apply, fetch new data
2. Show 3 charts using Chart.js:
   - Bar chart: trips by hour
   - Horizontal bar: top 10 zones
   - Line chart: average fare by hour
3. Update the stat cards with real numbers from /summary
4. Make the table show filtered trips

The fetch functions are started in app.js, you just need to finish them and call the chart functions.

Keep the yellow taxi theme (#FFD700) its looking good.

---

## Timeline

| Day | Who | What |
|-----|-----|------|
| 1-2 | Rajveer | Finish data cleaning |
| 2-3 | Michaella | Finish algorithm |
| 3-4 | Kevin | Finish all endpoints |
| 4-5 | Gael | Finish frontend |
| 5-6 | Everyone | Test together, fix bugs |
| 6-7 | Everyone | Documentation and video |

---

## My part (what I did)

- Created the folder structure
- Wrote schema.sql with 2 tables (zones + trips)
- Added indexes for fast queries  
- Wrote architecture documentation
- Made starter files for everyone with TODO comments

If you have questions just message the group chat. Lets get this done!

- Teniola
