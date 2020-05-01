from rest_framework import serializers
from city.models import City
class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = [
            'name',
            'country_name',
            'geolocation',
            'image',
            'creation_date',
            'modification_date'
        ]
