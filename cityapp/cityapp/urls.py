from django.urls import include, path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

api_urls = [
    path('community/', include('api.urls')),

]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('community.urls')),
    path('api/', include(api_urls)),
    path('cities/', include('city.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
