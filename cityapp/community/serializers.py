from rest_framework import serializers
from rest_framework.serializers import SerializerMethodField
from community.models import *
from community_user.models import CommunityUser


class DataTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostTemplate
        fields = ("name", "description", "community")


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("id", "name")


class CommunitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Community
        fields = ("id", "name")
        optional_fields = ('tags',)


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ("joined_community",)


class CommunitySearchSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)

    class Meta:
        model = Community
        fields = ("id", "name", "tags")


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("post", "content")


class CommentCreateSerializer_ForSpecificPost(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            "content"
        ]


class CommunityUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunityUser
        fields = [
            "username"
        ]

class CommentListSerializer(serializers.ModelSerializer):
    created_by = CommunityUserSerializer()
    class Meta:
        model = Comment
        fields = "__all__"


class CommentDeleteUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            "content"
        ]
