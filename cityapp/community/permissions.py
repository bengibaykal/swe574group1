from rest_framework.permissions import BasePermission
from community.models import Subscription


class IsUserInCommunity(BasePermission):
    message = "You are already a member of this Community"

    def has_permission(self, request, view):
        return False if Subscription.objects.filter(created_by=request.user,
                                                    joined_community=request.data["joined_community"]) else True

