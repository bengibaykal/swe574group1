from rest_framework.generics import ListAPIView
from city.models import City

class ListCityAPIView(ListAPIView):
    queryset = City.objects.all()