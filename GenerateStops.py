import csv
import os.path
import json

mypath = input("enter path: ") or "data/"

with open(os.path.join(mypath,'gtfs', 'stops.txt')) as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=',')
    geojson = {
        "type": "FeatureCollection",
        "features" : []
    }
    # Now reading CSV file line by line
    for row in csv_reader:
        feature = {
                "type" : "Feature",
                "properties" : {
                    "stop_id" : row["stop_id"],
                    "stop_code" : row["stop_code"],
                    "stop_name" : row["stop_name"]
                },
                "geometry" : {
                    "type" : "Point",
                    "coordinates" : [float(row["stop_lon"]),float(row["stop_lat"])]
                }
            }
        print('Parsing stop : '+row["stop_name"])
        geojson["features"].append(feature)
    out_file = os.path.join(mypath, 'stops.json')
    with open(out_file, 'w') as json_file:
        json.dump(geojson, json_file)
print('Json file generated : '+out_file)
print('-------------------------')
print('Process complete.')
