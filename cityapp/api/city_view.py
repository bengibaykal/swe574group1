from city.models import City
from rest_framework.generics import ListAPIView


class ListCityAPIView(ListAPIView):
    queryset = City.objects.all()