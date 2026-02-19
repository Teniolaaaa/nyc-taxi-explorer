# data cleaning script
# rajveer did this part
# basically loads the raw data, removes bad rows, and saves clean version
# took forever to figure out what counts as an "outlier" lol

import pandas as pd
import numpy as np
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


def load_trip_data(filepath):
    """
    Load the yellow taxi trip data from parquet or CSV file.
    
    Args:
        filepath: Path to the data file (.parquet or .csv)
        
    Returns:
        pandas DataFrame with trip data
    """
    if filepath.endswith('.parquet'):
        df = pd.read_parquet(filepath)
    elif filepath.endswith('.csv'):
        # Parse dates for CSV files
        date_cols = ['tpep_pickup_datetime', 'tpep_dropoff_datetime']
        df = pd.read_csv(filepath, parse_dates=date_cols)
    else:
        raise ValueError(f"Unsupported file format: {filepath}. Use .parquet or .csv")
    
    log_message(f"Loaded {len(df):,} records from: {filepath}")
    return df


def load_zone_lookup(filepath):
    """
    Load the taxi zone lookup CSV file.
    
    Args:
        filepath: Path to taxi_zone_lookup.csv
        
    Returns:
        pandas DataFrame with zone information
    """
    zone_df = pd.read_csv(filepath)
    log_message(f"Loaded {len(zone_df)} zones from lookup file: {filepath}")
    return zone_df


def merge_with_zones(trip_df, zone_df):
    """
    Merge trip data with zone lookup for both pickup and dropoff locations.
    
    Args:
        trip_df: DataFrame with trip data
        zone_df: DataFrame with zone lookup
        
    Returns:
        Merged DataFrame with borough and zone names
    """
    # Rename zone_df columns for pickup merge
    pickup_zones = zone_df.rename(columns={
        'LocationID': 'PULocationID',
        'Zone': 'pickup_zone_name',
        'Borough': 'pickup_borough'
    })[['PULocationID', 'pickup_zone_name', 'pickup_borough']]
    
    # Rename zone_df columns for dropoff merge
    dropoff_zones = zone_df.rename(columns={
        'LocationID': 'DOLocationID',
        'Zone': 'dropoff_zone_name',
        'Borough': 'dropoff_borough'
    })[['DOLocationID', 'dropoff_zone_name', 'dropoff_borough']]
    
    # Merge for pickup location
    df = trip_df.merge(pickup_zones, on='PULocationID', how='left')
    
    # Merge for dropoff location
    df = df.merge(dropoff_zones, on='DOLocationID', how='left')
    
    log_message(f"Merged with zone lookup. Shape after merge: {df.shape}")
    return df


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
    initial_count = len(df)
    
    # Log missing values per column
    missing_counts = df.isnull().sum()
    if missing_counts.any():
        log_message("Missing values per column:")
        for col, count in missing_counts[missing_counts > 0].items():
            log_message(f"  {col}: {count:,} missing")
    
    # Drop rows with critical missing values
    critical_cols = ['PULocationID', 'DOLocationID', 'tpep_pickup_datetime', 'tpep_dropoff_datetime']
    df_clean = df.dropna(subset=critical_cols).copy()
    
    removed_count = initial_count - len(df_clean)
    if removed_count > 0:
        log_message(f"Removed {removed_count:,} rows with missing critical values (location IDs or timestamps)")
    
    # Fill passenger_count with 1 if missing (assume at least driver)
    if 'passenger_count' in df_clean.columns:
        missing_passengers = df_clean['passenger_count'].isnull().sum()
        if missing_passengers > 0:
            df_clean['passenger_count'] = df_clean['passenger_count'].fillna(1)
            log_message(f"Filled {missing_passengers:,} missing passenger_count with 1")
    
    log_message(f"After missing value cleaning: {len(df_clean):,} rows")
    return df_clean


def remove_duplicates(df):
    """
    Remove duplicate trip records from the dataset.
    
    Duplicates are identified by matching:
    - pickup_datetime
    - dropoff_datetime
    - PULocationID
    - DOLocationID
    - total_amount
    
    This catches exact duplicates while preserving legitimate trips
    that happen to have similar characteristics.
    
    Returns:
        DataFrame with duplicates removed
    """
    initial_count = len(df)
    
    # Define subset of columns to check for duplicates
    # These uniquely identify a trip (same time, locations, and fare)
    duplicate_cols = [
        'tpep_pickup_datetime',
        'tpep_dropoff_datetime',
        'PULocationID',
        'DOLocationID',
        'total_amount'
    ]
    
    # Check which columns exist in the dataframe
    available_cols = [col for col in duplicate_cols if col in df.columns]
    
    if len(available_cols) < 3:
        log_message("Warning: Not enough columns available for duplicate detection")
        return df
    
    # Count duplicates before removal
    duplicate_count = df.duplicated(subset=available_cols, keep='first').sum()
    
    if duplicate_count > 0:
        df = df.drop_duplicates(subset=available_cols, keep='first')
        log_message(f"Removed {duplicate_count:,} duplicate trip records ({duplicate_count/initial_count*100:.2f}%)")
    else:
        log_message("No duplicate records found")
    
    return df


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
    initial_count = len(df)
    
    # 1. Remove negative trip distance
    negative_distance = df[df['trip_distance'] < 0]
    if len(negative_distance) > 0:
        df = df[df['trip_distance'] >= 0]
        log_message(f"Removed {len(negative_distance):,} rows with negative trip distance")
    
    # 2. Remove negative fare amount
    negative_fare = df[df['total_amount'] < 0]
    if len(negative_fare) > 0:
        df = df[df['total_amount'] >= 0]
        log_message(f"Removed {len(negative_fare):,} rows with negative fare amount")
    
    # Calculate duration in minutes for filtering
    df['temp_duration'] = (df['tpep_dropoff_datetime'] - df['tpep_pickup_datetime']).dt.total_seconds() / 60
    
    # 3. Remove extreme trip durations (< 1 minute or > 3 hours = 180 minutes)
    too_short = df[df['temp_duration'] < 1]
    too_long = df[df['temp_duration'] > 180]
    if len(too_short) > 0:
        df = df[df['temp_duration'] >= 1]
        log_message(f"Removed {len(too_short):,} rows with trip duration < 1 minute")
    if len(too_long) > 0:
        df = df[df['temp_duration'] <= 180]
        log_message(f"Removed {len(too_long):,} rows with trip duration > 3 hours")
    
    # 4. Remove trips with distance = 0 but fare > 0 (suspicious)
    zero_distance_with_fare = df[(df['trip_distance'] == 0) & (df['total_amount'] > 0)]
    if len(zero_distance_with_fare) > 0:
        df = df[~((df['trip_distance'] == 0) & (df['total_amount'] > 0))]
        log_message(f"Removed {len(zero_distance_with_fare):,} rows with 0 distance but fare > 0")
    
    # 5. Remove trips with distance = 0 entirely (can't calculate fare per mile)
    zero_distance = df[df['trip_distance'] == 0]
    if len(zero_distance) > 0:
        df = df[df['trip_distance'] > 0]
        log_message(f"Removed {len(zero_distance):,} rows with 0 distance")
    
    # Drop the temp column
    df = df.drop(columns=['temp_duration'])
    
    total_removed = initial_count - len(df)
    log_message(f"Total outliers removed: {total_removed:,} ({total_removed/initial_count*100:.2f}% of data)")
    log_message(f"Remaining rows: {len(df):,}")
    
    return df


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
    df = df.copy()
    
    # 1. pickup_hour: Hour extracted from pickup datetime (0-23)
    df['pickup_hour'] = df['tpep_pickup_datetime'].dt.hour
    
    # 2. trip_duration_minutes: (dropoff_time - pickup_time) in minutes
    df['trip_duration_minutes'] = (
        df['tpep_dropoff_datetime'] - df['tpep_pickup_datetime']
    ).dt.total_seconds() / 60
    
    # 3. fare_per_mile: total_amount / trip_distance (handle division by zero)
    # Using numpy where to avoid division by zero
    df['fare_per_mile'] = np.where(
        df['trip_distance'] > 0,
        df['total_amount'] / df['trip_distance'],
        0
    )
    
    # Remove unrealistic fare per mile (> $100/mile) - likely data errors
    extreme_fare_per_mile = df[df['fare_per_mile'] > 100]
    if len(extreme_fare_per_mile) > 0:
        df = df[df['fare_per_mile'] <= 100]
        log_message(f"Removed {len(extreme_fare_per_mile):,} rows with fare_per_mile > $100/mile")
    
    log_message(f"Created 3 derived features: pickup_hour, trip_duration_minutes, fare_per_mile")
    log_message(f"Final dataset shape: {df.shape}")
    
    return df


def run_data_pipeline(sample_size=None, date_filter=None, output_format='csv'):
    """
    Main function to run the complete data cleaning pipeline.
    
    Args:
        sample_size: Number of rows to sample (e.g., 50000). None = use all.
        date_filter: Date string to filter before (e.g., '2019-01-08'). None = no filter.
        output_format: 'csv' or 'parquet'. Default 'csv' for smaller files.
    
    Steps:
    1. Load trip data (parquet or csv)
    2. Optional: Sample or filter data
    3. Load zone lookup
    4. Merge datasets
    5. Clean missing values
    6. Remove duplicates
    7. Remove outliers
    8. Create derived features
    9. Save processed data
    """
    log_message("=" * 50)
    log_message("Starting data cleaning pipeline")
    log_message("=" * 50)
    
    # File paths
    trip_file = os.path.join(RAW_DATA_DIR, 'yellow_tripdata_2024-01.parquet')
    zone_lookup_file = os.path.join(RAW_DATA_DIR, 'taxi_zone_lookup.csv')
    
    if output_format == 'csv':
        output_file = os.path.join(PROCESSED_DATA_DIR, 'cleaned_taxi_data.csv')
    else:
        output_file = os.path.join(PROCESSED_DATA_DIR, 'cleaned_taxi_data.parquet')
    
    # Alternative: Find any trip data file if specific one doesn't exist
    if not os.path.exists(trip_file):
        # Look for parquet first, then csv
        trip_files = [f for f in os.listdir(RAW_DATA_DIR) 
                      if f.startswith('yellow_tripdata') and 
                      (f.endswith('.parquet') or f.endswith('.csv'))]
        if trip_files:
            trip_file = os.path.join(RAW_DATA_DIR, trip_files[0])
        else:
            log_message(f"ERROR: No trip data file found in {RAW_DATA_DIR}")
            log_message("Expected: yellow_tripdata_*.parquet or yellow_tripdata_*.csv")
            return
    
    # Check for zone lookup
    if not os.path.exists(zone_lookup_file):
        log_message(f"ERROR: Zone lookup file not found: {zone_lookup_file}")
        return
    
    # Create processed directory if it doesn't exist
    os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)
    
    try:
        # Step 1: Load data
        trip_df = load_trip_data(trip_file)
        
        # Optional: Sample or filter data to reduce size
        if sample_size and len(trip_df) > sample_size:
            trip_df = trip_df.sample(n=sample_size, random_state=42)
            log_message(f"Sampled {sample_size:,} rows from dataset")
        
        if date_filter:
            original_count = len(trip_df)
            trip_df = trip_df[trip_df['tpep_pickup_datetime'] < date_filter]
            log_message(f"Filtered to trips before {date_filter}: {len(trip_df):,} rows (removed {original_count - len(trip_df):,})")
        
        zone_df = load_zone_lookup(zone_lookup_file)
        
        # Step 2: Merge with zones
        merged_df = merge_with_zones(trip_df, zone_df)
        
        # Step 3: Clean missing values
        cleaned_df = clean_missing_values(merged_df)
        
        # Step 4: Remove duplicates
        deduped_df = remove_duplicates(cleaned_df)
        
        # Step 5: Remove outliers
        outlier_free_df = remove_outliers(deduped_df)
        
        # Step 6: Create derived features
        final_df = create_derived_features(outlier_free_df)
        
        # Step 7: Save processed data
        if output_format == 'csv':
            final_df.to_csv(output_file, index=False)
        else:
            final_df.to_parquet(output_file, index=False)
        log_message(f"Saved cleaned data to: {output_file}")
        
        # Summary stats
        log_message("=" * 50)
        log_message("CLEANING SUMMARY")
        log_message("=" * 50)
        log_message(f"Original rows: {len(trip_df):,}")
        log_message(f"Final rows: {len(final_df):,}")
        log_message(f"Rows removed: {len(trip_df) - len(final_df):,} ({(len(trip_df) - len(final_df))/len(trip_df)*100:.2f}%)")
        log_message(f"Key columns: pickup_hour, trip_duration_minutes, fare_per_mile, pickup_borough, total_amount")
        
    except Exception as e:
        log_message(f"ERROR: Pipeline failed with exception: {str(e)}")
        raise
    
    log_message("=" * 50)
    log_message("Data cleaning pipeline completed successfully")
    log_message("=" * 50)


if __name__ == '__main__':
    # Default: clean full dataset, output to CSV
    # run_data_pipeline()
    
    # Option 1: Sample 50,000 rows
    # run_data_pipeline(sample_size=50000)
    
    # Option 2: Filter to first week of data
    # run_data_pipeline(date_filter='2019-01-08')
    
    # Option 3: Sample AND filter
    run_data_pipeline(sample_size=100000, output_format='csv')
