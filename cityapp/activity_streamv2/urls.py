from django.urls import path
from activity_stream.views import *

app_name = 'community'

urlpatterns = [
    path('follow-user', follow_unfollow, name="communities-list-user"),


]