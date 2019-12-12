import googlemaps
from datetime import datetime
import polyline
import pandas as pd


def replace_str_index(text, index=0, replacement=''):
    return '%s%s%s' % (text[:index], replacement, text[index+1:])

# Read crime scores of streets (will update every week via automation)
score_table = pd.read_excel('crime_son.xlsx')

# Insert API key
gmaps = googlemaps.Client(key='')

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
            address_list.append([address, address_threat_score])
        else:
            address_threat_score = 0
        # Calculate threat score of route
        total_threat_score += address_threat_score

        route_threat_score = total_threat_score / len(address_list)

    count += 1
    # Assign weights
    w_l = 0.318126
    w_d = 0.33621
    w_s = 0.345664
    # Calculate z-value
    z_value = (w_l * route_distance_value) + (w_d * route_distance_value) + (w_s * route_threat_score)

    z_value_list.append(z_value)
    # Print out route's info
    print('--- ' + 'Route Alternative ' + str(count) + ' ---')
    print(address_list)
    print('Distance of this route is ' + str(route_distance_text))
    print('Duration of this route is ' + str(route_duration_text))
    print('Threat score of this route is ' + str(route_threat_score) + '\n')
# Print out each route's z-value
for a in range(len(z_value_list)):
    print('z value of Route Alternative ' + str(a+1) + ' is ' + str(z_value_list[a]))
# Get minimum z-value
minimum_z_value = min(z_value_list)
index_of_min = z_value_list.index(minimum_z_value)
# Print out result
print('\nMinimum z_value is: ' + str(minimum_z_value))
print('\nYou should choose Route Alternative ' + str(index_of_min+1))
