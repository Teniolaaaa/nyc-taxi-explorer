# =============================================================================
# NYC Yellow Taxi Data Explorer - Flask Application
# =============================================================================
# Responsibility: Kevin Manzi (Backend API)
# 
# This is the main Flask application file that serves the REST API endpoints.
# Kevin will implement the routes and database connections here.
# =============================================================================

from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing for frontend

# Database path - connects to the SQLite database
DATABASE_PATH = os.path.join(os.path.dirname(__file__), '..', 'database', 'taxi_data.db')

def get_db_connection():
    """
    Create and return a database connection.
    Uses Row factory for dictionary-like access to columns.
    """
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# =============================================================================
# API ENDPOINTS - Kevin will implement these
# =============================================================================

@app.route('/')
def home():
    """Health check endpoint"""
    return jsonify({"message": "NYC Taxi Explorer API is running", "status": "ok"})

@app.route('/summary')
def get_summary():
    """
    GET /summary
    Returns overall statistics about the dataset.
    Example: total trips, average fare, average distance, etc.
    """
    # TODO: Kevin - Implement this endpoint
    pass

@app.route('/trips')
def get_trips():
    """
    GET /trips?borough=<borough>&hour=<hour>
    Returns filtered trip data based on query parameters.
    - borough: Filter by pickup borough (e.g., "Manhattan", "Brooklyn")
    - hour: Filter by pickup hour (0-23)
    """
    # TODO: Kevin - Implement this endpoint
    borough = request.args.get('borough')
    hour = request.args.get('hour')
    pass

@app.route('/average-fare-by-hour')
def get_average_fare_by_hour():
    """
    GET /average-fare-by-hour
    Returns average fare amount grouped by hour of day.
    Useful for understanding fare patterns throughout the day.
    """
    # TODO: Kevin - Implement this endpoint
    pass

@app.route('/top-zones')
def get_top_zones():
    """
    GET /top-zones?n=<number>
    Returns the top N busiest pickup zones.
    This endpoint uses Michaella's manual algorithm implementation.
    """
    # TODO: Kevin - Implement this endpoint
    # Note: Use the algorithm from algorithms/top_zones.py
    pass

if __name__ == '__main__':
    app.run(debug=True, port=5000)
