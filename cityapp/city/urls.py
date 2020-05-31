from django.urls import path
from city.views import *


app_name = 'city'

urlpatterns = [
    path('list', ListCityAPIView.as_view(), name="list-city"),
    path('detail/<name>', ShowDetailedCityAPIView.as_view(), name="detail-city"),
    path('delete/<name>', DeleteCityAPIView.as_view(), name="delete-city"),
    path('update/<name>', UpdateCityAPIView.as_view(), name="update-city"),
    path('create/', CreateCityAPIView.as_view(), name="create-city"),
    path('allCities/', ListAllCitiesAPIView.as_view(), name="all-cities"),
]