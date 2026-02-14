-- ================================================
-- Database Schema for NYC Taxi Explorer
-- Author: Teniola Adam Olaleye
-- Role: Team Leader / Database Design
-- ================================================

-- I chose to split the data into 2 tables because storing
-- borough name for every single trip wastes space. With 
-- millions of trips, this adds up fast.

-- First drop existing tables (in case we need to recreate)
DROP TABLE IF EXISTS trips;
DROP TABLE IF EXISTS zones;


-- ZONES TABLE
-- This comes from the taxi_zone_lookup.csv file
-- It maps zone IDs to actual names and boroughs
CREATE TABLE zones (
    zone_id INTEGER PRIMARY KEY,
    zone_name TEXT NOT NULL,
    borough TEXT NOT NULL,
    service_zone TEXT
);

-- Adding index on borough since we filter by it a lot
CREATE INDEX idx_borough ON zones(borough);


-- TRIPS TABLE  
-- Main table with all the taxi ride data
-- Includes the 3 derived features Rajveer will calculate
CREATE TABLE trips (
    trip_id INTEGER PRIMARY KEY AUTOINCREMENT,
    
    -- when did the trip happen
    pickup_datetime TEXT NOT NULL,
    dropoff_datetime TEXT NOT NULL,
    
    -- where (links to zones table)
    pickup_zone_id INTEGER NOT NULL,
    dropoff_zone_id INTEGER NOT NULL,
    
    -- trip info
    trip_distance REAL NOT NULL,
    passenger_count INTEGER,
    
    -- money stuff
    fare_amount REAL NOT NULL,
    tip_amount REAL DEFAULT 0,
    tolls_amount REAL DEFAULT 0,
    total_amount REAL NOT NULL,
    payment_type INTEGER,
    
    -- DERIVED FEATURES (calculated during cleaning)
    -- these give us more insights than raw data
    trip_duration_minutes REAL,    -- how long was the ride
    fare_per_mile REAL,            -- cost efficiency 
    pickup_hour INTEGER NOT NULL,  -- for time-of-day analysis
    
    -- foreign keys to link tables
    FOREIGN KEY (pickup_zone_id) REFERENCES zones(zone_id),
    FOREIGN KEY (dropoff_zone_id) REFERENCES zones(zone_id)
);

-- INDEXES
-- These speed up queries that filter by these columns
-- Without indexes, SQLite scans the whole table which is slow

CREATE INDEX idx_pickup_hour ON trips(pickup_hour);
CREATE INDEX idx_pickup_zone ON trips(pickup_zone_id);
CREATE INDEX idx_dropoff_zone ON trips(dropoff_zone_id);

-- composite index for when we filter by hour AND zone together
CREATE INDEX idx_hour_and_zone ON trips(pickup_hour, pickup_zone_id);


-- ================================================
-- WHY I DESIGNED IT THIS WAY (for documentation)
-- ================================================
-- 
-- Normalization: Instead of storing "Manhattan" 10000 times,
-- we store zone_id (just a number) and look up the name.
-- This is called 3rd Normal Form.
--
-- Indexes: The dashboard lets users filter by hour and borough.
-- Without indexes these queries would be super slow on big data.
--
-- Foreign Keys: Makes sure every trip points to a real zone.
-- Prevents bad data from getting in.
-- ================================================
