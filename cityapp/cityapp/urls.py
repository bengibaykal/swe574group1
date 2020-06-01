from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

api_urls = [
    path('community/', include('api.urls')),

]

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', include('community.urls')),
                  path('api/', include(api_urls)),
                  path('city/', include('city.urls')),
                  path('activity/', include('actstream.urls')),  # Activity Stream URL
                  path('api/annotations/', include('annotations.api.urls')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
