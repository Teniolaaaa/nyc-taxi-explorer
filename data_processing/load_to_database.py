# =============================================================================
# Database Loader Script
# =============================================================================
# Author: Teniola Adam Olaleye
#
# Loads cleaned data into SQLite database
# =============================================================================

import sqlite3
import pandas as pd
import os

DATABASE_PATH = os.path.join(os.path.dirname(__file__), '..', 'database', 'taxi_data.db')
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), '..', 'database', 'schema.sql')
RAW_DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw')
PROCESSED_DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed')


def initialize_database():
    """Create tables using schema.sql"""
    conn = sqlite3.connect(DATABASE_PATH)
    
    with open(SCHEMA_PATH, 'r') as f:
        schema_sql = f.read()
    
    conn.executescript(schema_sql)
    conn.commit()
    conn.close()
    print("Database initialized!")


def load_zones_data():
    """Load zone lookup into zones table - extract from cleaned data"""
    trips_file = os.path.join(PROCESSED_DATA_PATH, 'cleaned_taxi_data.csv')
    
    if not os.path.exists(trips_file):
        print("ERROR: Cleaned data not found, cant extract zones")
        return False
    
    print("Extracting zones from cleaned data...")
    df = pd.read_csv(trips_file)
    
    conn = sqlite3.connect(DATABASE_PATH)
    
    # Get unique pickup zones from the data
    # Rajveer already joined zone info into the cleaned data
    zones_seen = set()
    
    for _, row in df.iterrows():
        pu_id = int(row['PULocationID'])
        if pu_id not in zones_seen:
            zones_seen.add(pu_id)
            zone_name = row['pickup_zone_name'] if pd.notna(row['pickup_zone_name']) else f'Zone {pu_id}'
            borough = row['pickup_borough'] if pd.notna(row['pickup_borough']) else 'Unknown'
            conn.execute("""
                INSERT OR REPLACE INTO zones (zone_id, zone_name, borough, service_zone)
                VALUES (?, ?, ?, ?)
            """, (pu_id, zone_name, borough, ''))
        
        # Also add dropoff zones
        do_id = int(row['DOLocationID'])
        if do_id not in zones_seen:
            zones_seen.add(do_id)
            zone_name = row['dropoff_zone_name'] if pd.notna(row['dropoff_zone_name']) else f'Zone {do_id}'
            borough = row['dropoff_borough'] if pd.notna(row['dropoff_borough']) else 'Unknown'
            conn.execute("""
                INSERT OR REPLACE INTO zones (zone_id, zone_name, borough, service_zone)
                VALUES (?, ?, ?, ?)
            """, (do_id, zone_name, borough, ''))
    
    conn.commit()
    conn.close()
    print(f"Extracted {len(zones_seen)} zones from trip data")
    return True


def load_trips_data():
    """Load cleaned trip data into trips table"""
    trips_file = os.path.join(PROCESSED_DATA_PATH, 'cleaned_taxi_data.csv')
    
    if not os.path.exists(trips_file):
        print(f"ERROR: Cleaned trips file not found: {trips_file}")
        print("Run data_cleaner.py first!")
        return False
    
    print("Loading trips... this might take a minute")
    df = pd.read_csv(trips_file)
    
    conn = sqlite3.connect(DATABASE_PATH)
    
    # Map columns from cleaned data to database schema
    # Rajveer's cleaned data has these columns we need
    inserted = 0
    for _, row in df.iterrows():
        try:
            conn.execute("""
                INSERT INTO trips (
                    pickup_datetime, dropoff_datetime,
                    pickup_zone_id, dropoff_zone_id,
                    trip_distance, passenger_count,
                    fare_amount, tip_amount, tolls_amount, total_amount,
                    payment_type,
                    trip_duration_minutes, fare_per_mile, pickup_hour
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                row.get('tpep_pickup_datetime', ''),
                row.get('tpep_dropoff_datetime', ''),
                int(row.get('PULocationID', 0)),
                int(row.get('DOLocationID', 0)),
                row.get('trip_distance', 0),
                int(row.get('passenger_count', 1)),
                row.get('fare_amount', 0),
                row.get('tip_amount', 0),
                row.get('tolls_amount', 0),
                row.get('total_amount', 0),
                int(row.get('payment_type', 0)) if pd.notna(row.get('payment_type')) else 0,
                row.get('trip_duration_minutes', 0),
                row.get('fare_per_mile', 0),
                int(row.get('pickup_hour', 0))
            ))
            inserted += 1
        except Exception as e:
            # Skip bad rows
            continue
        
        # Progress indicator
        if inserted % 10000 == 0:
            print(f"  Inserted {inserted} trips...")
    
    conn.commit()
    conn.close()
    print(f"Loaded {inserted} trips into database")
    return True


def verify_data():
    """Check data was loaded"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM zones")
    zones = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM trips")
    trips = cursor.fetchone()[0]
    
    print(f"\n--- Database Summary ---")
    print(f"Zones: {zones}")
    print(f"Trips: {trips}")
    
    # Show sample data
    if trips > 0:
        cursor.execute("SELECT pickup_hour, COUNT(*) FROM trips GROUP BY pickup_hour LIMIT 5")
        print("\nTrips by hour (sample):")
        for row in cursor.fetchall():
            print(f"  Hour {row[0]}: {row[1]} trips")
    
    conn.close()


if __name__ == '__main__':
    print("=== Loading Data to Database ===\n")
    
    # Step 1: Create tables
    initialize_database()
    
    # Step 2: Load zones
    load_zones_data()
    
    # Step 3: Load trips
    load_trips_data()
    
    # Step 4: Verify
    verify_data()
    
    print("\nDone!")
