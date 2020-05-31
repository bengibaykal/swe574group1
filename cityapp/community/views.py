# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework import status
from django.shortcuts import redirect
import actstream
from actstream import models
from django.contrib.contenttypes.models import ContentType
from community.models import *
from django.shortcuts import render
from community.models import *
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth import logout
from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, CreateAPIView, RetrieveAPIView
from django.db.models import Q
from community_user.models import *
from community_user.permissions import *
from django.forms import modelform_factory
from django.http import JsonResponse
from community_user.serializers import *
from community.serializers import CommunitySerializer
from django.core import serializers


# Create your views here.
from community_user.models import CommunityUser


class IndexTemplateView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "index.html"

    def get(self, request, *args, **kwargs):
        print(request.user)
        if request.user.is_authenticated:
            self.template_name = "user/manager.html"
            user_communities = Community.objects.filter(joined_users=self.request.user)
            user_communities_ids = [comm.id for comm in user_communities]
            posts = Post.objects.filter(community_id__in=user_communities_ids).order_by('-created')[:30]
            communities = Community.objects.filter(joined_users=self.request.user)
            print(request.user)
            return Response({"posts": posts, "communities": communities, "user": request.user},
                            status=status.HTTP_200_OK
                            )
        return Response(
            status=status.HTTP_200_OK
        )


def register_view(request):
    if request.user.is_authenticated:
        return redirect("community:index")

    return render(request, "register.html")


def login_view(request):
    print(request.user)
    if request.user.is_authenticated:
        return redirect("community:index")
    return render(request, "login.html")


def logout_view(request):
    logout(request)
    return redirect('community:index')


class CommunityLoginTemplateView(GenericAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    serializer_class = UserLoginSerializer
    template_name = "login.html"

    def post(self, request, *args, **kwargs):
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.template_name = 'user/manager.html'
            user = serializer.user
            token, _ = Token.objects.get_or_create(user=user)
            user = authenticate(request, username=user.username, password=request.POST.get('password'))
            if user is not None:
                login(request, user)
            return redirect("community:index")
        else:
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

    def get(self, request, *args, **kwargs):
        return redirect("community:index")


# todo Refactor
class CommunitiesListTemplateView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'search.html'

    def get(self, request):
        queryset = Community.objects.all()
        comm = self.request.query_params.get('comm', None)
        print(comm)
        if comm is not None:
            queryset = queryset.filter(Q(name__contains=comm) | Q(tags__name__contains=comm))
        if len(queryset) < 1:
            queryset = Community.objects.all()
        return Response({'comms': queryset})


# todo Refactor
class UserCommunitiesListTemplateView(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'user/communities.html'

    def get(self, request):
        communities = Community.objects.filter(joined_users=self.request.user)
        queryset = Community.objects.all()
        return Response({'comms': queryset, "user": request.user, "communities": communities})

class UserNameFromIDTemplateView(APIView):
    print("response")
    def get(self, request):
        users = CommunityUser.objects.all()
        serialized_qs = serializers.serialize('json', users)
        return Response({'users': serialized_qs})


# todo Refactor
class CommunitiesDetailedTemplateView(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'user/community.html'

    def get(self, request, community_id):
        posts = Post.objects.filter(community__id=community_id)
        communities = Community.objects.filter(joined_users=self.request.user)
        community = Community.objects.filter(id=community_id).first()
        is_user_joined = True if request.user in community.joined_users.all() else False
        return Response({'posts': posts, "user": request.user, "communities": communities, "community": community,
                         "is_user_joined": is_user_joined})


# todo Refactor
class PostsDetailedTemplateView(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'user/post.html'

    def get(self, request, post_id):
        post = Post.objects.filter(id=post_id).first()
        communities = Community.objects.filter(joined_users=self.request.user)
        return Response({'post': post, "user": request.user, "communities": communities})


class CreateCommunityTemplateView(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'user/create_community.html'
    CommunityForm = modelform_factory(Community, fields=('name', 'tags'))

    def post(self, request):
        name = request.data["name"]
        description = request.data["description"]
        try:
            community = Community.objects.create(name=name, description=description, created_by=request.user)
            community.joined_users.add(request.user)
            Subscription.objects.create(created_by=self.request.user, joined_community=community)
        except:
            return JsonResponse(
                {"error": "A community with the same name already exists"})
        tags = request.data.getlist('tag[]')
        tags_obj = []
        for i, tag in enumerate(tags):
            print(i)
            obj, created = Tag.objects.get_or_create(name=tag, created_by=request.user)
            tags_obj.append(obj.id)
        print(tags)
        community.tags.add(*tags_obj)
        return JsonResponse(
            {"community_id": community.id})

    def get(self, request):
        communities = Community.objects.filter(joined_users=self.request.user)
        formset = self.CommunityForm()
        return Response({"formset": formset, "user": request.user, "communities": communities})


class CreatePostTemplateView(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'user/create_post.html'

    def post(self, request, community_id):
        return redirect("/")

    def get(self, request, community_id):
        communities = Community.objects.filter(joined_users=self.request.user)
        templates = PostTemplate.objects.filter(community__id=community_id)
        community = Community.objects.filter(id=community_id).first()
        if request.user in community.joined_users.all():
            return Response(
                {"user": request.user, "communities": communities, "community": community,
                 "templates": templates})
        else:
            return JsonResponse(
                {"error": "error"})


class CreateDataTypeTemplateView(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'user/create_data_type.html'

    def post(self, request, community_id):
        community = Community.objects.filter(id=community_id).first()
        if request.user in community.joined_users.all():
            name = request.data["name"]
            description = request.data["description"]
            community = Community.objects.filter(id=community_id).first()
            post_template = PostTemplate.objects.create(name=name, description=description,
                                                        custom_template=request.data,
                                                        created_by=request.user,
                                                        community=community)
            tags = request.data.getlist('tag[]')
            tags_obj = []
            for i, tag in enumerate(tags):
                print(i)
                obj, created = Tag.objects.get_or_create(name=tag, created_by=request.user)
                tags_obj.append(obj.id)
            print(request.data)
            post_template.tags.add(*tags_obj)
            return JsonResponse(
                {"post_template_id": post_template.id, "community_id": community_id})
        else:
            return JsonResponse({"error": "error"})

    def get(self, request, community_id):
        community = Community.objects.filter(id=community_id).first()
        if request.user in community.joined_users.all():
            communities = Community.objects.filter(joined_users=self.request.user)
            return Response(
                {"user": request.user, "communities": communities, "community_id": community_id})
        else:
            return JsonResponse({"error": "error"})


class DataTypeTemplateView(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'user/data_type.html'

    def get(self, request, data_type_id):
        communities = Community.objects.filter(joined_users=self.request.user)
        data_type = PostTemplate.objects.filter(id=data_type_id).first()
        community_id = data_type.community.id
        community = Community.objects.filter(id=community_id).first()
        if request.user in community.joined_users.all():
            return Response(
                {"user": request.user, "communities": communities, "data_type": data_type,
                 "community_id": community_id})
        else:
            return JsonResponse({"error": "error"})

    def post(self, request, data_type_id):
        if not request.POST._mutable:
            request.POST._mutable = True
        json_template = request.data
        json_template.pop("csrfmiddlewaretoken")
        data_type = PostTemplate.objects.filter(id=data_type_id).first()
        community = data_type.community
        if request.user in community.joined_users.all():
            for data in request.data:
                if type(request.data[data]) is InMemoryUploadedFile:
                    file = DataFileField.objects.create(file_field=request.data[data])
                    print(file.file_field.url.split("/")[2])
                    print(request.data[data].name)
                    request.data[data] = {"url": file.file_field.url.split("/")[2], "type": "file"}
            print(request.data)
            post = Post.objects.create(name=request.data["name"], description=request.data["description"],
                                       post_content=json_template, community=community,
                                       post_template=data_type, created_by=request.user)
            try:
                post.tags.add(*community.tags.all())
            except:
                pass
        else:
            return Response(
                {"error": "error"})
        return redirect("/")


class JoinCommunityTemplateView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, joined_community):
        community = Community.objects.filter(id=joined_community).first()
        community.joined_users.add(request.user)
        Subscription.objects.create(created_by=self.request.user, joined_community=community)
        return redirect("community:community-detail", community.id)


class ListCommunitiesOfCityAPIView(RetrieveAPIView):

    def get(self, request, city_id):
        communities = Community.objects.filter(city_id=city_id)
        serialized_qs = serializers.serialize('json', communities)

        return Response({'communitiesOfCity': serialized_qs})


# User Notification View with Simple Template
USER_MODEL = get_user_model()


def notification(request):
    communities = Community.objects.filter(joined_users=request.user)
    return render(request, 'user/activity.html',
                  context={
                      'ctype': ContentType.objects.get_for_model(USER_MODEL),
                      'actor': request.user,
                      'action_list': actstream.models.user_stream(request.user),
                      'communities': communities
                  }
                  )


# Class for Joined Communities List
class JoinedCommunitiesListTemplateView(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'user/joined_communities.html'

    def get(self, request):
        communities = Community.objects.filter(joined_users=request.user) # For My Communities Panel
        queryset = Community.objects.filter(joined_users=self.request.user)
        return Response({'comms': queryset, "user": request.user, "communities": communities})


class GetAllUsersTemplateView(APIView):
    def get(self, request):
        queryset = CommunityUser.objects.all()
        serialized_qs = serializers.serialize('json', queryset)
        return Response({'users': serialized_qs})