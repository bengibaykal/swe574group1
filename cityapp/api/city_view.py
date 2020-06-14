from city.models import City
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView, GenericAPIView
import json
import requests


class ListCityAPIView(ListAPIView):
    queryset = City.objects.all()


class GetCityInformation(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        city = request.POST.get("city")
        r = requests.get(
            "https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input=" + city + "&inputtype=textquery&fields=photos,formatted_address,name,rating,opening_hours,geometry&key=AIzaSyDX0K8j8RSzk2VyXi3Eks1cy-muY2FmD50")
        return JsonResponse({"message": r.json()}, status=200)
