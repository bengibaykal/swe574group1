from activity_stream.views import *
from django.urls import path

app_name = 'community'

urlpatterns = [
    path('follow-user', follow_unfollow, name="communities-list-user"),


]