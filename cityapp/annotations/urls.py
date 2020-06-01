from django.urls import include, path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from annotations.api.views import AnnotationAPIView, AnnotationDetailAPIView, AnnotationDeleteAPIView, AnnotationUpdateAPIView, AnnotationCreateAPIView



urlpatterns = [
    path('list/', AnnotationAPIView.as_view(), name='list'),
    path('detail/<id>', AnnotationDetailAPIView.as_view(), name='detail'),
    path('delete/<id>', AnnotationDeleteAPIView.as_view(), name='delete'),
    path('update/<id>', AnnotationUpdateAPIView.as_view(), name='update'),
    path('create', AnnotationCreateAPIView.as_view(), name='create'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



