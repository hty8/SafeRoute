from django.http import HttpResponse
from django.shortcuts import render
import json
from shapely.geometry import Point, LineString
from app.models import Scores
from django.db import connection, transaction


def index(request):
    return render(request, template_name="index.html")


def map(request):
    return render(request, template_name="map.html")


def heatmap(request):
    return render(request, template_name="heatmap.html")


def get_data(request):

    result = json.loads(request.POST.get('arr'))['arr']

    point_list = []
    for item in result:
        latlon = item.split(", ")
        lat = float(latlon[0])
        lon = float(latlon[1])
        point_list.append(Point(lon, lat))

    # print(point_list)
    line = LineString(point_list)
    print(line)

    line_buffered = str(line.buffer(0.001))
    print(line_buffered)
    response = 'init'

    cursor = connection.cursor()
    query = "SELECT * FROM scores where ST_Intersects(ST_GeomFromText('SRID=4326;{line_buffered}'), geom) = TRUE".format(line_buffered=line_buffered)
    cursor.execute(query)
    print(query)
    #cursor.execute("SELECT * FROM scores WHERE st_intersects(scores.geom,'{line_buffered}'::geometry) = true".format(line_buffered=line_buffered))
    # cursor.execute("SELECT ST_Intersects(ST_GeomFromText('{line_buffered}'), geom) FROM scores".format(line_buffered=line_buffered))
    #cursor.execute("SELECT location,weight FROM scores WHERE location in ({result})".format(result=str(result).strip('[]')))
    #cursor.execute("SELECT weight FROM scores WHERE weight < 5")
    #cursor.execute("SELECT * FROM scores WHERE ST_Intersects(scores.geom,'SRID=4326;POLYGON((28 53,27.707 52.293,27 52,26.293 52.293,26 53,26.293 53.707,27 54,27.707 53.707,28 53))') = true")

    row = cursor.fetchall()
    print(row)
    response_list = []
    for i in range(len(row)):
        latlong = row[i][0].split(", ")
        latitude = float(latlong[0])
        longitude = float(latlong[1])
        loc = row[i][0]
        weight = float(row[i][1])
        response_list.append([loc, latitude, longitude, weight])

    response = json.dumps(response_list)

    print(response)

    return HttpResponse(json.dumps(response), content_type="application/json")
