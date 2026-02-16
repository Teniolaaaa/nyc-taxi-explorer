# =============================================================================
# NYC Yellow Taxi Data Explorer - Flask Application
# =============================================================================
# Responsibility: Kevin Manzi (Backend API)
# =============================================================================

from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
import os
from algorithms.top_zones import get_top_n_zones

app = Flask(__name__)
CORS(app)

DATABASE_PATH = os.path.join(os.path.dirname(__file__), '..', 'database', 'taxi_data.db')


def get_db_connection():
    if not os.path.exists(DATABASE_PATH):
        raise FileNotFoundError("Database file not found. Ensure ETL process created taxi_data.db")

    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# =============================================================================
# API ENDPOINTS
# =============================================================================

@app.route('/')
def home():
    return jsonify({"message": "NYC Taxi Explorer API is running", "status": "ok"})


@app.route('/summary')
def get_summary():
    """
    GET /summary
    Returns overall statistics about the dataset.
    """
    try:
        conn = get_db_connection()

        query = """
            SELECT 
                COUNT(*) AS total_trips,
                AVG(fare_amount) AS average_fare,
                AVG(trip_distance) AS average_distance
            FROM trips
        """

        result = conn.execute(query).fetchone()
        conn.close()

        return jsonify({
            "total_trips": result["total_trips"],
            "average_fare": round(result["average_fare"], 2) if result["average_fare"] else 0,
            "average_distance": round(result["average_distance"], 2) if result["average_distance"] else 0
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/trips')
def get_trips():
    """
    GET /trips?borough=<borough>&hour=<hour>
    """
    try:
        borough = request.args.get('borough')
        hour = request.args.get('hour')

        conn = get_db_connection()

        query = "SELECT * FROM trips WHERE 1=1"
        params = []

        if borough:
            query += " AND pickup_borough = ?"
            params.append(borough)

        if hour:
            query += " AND pickup_hour = ?"
            params.append(hour)

        query += " LIMIT 100"

        rows = conn.execute(query, params).fetchall()
        conn.close()

        trips = [dict(row) for row in rows]

        return jsonify(trips)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/average-fare-by-hour')
def get_average_fare_by_hour():
    """
    GET /average-fare-by-hour
    """
    try:
        conn = get_db_connection()

        query = """
            SELECT pickup_hour, AVG(fare_amount) AS average_fare
            FROM trips
            GROUP BY pickup_hour
            ORDER BY pickup_hour
        """

        rows = conn.execute(query).fetchall()
        conn.close()

        results = [
            {
                "hour": row["pickup_hour"],
                "average_fare": round(row["average_fare"], 2)
            }
            for row in rows
        ]

        return jsonify(results)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/top-zones')
def get_top_zones():
    """
    GET /top-zones?n=<number>
    Returns top N busiest pickup zones.
    Uses manual sorting algorithm.
    """
    try:
        n = request.args.get('n', default=10, type=int)

        conn = get_db_connection()

        #  Efficient aggregation in SQL (not pulling all rows)
        query = """
            SELECT pickup_zone_id, COUNT(*) AS pickup_count
            FROM trips
            GROUP BY pickup_zone_id
        """

        rows = conn.execute(query).fetchall()
        conn.close()

        # Convert to algorithm-friendly structure
        aggregated_data = [
            {
                "pickup_zone_id": row["pickup_zone_id"],
                "count": row["pickup_count"]
            }
            for row in rows
        ]

        # Using Michaella's manual algorithm for sorting
        top_zones = get_top_n_zones(aggregated_data, n)

        return jsonify(top_zones)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Here is even an Endpoint that returns the available boroughs
@app.route('/boroughs')
def get_boroughs():
    try:
        conn = get_db_connection()
        query = "SELECT DISTINCT pickup_borough FROM trips WHERE pickup_borough IS NOT NULL"
        rows = conn.execute(query).fetchall()
        conn.close()
        return jsonify([row["pickup_borough"] for row in rows])
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)

