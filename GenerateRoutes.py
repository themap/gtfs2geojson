import csv
import os.path
import json

mypath = input("enter path: ") or "data/"

route_groups = {}
print('Building routes...')
with open(os.path.join(mypath,'gtfs', 'routes.txt')) as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=',')

    # Now reading CSV file line by line
    for row in csv_reader:
        if row['route_type'] not in route_groups:
            route_groups[row['route_type']] = []
        route = {
            'route_id' : row['route_id'],
            'agency_id' : row['agency_id'],
            'short_name' : row['route_short_name'],
            'long_name' : row['route_long_name'],
            'shape_id' : None
        }
        print('Building route : '+row["route_long_name"])
        with open(os.path.join(mypath,'gtfs', 'trips.txt')) as trip_file:
            trip_reader = csv.DictReader(trip_file, delimiter=',')

            # Now reading CSV file line by line
            for trip in trip_reader:
                if trip['route_id'] == route['route_id']:
                    route['shape_id'] = trip['shape_id']
                    break
        if route['shape_id'] == None:
            print("No shape found for route : "+row["long_name"])
            input("Press any key to continue...")
        else:
            route_groups[row['route_type']].append(route)

print('Building shapes...')
all_points = []
with open(os.path.join(mypath,'gtfs', 'shapes.txt')) as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=',')

    # Now reading CSV file line by line
    for row in csv_reader:
        all_points.append({
            'shape_id' : row['shape_id'],
            'sequence' : row['shape_pt_sequence'],
            "coordinates" : [float(row["shape_pt_lon"]),float(row["shape_pt_lat"])]
            })

print('Generating route types...')
for key in route_groups:
    print('Generating route type :'+key)
    geojson = {
        "type": "FeatureCollection",
        "features" : []
    }
    for route in route_groups[key]:
        points = []

        print('Scaning geometry for : '+route['long_name'])
        for point in all_points:
            if point['shape_id'] == route['shape_id']:
                points.append(point)

        points = sorted(points, key=lambda x: float(x["sequence"]), reverse=False)
        feature = {
                "type" : "Feature",
                "properties" : route,
                "geometry" : {
                    "type" : "LineString",
                    "coordinates" : []
                }
            }
        for point in points:
            feature["geometry"]["coordinates"].append(point["coordinates"])
        geojson["features"].append(feature)
    out_file = os.path.join(mypath,key+'-routes.json')
    with open(out_file, 'w') as json_file:
        json.dump(geojson, json_file)
    print('Json file generated : '+out_file)
    print('-------------------------')
print('Process complete.')
