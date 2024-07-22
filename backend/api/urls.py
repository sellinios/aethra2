from django.urls import path
from api.views.view_weather import weather_for_place
from api.views.view_geographic_place import nearest_place
from api.views.view_urls_places import all_places_with_urls
from api.views.view_weather_city import weather_for_city
from api.views.view_gfs_forecast import gfs_data
from api.views.view_division import greek_municipalities
from api.views.view_contact_message import contact_message_create

urlpatterns = [
    path('<str:lang_code>/nearest-place/', nearest_place, name='nearest_place'),
    path('<str:lang_code>/weather/<str:continent>/<str:country>/<str:region>/<str:subregion>/<str:city>/', weather_for_place, name='weather_for_place'),
    path('<str:lang_code>/places-with-urls/', all_places_with_urls, name='places_with_urls'),
    path('<str:lang_code>/weather/cities/', weather_for_city, name='weather_for_city'),
    path('weather-data/', gfs_data, name='gfs_data'),
    path('geography/greece/municipalities/', greek_municipalities, name='greek_municipalities'),
    path('contact/', contact_message_create, name='contact_message_create'),
]
