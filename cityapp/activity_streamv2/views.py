# Create your views here.

from actstream.actions import follow, unfollow

# Follow the group (where it is an actor).

def follow_user(request):
    follow(request.user, group)

# Stop following the group.
def unfollow_user(request):
    unfollow(request.user, group)