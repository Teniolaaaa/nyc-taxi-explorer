# top zones algorithm
# michaella wrote this
#
# we cant use sort() or Counter because prof said no built-ins
# so we have to do it manually with selection sort
# took a while to figure out but it works


def count_pickups_by_zone(trip_data):
    """
    count how many pickups happened in each zone
    uses a dictionary to keep track
    
    time: O(n) - goes through all trips once
    space: O(z) - one entry per zone
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
    sort the zones by count, highest first
    using selection sort since we cant use built-in sort
    
    basically finds the biggest, puts it first, then finds next biggest, etc
    
    time: O(z^2) - nested loops
    space: O(1) - sorts in place
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
    main function - gets the busiest pickup zones
    
    1. count pickups per zone (using dict)
    2. sort them (using selection sort)
    3. return top n
    
    time: O(t + z^2) where t=trips, z=zones
    space: O(z)
    """

    # count all the pickups
    zone_counts = count_pickups_by_zone(trip_data)

    # Step 2: Convert dictionary to list of tuples
    zone_list = []
    for zone_id in zone_counts:
        zone_list.append((zone_id, zone_counts[zone_id]))

    # Step 3: Manual selection sort
    sorted_zones = selection_sort_descending(zone_list)

    # Step 4: Manually build top N list (NO slicing)
    top_n = []

    limit = n
    if n > len(sorted_zones):
        limit = len(sorted_zones)

    for i in range(limit):
        top_n.append(sorted_zones[i])

    return top_n


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
    CREATE empty list top_n
    FOR i FROM 0 TO n-1:
        ADD sorted_list[i] TO top_n
    RETURN top_n
"""

