# =============================================================================
# Manual Algorithm: Top N Busiest Pickup Zones
# =============================================================================
# Responsibility: Michaella Kamikazi Karangwa (Algorithm Implementation)
#
# CONSTRAINTS (as per assignment requirements):
# - NO built-in sort() function
# - NO Counter from collections
# - NO pandas groupby
# - Must manually count using dictionary logic
# - Must manually sort using selection sort
#
# This file demonstrates understanding of fundamental algorithms
# and data structures.
# =============================================================================


def count_pickups_by_zone(trip_data):
    """
    Manually count the number of pickups per zone using a dictionary.

    Args:
        trip_data: List of tuples or dictionaries containing pickup_zone_id

    Returns:
        Dictionary with zone_id as key and pickup count as value

    Time Complexity: O(n)
    Space Complexity: O(z)
    """

    zone_counts = {}

    for trip in trip_data:

        # Supports both dict and tuple input
        if isinstance(trip, dict):
            zone_id = trip["pickup_zone_id"]
        else:
            zone_id = trip[0]

        if zone_id in zone_counts:
            zone_counts[zone_id] += 1
        else:
            zone_counts[zone_id] = 1

    return zone_counts


def selection_sort_descending(zone_count_list):
    """
    Manually sort zones by count in descending order using Selection Sort.

    Args:
        zone_count_list: List of tuples [(zone_id, count), ...]

    Returns:
        Sorted list in descending order by count

    Time Complexity: O(z²)
    Space Complexity: O(1)
    """

    n = len(zone_count_list)

    for i in range(n):
        max_idx = i

        for j in range(i + 1, n):
            if zone_count_list[j][1] > zone_count_list[max_idx][1]:
                max_idx = j

        # Swap
        zone_count_list[i], zone_count_list[max_idx] = (
            zone_count_list[max_idx],
            zone_count_list[i],
        )

    return zone_count_list


def get_top_n_zones(trip_data, n=10):
    """
    Main function: Get the top N busiest pickup zones.

    Args:
        trip_data: List of trip records
        n: Number of top zones to return

    Returns:
        List of top N zones as (zone_id, count) tuples

    Overall Time Complexity: O(t + z²)
    Overall Space Complexity: O(z)
    """

    # Step 1: Manual counting
    zone_counts = count_pickups_by_zone(trip_data)

    # Step 2: Convert dictionary to list of tuples
    zone_list = []
    for zone_id in zone_counts:
        zone_list.append((zone_id, zone_counts[zone_id]))

    # Step 3: Manual selection sort
    sorted_zones = selection_sort_descending(zone_list)

    # Step 4: Return top N
    return sorted_zones[:n]


# =============================================================================
# PSEUDO-CODE FOR DOCUMENTATION
# =============================================================================
"""
PSEUDO-CODE: Top N Busiest Zones Algorithm

FUNCTION count_pickups_by_zone(trips):
    CREATE empty dictionary zone_counts
    FOR each trip IN trips:
        zone = trip.pickup_zone_id
        IF zone EXISTS in zone_counts:
            zone_counts[zone] = zone_counts[zone] + 1
        ELSE:
            zone_counts[zone] = 1
    RETURN zone_counts

FUNCTION selection_sort_descending(list):
    n = length of list
    FOR i FROM 0 TO n-1:
        max_index = i
        FOR j FROM i+1 TO n-1:
            IF list[j].count > list[max_index].count:
                max_index = j
        SWAP list[i] WITH list[max_index]
    RETURN list

FUNCTION get_top_n_zones(trips, n):
    counts = count_pickups_by_zone(trips)
    zone_list = CONVERT counts TO list of (zone, count) pairs
    sorted_list = selection_sort_descending(zone_list)
    RETURN first n elements of sorted_list
"""

