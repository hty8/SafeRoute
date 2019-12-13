from django.http import HttpResponse
from django.shortcuts import render


def home(request):
    return render(request, template_name="home.html")

def index(request):
    return render(request, template_name="index.html")

def about(request):
    return render(request, template_name="about.html")

def map(request):
    return render(request, template_name="map.html")

def heatmap(request):
    return render(request, template_name="heatmap.html")
