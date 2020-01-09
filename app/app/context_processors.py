from django.conf import settings # import the settings file


def google_maps_api_key(request):
    return {'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY}
