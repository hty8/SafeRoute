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

    line_buffered = str(line.buffer(0.001))
    response = 'init'

    cursor = connection.cursor()
    query = "SELECT * FROM scores where ST_Intersects(ST_GeomFromText('SRID=4326;{line_buffered}'), geom) = TRUE".format(line_buffered=line_buffered)
    cursor.execute(query)

    scores = cursor.fetchall()
    response_list = {}
    for index, data in enumerate(scores):
        lat = float(data[2])
        lon = float(data[3])
        weight = float(data[4])
        response_list[index] = [lat,lon,weight]
    

    return HttpResponse(json.dumps(response_list), content_type="application/json")
