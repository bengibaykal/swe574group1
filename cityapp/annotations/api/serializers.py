from rest_framework import serializers
from annotations.models import Annotation


class AnnotationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Annotation
        fields = ['annotation']
        validators = []


schema = {
    "type": "object",
    "properties": {
        "price": {"type": "number"},
        "name": {"type": "string"},
    },
}


class AnnotationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Annotation
        fields = ['annotation']

    # def validate_annotation(self, value):
    # if value = "ben":
    #    raise serializers.ValidationError("Input data is not in a valid W3C Annotation Data Model.")
    # return value
    # def validate(self, attrs):
    #   if attrs['annotation'] != '':
    #       raise serializers.ValidationError("The schema is null")
    #   validate(instance=self, schema=schema)
    #   return attrs
