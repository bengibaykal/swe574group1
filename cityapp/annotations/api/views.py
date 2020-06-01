from rest_framework.generics import (ListAPIView, RetrieveAPIView, DestroyAPIView, UpdateAPIView, CreateAPIView )
from annotations.models import Annotation
from annotations.api.serializers import AnnotationSerializer, AnnotationCreateSerializer
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response

class AnnotationAPIView(ListAPIView):
    queryset = Annotation.objects.all()
    serializer_class = AnnotationSerializer

class AnnotationDetailAPIView(RetrieveAPIView):
    queryset = Annotation.objects.all()
    serializer_class = AnnotationSerializer
    lookup_field = 'pk'

class AnnotationDeleteAPIView(DestroyAPIView):
    queryset = Annotation.objects.all()
    serializer_class = AnnotationSerializer
    lookup_field = 'pk'

class AnnotationUpdateAPIView(UpdateAPIView):
    queryset = Annotation.objects.all()
    serializer_class = AnnotationSerializer
    lookup_field = 'pk'

class AnnotationCreateAPIView(CreateAPIView):
    queryset = Annotation.objects.all()
    serializer_class = AnnotationCreateSerializer

    @api_view(['GET', 'POST'])
    def hello_world(request):
        if request.method == 'POST':

            return Response({"message": "Got some data!", "data": request.data})
        return Response({"message": "Hello, world!"})





