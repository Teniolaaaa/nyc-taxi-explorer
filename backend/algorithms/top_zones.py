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
# - Must manually sort using selection sort or insertion sort
#
# This file demonstrates understanding of fundamental algorithms and data structures.
# =============================================================================

def count_pickups_by_zone(trip_data):
    """
    Manually count the number of pickups per zone using a dictionary.
    
    Args:
        trip_data: List of tuples/dicts containing pickup_zone_id
        
    Returns:
        Dictionary with zone_id as key and pickup count as value
    
    Time Complexity: O(n) where n = number of trips
    Space Complexity: O(z) where z = number of unique zones
    
    Algorithm Explanation:
    - We iterate through each trip once
    - For each trip, we check if the zone exists in our dictionary
    - If yes, increment the count; if no, initialize to 1
    """
    # TODO: Michaella - Implement manual counting logic here
    zone_counts = {}
    
    # Example implementation structure:
    # for trip in trip_data:
    #     zone_id = trip['pickup_zone_id']  # or trip[0] if tuple
    #     if zone_id in zone_counts:
    #         zone_counts[zone_id] = zone_counts[zone_id] + 1
    #     else:
    #         zone_counts[zone_id] = 1
    
    return zone_counts


def selection_sort_descending(zone_count_list):
    """
    Manually sort zones by count in descending order using Selection Sort.
    
    Args:
        zone_count_list: List of tuples [(zone_id, count), ...]
        
    Returns:
        Sorted list in descending order by count
    
    Time Complexity: O(z²) where z = number of zones
    Space Complexity: O(1) - sorts in place
    
    Algorithm Explanation (Selection Sort):
    1. Start from the first position
    2. Find the MAXIMUM element in the unsorted portion
    3. Swap it with the first unsorted position
    4. Move the boundary of sorted portion one step right
    5. Repeat until entire list is sorted
    
    Why Selection Sort?
    - Simple to understand and implement
    - Works well for small datasets (number of zones is limited)
    - Demonstrates understanding of sorting without built-in functions
    """
    # TODO: Michaella - Implement selection sort here
    
    # Example implementation structure:
    # n = len(zone_count_list)
    # for i in range(n):
    #     # Find index of maximum in remaining unsorted portion
    #     max_idx = i
    #     for j in range(i + 1, n):
    #         if zone_count_list[j][1] > zone_count_list[max_idx][1]:
    #             max_idx = j
    #     # Swap the found maximum with first unsorted element
    #     zone_count_list[i], zone_count_list[max_idx] = zone_count_list[max_idx], zone_count_list[i]
    
    return zone_count
    # TODO: Michaella - Combine the functions above
    
    # Step 1: Count pickups per zone
    zone_counts = count_pickups_by_zone(trip_data)
    
    # Step 2: Convert dictionary to list of tuples for sorting
    zone_list = []
    for zone_id in zone_counts:
        zone_list.append((zone_id, zone_counts[zone_id]))
    
    # Step 3: Sort using manual selection sort
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
