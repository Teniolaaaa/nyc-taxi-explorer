# =============================================================================
# Data Cleaning & Feature Engineering Script
# =============================================================================
# Responsibility: Rajveer Singh Jolly (Data Cleaning & Feature Engineering)
#
# This script handles:
# 1. Loading the parquet file
# 2. Merging with taxi_zone_lookup.csv
# 3. Cleaning missing values
# 4. Removing logical outliers
# 5. Creating derived features
# 6. Logging removed/suspicious records
# =============================================================================

import pandas as pd
import os
from datetime import datetime

# Paths to data files
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
RAW_DATA_DIR = os.path.join(DATA_DIR, 'raw')
PROCESSED_DATA_DIR = os.path.join(DATA_DIR, 'processed')
LOG_FILE = os.path.join(DATA_DIR, 'cleaning_log.txt')

def log_message(message):
    """Write a message to the cleaning log file."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(LOG_FILE, 'a') as f:
        f.write(f"[{timestamp}] {message}\n")
    print(message)


def load_parquet_data(filepath):
    """
    Load the yellow taxi trip data from parquet file.
    
    Args:
        filepath: Path to the .parquet file
        
    Returns:
        pandas DataFrame with trip data
    """
    # TODO: Rajveer - Implement parquet loading
    # df = pd.read_parquet(filepath)
    # log_message(f"Loaded {len(df)} records from parquet file")
    pass


def load_zone_lookup(filepath):
    """
    Load the taxi zone lookup CSV file.
    
    Args:
        filepath: Path to taxi_zone_lookup.csv
        
    Returns:
        pandas DataFrame with zone information
    """
    # TODO: Rajveer - Implement CSV loading
    # zone_df = pd.read_csv(filepath)
    # log_message(f"Loaded {len(zone_df)} zones from lookup file")
    pass


def merge_with_zones(trip_df, zone_df):
    """
    Merge trip data with zone lookup for both pickup and dropoff locations.
    
    Args:
        trip_df: DataFrame with trip data
        zone_df: DataFrame with zone lookup
        
    Returns:
        Merged DataFrame with borough and zone names
    """
    # TODO: Rajveer - Implement merging logic
    # Hint: Merge twice - once for pickup location, once for dropoff
    pass


def clean_missing_values(df):
    """
    Handle missing values in the dataset.
    
    Strategy:
    - Log the number of missing values per column
    - Drop rows with critical missing values (location IDs, timestamps)
    - Fill numeric columns with appropriate defaults if minor
    
    Returns:
        Cleaned DataFrame
    """
    # TODO: Rajveer - Implement missing value handling
    # initial_count = len(df)
    # ... cleaning logic ...
    # log_message(f"Removed {initial_count - len(df)} rows with missing values")
    pass


def remove_outliers(df):
    """
    Remove logical outliers from the dataset.
    
    Outlier Criteria:
    1. Negative trip distance
    2. Negative fare amount
    3. Extreme trip duration (< 1 minute or > 3 hours)
    4. Trip distance = 0 but fare > 0 (suspicious)
    5. Unrealistic fare per mile (> $100/mile)
    
    Returns:
        DataFrame with outliers removed
    """
    # TODO: Rajveer - Implement outlier removal
    # Log each type of outlier separately for transparency
    pass


def create_derived_features(df):
    """
    Create three derived features for deeper analysis.
    
    Derived Features:
    1. trip_duration_minutes: (dropoff_time - pickup_time) in minutes
       - Why: Helps analyze how long trips take across different areas/times
    
    2. fare_per_mile: total_amount / trip_distance
       - Why: Normalizes fare to understand pricing efficiency
       - Handle division by zero (set to 0 if distance is 0)
    
    3. pickup_hour: Hour extracted from pickup datetime (0-23)
       - Why: Enables time-of-day analysis for patterns
    
    Returns:
        DataFrame with new feature columns
    """
    # TODO: Rajveer - Implement feature engineering
    
    # Example for pickup_hour:
    # df['pickup_hour'] = df['tpep_pickup_datetime'].dt.hour
    
    # Example for trip_duration_minutes:
    # df['trip_duration_minutes'] = (df['tpep_dropoff_datetime'] - df['tpep_pickup_datetime']).dt.total_seconds() / 60
    
    # Example for fare_per_mile:
    # df['fare_per_mile'] = df.apply(lambda row: row['total_amount'] / row['trip_distance'] if row['trip_distance'] > 0 else 0, axis=1)
    
    pass


def run_data_pipeline():
    """
    Main function to run the complete data cleaning pipeline.
    
    Steps:
    1. Load parquet data
    2. Load zone lookup
    3. Merge datasets
    4. Clean missing values
    5. Remove outliers
    6. Create derived features
    7. Save processed data
    """
    log_message("=" * 50)
    log_message("Starting data cleaning pipeline")
    log_message("=" * 50)
    
    # TODO: Rajveer - Implement the full pipeline
    # Call each function in order and save the final result
    
    log_message("Data cleaning pipeline completed")


if __name__ == '__main__':
    run_data_pipeline()
