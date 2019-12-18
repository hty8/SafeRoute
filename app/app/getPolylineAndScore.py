import googlemaps
from datetime import datetime
import polyline
import pandas as pd


def replace_str_index(text, index=0, replacement=''):
    return '%s%s%s' % (text[:index], replacement, text[index+1:])

# Read crime scores of streets (will update every week via automation)
score_table = pd.read_excel('data/crime_son.xlsx')

# Insert API key
gmaps = googlemaps.Client(key='AIzaSyA18jMzuWuFQskJh39ivf6O_VPXcc-CzzI')

# Request directions via driving mode and alternative routes
now = datetime.now()
directions_result = gmaps.directions("W Randolph St, Chicago, IL 60607, USA",
                                     "4499-4401 W Washington Blvd, Chicago, IL 60624, USA",
                                     mode="driving",
                                     departure_time=now,
                                     alternatives=True)
print('Getting the route alternatives...')
count = 0
z_value_list = []
# Iterate through each alternative route
for result in directions_result:
    # Get route info
    route_duration_value = result["legs"][0]["duration"]["value"]
    route_duration_text = result["legs"][0]["duration"]["text"]
    route_distance_value = result["legs"][0]["distance"]["value"]
    route_distance_text = result["legs"][0]["distance"]["text"]
    overview_polyline = result["overview_polyline"]["points"]
    overview_path = polyline.decode(overview_polyline)

    address_list = []
    total_threat_score = 0
    # Iterate through every point on the route
    map_data = []
    for path in overview_path:
        # Look up an address with reverse geocoding
        geo_to_address = gmaps.reverse_geocode(path,
                                               result_type="street_address")[0]

        address_components = geo_to_address["address_components"]

        formatted_string = '000XX'

        address_number = address_components[0]["long_name"]

        # Format address to be aligned with score data
        if len(address_number) == 1:
            address_number = '0000X'
        elif len(address_number) == 2:
            address_number = '000XX'
        elif len(address_number) == 3:
            address_number = replace_str_index(formatted_string, 2, address_number[0])
        elif len(address_number) == 4:
            formatted_string = replace_str_index(formatted_string, 1, address_number[0])
            address_number = replace_str_index(formatted_string, 2, address_number[1])
        elif len(address_number) == 5:
            formatted_string = replace_str_index(formatted_string, 0, address_number[0])
            formatted_string = replace_str_index(formatted_string, 1, address_number[1])
            address_number = replace_str_index(formatted_string, 2, address_number[2])
        else:
            address_number = formatted_string

        address_name = address_components[1]["short_name"].upper()

        address = address_number + ' ' + address_name
        # Get each point's score
        if score_table.loc[score_table['Block'] == address]['Score'].any():
            address_threat_score = score_table.loc[score_table['Block'] == address]['Score'].to_list()[0]
        else:
            address_threat_score = 0

        address_list.append([address, address_threat_score])
        map_data.append([path, address_threat_score])

        # Calculate threat score of route
        total_threat_score += address_threat_score

        route_threat_score = total_threat_score / len(address_list)

    count += 1

    print(map_data)

    df = pd.DataFrame(map_data, columns=['point', 'weight'])
    df['weight'] = df.weight.astype(str)
    df['point'] = df.point.astype(str)
    df['point'] = '{location: new google.maps.LatLng' + df['point']

    df['weight'] = ', weight: ' + df['weight'] + '},'
    print(df.head())
    df.to_csv('map_data_'+str(count)+'.csv', index=False)
