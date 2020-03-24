from rest_framework.permissions import BasePermission


class IsUserCommunityBuilder(BasePermission):

    def has_permission(self, request, view):
        return request.user.role == 'cb'
