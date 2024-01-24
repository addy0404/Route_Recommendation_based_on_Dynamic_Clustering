
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
import warnings
warnings.filterwarnings("ignore")
from route_helpers.temporal_cluster_adj import *
from route_helpers.scrape_KML import *
from route_helpers.map_generate import create_map


places = get_places_table("KML_files\Yosemite_locs.kml")
clusters_num = 3

coords = places["coords"].tolist()
kmeans = KMeans(n_clusters=clusters_num, random_state=42).fit(coords)
clusters = kmeans.labels_
centroids  = kmeans.cluster_centers_
places["cluster"] = clusters

create_map(places,"cluster","Output\Yosemite_cluster_map.html")

places["stay_duration"] = [1,2,1,0.5,0.5,1,2,1.5,1.5,1,1,2,1,1,1.5,1.5,0.5]

locations = {}
for _, row in places.iterrows():
    name = row['name']
    coords = row["coords"]
    stay_duration = row['stay_duration']
    locations[name] = {'coords': coords, 'stay_duration': stay_duration}

day_locations = {i: [] for i in range(clusters_num)}
for location, cluster in zip(locations.keys(), clusters):
    day_locations[cluster].append(location)


daily_limit_hours = 7  # Adjust as needed
adjusted_day_locations = adjust_clusters(day_locations, locations, daily_limit_hours)

data_tuples = [(cluster, location) for cluster, locations in adjusted_day_locations.items() for location in locations]
df = pd.DataFrame(data_tuples, columns=['adj_cluster', 'name'])
places = places.merge(df, on='name',how='left')

create_map(places,"adj_cluster","Output\Yosemite_cluster_map_after_adjust.html")

print("Completed")
