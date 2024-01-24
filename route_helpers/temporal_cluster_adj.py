import math
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")


def calculate_distance(coord1, coord2):
    R = 6371  # Earth radius in kilometers
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance


def calculate_centroid(locations):
    latitudes, longitudes = zip(*[locations[loc]['coords'] for loc in locations])
    return (sum(latitudes) / len(latitudes), sum(longitudes) / len(longitudes))


def adjust_clusters(day_locations, locations, daily_limit_hours):
    cluster_centroids = {day: calculate_centroid({loc: locations[loc] for loc in locs}) for day, locs in day_locations.items()}
    adjusted_day_locations = day_locations.copy()
    for day, locs in day_locations.items():
        total_time = sum(locations[loc]['stay_duration'] for loc in locs)
        while total_time > daily_limit_hours:
            # Find the best location to move based on proximity to other clusters
            loc_to_move = None
            closest_cluster_day = None
            min_distance = float('inf')
            for loc in locs:
                for other_day, centroid in cluster_centroids.items():
                    if other_day != day:
                        distance = calculate_distance(locations[loc]['coords'], centroid)
                        if distance < min_distance:
                            min_distance = distance
                            loc_to_move = loc
                            closest_cluster_day = other_day
            # Move the selected location to the closest cluster
            if loc_to_move:
                adjusted_day_locations[day].remove(loc_to_move)
                adjusted_day_locations[closest_cluster_day].append(loc_to_move)
            # Recalculate total time for the current day
            total_time = sum(locations[loc]['stay_duration'] for loc in adjusted_day_locations[day])

    return adjusted_day_locations