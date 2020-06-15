from city.models import City
from community.models import *
from community.serializers import *
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView, GenericAPIView
from django.db.models import Q
import json
import requests


class ListCityAPIView(ListAPIView):
    queryset = City.objects.all()


class GetCityInformation(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        city = request.POST.get("city")
        r = requests.get(
            "https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input=" + city + "&inputtype=textquery&fields=photos,formatted_address,name,rating,opening_hours,geometry&key=AIzaSyDX0K8j8RSzk2VyXi3Eks1cy-muY2FmD50&language=en")
        return JsonResponse({"message": r.json()}, status=200)


class AdvancedSearch(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = DataTypeSearchSerializer

    def get_queryset(self):
        queryset = PostTemplate.objects.all()
        q = self.request.query_params.get('q', None)
        print(self.request.data)
        print(q)
        print(len(queryset))
        if q is not None:
            queryset = queryset.filter(Q(name__contains=q) | Q(tags__name__contains=q) | Q(description__contains=q) | Q(
                community__name__contains=q) | Q(custom_template__contains=q))
        print(len(queryset))
        return queryset
