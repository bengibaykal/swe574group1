from django.forms import modelform_factory
from django.shortcuts import render

# Create your views here.
from rest_framework.generics import (ListAPIView,
                                     RetrieveAPIView,
                                     DestroyAPIView,
                                     UpdateAPIView,
                                     CreateAPIView,)

from city.models import City
from city.serializers import CitySerializer
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from django.http import JsonResponse



class ListCityAPIView(ListAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'user/cities.html'
    serializer_class = CitySerializer

    def get(self, request):
        queryset = City.objects.all()
        return Response({"cities": queryset})


class ShowDetailedCityAPIView(RetrieveAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    lookup_field = 'name'

    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'user/city.html'

    def get(self, request, name):
        city = City.objects.get(name=name)
        return Response({'city': city})

class DeleteCityAPIView(DestroyAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    lookup_field = 'name'

class UpdateCityAPIView(UpdateAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    lookup_field = 'name'

class CreateCityAPIView(CreateAPIView):
    serializer_class = CitySerializer
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'user/create_city.html'

    def get(self, request):
        queryset = City.objects.all()
        return Response({"cities": queryset})


    def post(self, request):
        name = request.data["name"]
        country_name = request.data["country_name"]
        image = request.data["image"]
        print("Name:" + name)
        try:
            city = City.objects.create(name=name, country_name=country_name, image=image)
        except:
            return JsonResponse( {"error": "A community with the same name already exists"})

        return JsonResponse({"name": city.name})


