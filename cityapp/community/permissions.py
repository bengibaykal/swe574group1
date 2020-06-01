from community.models import Subscription
from rest_framework.permissions import BasePermission


class IsUserInCommunity(BasePermission):
    message = "You are already a member of this Community"

    def has_permission(self, request, view):
        return False if Subscription.objects.filter(created_by=request.user,
                                                    joined_community=request.data["joined_community"]) else True


class IsOwner(BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    message = "You must be the owner of the object"
    def has_object_permission(self, request, view, obj):
        return (obj.created_by == request.user) or request.user.is_superuser