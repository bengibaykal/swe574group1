from rest_framework.generics import CreateAPIView, GenericAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from community_user.permissions import IsUserCommunityBuilder
from community.permissions import IsUserInCommunity
from rest_framework.response import Response
from community.serializers import *
from django.db.models import Q


class CreateCommunityAPIView(CreateAPIView):
    permission_classes = (IsAuthenticated, IsUserCommunityBuilder)
    serializer_class = CommunitySerializer

    def perform_create(self, serializer):
        tags = []
        if self.request.POST.get("tags", False):
            tags = self.request.data["tags"]
        community = serializer.save(created_by=self.request.user, joined_users=[self.request.user], tags=tags)
        Subscription.objects.create(created_by=self.request.user, joined_community=community)
        return community

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)
        instance_serializer = CommunitySearchSerializer(instance)
        return Response(instance_serializer.data)


class JoinCommunityAPIView(CreateAPIView):
    permission_classes = (IsAuthenticated, IsUserInCommunity)
    serializer_class = SubscriptionSerializer

    def perform_create(self, serializer):
        Community.objects.get(pk=self.request.data["joined_community"]).joined_users.add(self.request.user)
        return serializer.save(created_by=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)
        instance_serializer = CommunitySearchSerializer(instance)
        return Response(instance_serializer.data)


class SearchCommunitiesAPIView(ListAPIView):
    serializer_class = CommunitySearchSerializer

    def get_queryset(self):
        queryset = Community.objects.all()
        comm = self.request.query_params.get('comm', None)
        if comm is not None:
            queryset = queryset.filter(Q(name__contains=comm) | Q(tags__name__contains=comm))

        return queryset


class UsersLatestPostsListAPIView(ListAPIView):
    serializer_class = CommunitySearchSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user_communities = Community.objects.filter(joined_users=self.request.user)
        user_communities_ids = [comm.id for comm in user_communities]
        print(user_communities_ids)
        queryset = Post.objects.filter(community_id__in=user_communities_ids)

        return queryset


class CreateDataType(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = DataTypeSerializer

    def perform_create(self, serializer):
        return serializer.save(created_by=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)
        instance_serializer = DataTypeSerializer(instance)
        return Response(instance_serializer.data)

