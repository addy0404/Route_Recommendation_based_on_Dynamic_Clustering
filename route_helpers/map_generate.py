import folium
import pandas as pd
import numpy as np


def get_color(cluster_num):
    colors = ['red', 'blue', 'black','green', 'purple', 'orange', 'darkred', 
              'lightred', 'beige', 'darkblue', 'darkgreen', 'cadetblue', 
              'darkpurple', 'white', 'pink', 'lightblue', 'lightgreen', 
              'gray', 'lightgray']
    return colors[cluster_num % len(colors)]

#To create the map with the clusters and save on html file
def create_map(places,col_name,map_name="cluster_map.html"):
    avg_lat = places['lat'].mean()
    avg_lon = places['long'].mean()
    mymap = folium.Map(location=[avg_lat, avg_lon], zoom_start=6)
    for idx, row in places.iterrows():
        popup_text = f"{row['name']}"
        folium.CircleMarker(location=[row['lat'], row['long']],
                            radius=5, # you can change the size of the circles here
                            color=get_color(row[col_name]), # you can change the color of the circles here
                            fill=True,
                            fill_color=get_color(row[col_name]), # you can change the fill color here
                            popup=popup_text).add_to(mymap)
        
    mymap.save(map_name)