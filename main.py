import math
from walkscore import LocationScore
import json
import folium
from folium.plugins import HeatMap

from walk_score import *

WALK_SCORE_FILE_NAME = "walk_score_data.json"

def generate_coords_from_bounding_box(
    min_lat: float,
    max_lat: float,
    min_long: float,
    max_long: float,
    interval: float) -> list[float, float]:

    coords = []
    while min_lat <= max_lat:
        min_long_cp = min_long
        while min_long_cp <= max_long:
            coords.append([min_lat, min_long_cp])
            min_long_cp += interval
        min_lat += interval
    return coords

def collect_data(coords: list) -> None:
    walkScoreGenerator = WalkScore()
    walk_score_jsons = []

    for coord in coords:
        lat = coord[0]
        long = coord[1]
        location_score_data = walkScoreGenerator.get_walk_score(latitude=lat, longitude=long)
        location_score_json = LocationScore.to_json(location_score_data)
        walk_score_jsons.append(location_score_json)

    # this is jank as fuck, but it gets the job done
    with open(WALK_SCORE_FILE_NAME, 'w') as walk_score_file:
        walk_score_file.write('{')
        text = "\n \"" + str(1) + "\" : "
        walk_score_file.write(text)
        walk_score_file.write(walk_score_jsons[0])
        for i, score_data in enumerate(walk_score_jsons[1:], start=2):
            text = ",\n \"" + str(i) + "\" : "
            walk_score_file.write(text)
            walk_score_file.write(score_data)
        walk_score_file.write('\n')
        walk_score_file.write('}')

def load_walk_scores_from_json() -> list:
    """ Loads walk scores from the saved json file and returns each of the individual scores in a 
    list"""
    
    walk_scores = []
    with open(WALK_SCORE_FILE_NAME, 'r') as walk_score_json:
        data = json.load(walk_score_json)
        for (k, v) in data.items():
            walk_scores.append(v)
    
    return walk_scores

def get_color_from_score(score: int) -> str:
    if score > 95:
        return "green"
    elif score > 90:
        return "Orange"
    elif score > 85:
        return "darkblue"
    elif score > 80:
        return "red"
    elif score > 75:
        return "lightblue"
    elif score > 70:
        return "brown"
    elif score > 65:
        return "grey"
    else:
        return "black"

def extract_coords_and_walk_score(walk_scores: list) -> dict:
    location_to_walk_score = {}
    for walk_score in walk_scores:
        coords = (walk_score['snapped_coordinates']['latitude'], \
            walk_score['snapped_coordinates']['longitude'])
        score = walk_score['walk']['score']
        color = get_color_from_score(score)

        location_to_walk_score[coords] = { "walk_score": score, "color": color }

    return location_to_walk_score

def draw_and_save_map(location_to_walk_score: dict):
    map = folium.Map([34.2012,-118.4662],zoom_start=11)
    for location, data in location_to_walk_score.items():
        folium.CircleMarker(location, 
                            radius=data["walk_score"] / 25, 
                            color=data["color"], 
                            popup="walk data",
                            fill=True, 
                            fill_opacity=0.7, 
                            fill_color=data["color"]).add_to(map)
    map.save('LA Walkability.html')

def draw_and_save_heat_map(location_to_walk_score: dict):
    lats = []
    longs = []
    walk_scores = []
    for location, data in location_to_walk_score.items():
        lats.append(location[0])
        longs.append(location[1])
        walk_scores.append(data["walk_score"] / 5)

    map = folium.Map([34.2012,-118.4662],zoom_start=11)
    heatmap = HeatMap(list(zip(lats, longs, walk_scores)), 
                        min_opacity=.2,
                        radius=50,
                        blur=75,
                        max_zoom=1)
    heatmap.add_to(map)
    map.save('LA Walkability Heat Map.html')

if __name__ == "__main__":
    coords = generate_coords_from_bounding_box( min_lat=34.011212, 
                                                max_lat=34.026198,
                                                min_long=-118.496391,
                                                max_long=-118.371628,
                                                interval=.001)

    # This line calls the api and actually uses up our api requests, so uncomment only when you 
    # wanna gather new data.
    #collect_data(coords)

    walk_scores = load_walk_scores_from_json()
    location_to_walk_score = extract_coords_and_walk_score(walk_scores)
    draw_and_save_heat_map(location_to_walk_score)