# Create your views here.
import base64

from city.models import City
from city.serializers import CitySerializer
from community.models import Community
from django.core import serializers
from django.core.files.base import ContentFile
from django.http import JsonResponse
from rest_framework.generics import (ListAPIView,
                                     RetrieveAPIView,
                                     DestroyAPIView,
                                     UpdateAPIView,
                                     CreateAPIView, )
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response


# Format for Uploading an image
def base64_file(data, name=None):
    _format, _img_str = data.split(';base64,')
    _name, ext = _format.split('/')
    if not name:
        name = _name.split(":")[-1]
    return ContentFile(base64.b64decode(_img_str), name='{}.{}'.format(name, ext))


# Listing all cities view
class ListCityAPIView(ListAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'user/cities.html'
    serializer_class = CitySerializer

    def get(self, request):
        queryset = City.objects.all()
        my_communities = Community.objects.filter(joined_users=self.request.user)
        return Response({"cities": queryset, "communities": my_communities})


# Displaying Specific City View
class ShowDetailedCityAPIView(RetrieveAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    lookup_field = 'name'

    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'user/city.html'

    def get(self, request, name):
        city = City.objects.get(name=name)
        my_communities = Community.objects.filter(joined_users=self.request.user)
        communities = Community.objects.filter(city_id=city.id)

        return Response({'city': city, 'comms': communities, "communities": my_communities})


# Deleting city view (view not compleated):TODO
class DeleteCityAPIView(DestroyAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    lookup_field = 'name'


# Updating city view (view page not compleated):TODO
class UpdateCityAPIView(UpdateAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    lookup_field = 'name'


# Creating a new city view
class CreateCityAPIView(CreateAPIView):
    serializer_class = CitySerializer
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'user/create_city.html'

    def get(self, request):
        communities = Community.objects.filter(joined_users=self.request.user)
        queryset = City.objects.all()
        return Response({"cities": queryset, "communities": communities})

    def post(self, request):
        name = request.data["name"]
        country_name = request.data["country_name"]
        image = request.data["image"]
        if not name:
            return JsonResponse({"error": "City Name Can't be Empty"})
        try:
            city = City.objects.create(name=name, country_name=country_name, image=base64_file(image),
                                       created_by=request.user)
        except Exception as e:
            print(e)
            return JsonResponse({"error": "Error Creating the City"})

        return JsonResponse({"name": city.name})


class ListAllCitiesAPIView(RetrieveAPIView):
    serializer_class = CitySerializer

    def get(self, request):
        queryset = City.objects.all()
        cities_serialized = serializers.serialize('json', queryset)
        return JsonResponse({"cities": cities_serialized})
