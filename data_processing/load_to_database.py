# =============================================================================
# Database Loader Script
# =============================================================================
# Responsibility: Shared (Teniola designs schema, Rajveer prepares data)
#
# This script loads the cleaned data into the SQLite database.
# =============================================================================

import sqlite3
import pandas as pd
import os

DATABASE_PATH = os.path.join(os.path.dirname(__file__), '..', 'database', 'taxi_data.db')
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), '..', 'database', 'schema.sql')
PROCESSED_DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed')

def initialize_database():
    """
    Create database tables using the schema.sql file.
    """
    conn = sqlite3.connect(DATABASE_PATH)
    
    with open(SCHEMA_PATH, 'r') as schema_file:
        schema_sql = schema_file.read()
    
    conn.executescript(schema_sql)
    conn.commit()
    conn.close()
    print("Database initialized successfully!")


def load_zones_data(zone_csv_path):
    """
    Load zone lookup data into the zones table.
    """
    # TODO: Implement zone data loading
    pass


def load_trips_data(trips_csv_path):
    """
    Load cleaned trip data into the trips table.
    """
    # TODO: Implement trip data loading
    pass


def verify_data_loaded():
    """
    Verify that data was loaded correctly by printing counts.
    """
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM zones")
    zone_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM trips")
    trip_count = cursor.fetchone()[0]
    
    print(f"Zones loaded: {zone_count}")
    print(f"Trips loaded: {trip_count}")
    
    conn.close()


if __name__ == '__main__':
    initialize_database()
    # load_zones_data(...)
    # load_trips_data(...)
    verify_data_loaded()
