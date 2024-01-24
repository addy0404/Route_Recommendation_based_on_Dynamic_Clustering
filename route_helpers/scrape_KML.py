
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup

def get_places_table(file_name):
    kml_filename = file_name 
    locations = []
    with open(kml_filename, "r") as file:
        kml_input = file.readlines()
        kml_input = "".join(kml_input)
        bs_kml_input = BeautifulSoup(kml_input, "xml")
        placemarks = bs_kml_input.findAll('Placemark')
        for placemark in placemarks:
            coords = placemark.find('coordinates').text.strip()
            long = coords.split(',')[0]
            lat = coords.split(',')[1]
            locations.append({
                'name': placemark.find('name').text.strip(),
                'lat': lat,
                'long': long
            })
    locations = pd.DataFrame(locations)
    locations['lat'] = locations['lat'].astype(float)
    locations['long'] = locations['long'].astype(float)
    locations["coords"] = locations.apply(lambda row: (row["lat"], row["long"]), axis=1)

    return locations