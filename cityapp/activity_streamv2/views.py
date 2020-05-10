from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse

from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
from actstream import actions, models, compat
from community_user.models import CommunityUser

from actstream.actions import follow, unfollow

# Follow the group (where it is an actor).

def follow_user(request):
    follow(request.user, group)

# Stop following the group.
def unfollow_user(request):
    unfollow(request.user, group)