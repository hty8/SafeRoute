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

    request_data = json.loads(request.body.decode('utf-8'))
    routes = request_data.get('routes')
    buffer_input = request_data.get('buffer_input')

    response_list = []
    for route in routes:
        point_list = []
        for item in route:
            point_list.append(Point(item.get('longitude'), item.get('latitude')))

        line = LineString(point_list)

        line_buffered = str(line.buffer(buffer_input))

        cursor = connection.cursor()
        query = "SELECT * FROM scores where ST_Intersects(ST_GeomFromEWKT('SRID=4326;{line_buffered}'), geom) = TRUE".format(line_buffered=line_buffered)
        cursor.execute(query)

        scores = cursor.fetchall()
        response_data = []
        for ind, data in enumerate(scores):
            loc = data[1]
            lat = float(data[2])
            lon = float(data[3])
            weight = float(data[4])
            response_data.append([loc, lat, lon, weight])

        response_list.append(response_data)

    response = json.dumps(response_list)

    return HttpResponse(response, content_type="application/json")
