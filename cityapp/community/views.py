# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from actstream.views import respond
from django.db.models import Count
from actstream.models import following, Action, Follow
from community import actions
from community.models import *
from community.models import *
from community.serializers import PostSerializer
from community_user.models import *
# Create your views here.
from community_user.models import CommunityUser
from community_user.permissions import *
from community_user.serializers import *
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth import logout
from django.contrib.contenttypes.models import ContentType
from django.core import serializers
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models import Q
from django.forms import modelform_factory
from django.http import JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import GenericAPIView, RetrieveAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import datetime



USER_MODEL = get_user_model()


class IndexTemplateView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "index.html"

    def get(self, request, *args, **kwargs):
        print(request.user)
        if request.user.is_authenticated:
            self.template_name = "user/manager.html"
            user_communities = Community.objects.filter(joined_users=self.request.user)
            user_communities_ids = [comm.id for comm in user_communities]
            # https://stackoverflow.com/questions/32998591/django-count-of-foreign-key-model
            posts = Post.objects.filter(community_id__in=user_communities_ids).order_by('-created')[:30]\
                .annotate(number_of_comments=Count("related_post"))
            communities = Community.objects.filter(joined_users=self.request.user)
            following_objects = following(request.user)
            ctype_community = ContentType.objects.get_for_model(Community)
            ctype_post = ContentType.objects.get_for_model(Post)
            ctype_posttemplate = ContentType.objects.get_for_model(PostTemplate)
            ctype_user = ContentType.objects.get_for_model(USER_MODEL)
            print(request.user)
            return Response({"posts": posts, "communities": communities, "user": request.user,
                             "following": following_objects, "ctype_community": ctype_community,
                             "ctype_post": ctype_post, "ctype_user": ctype_user, "ctype_posttemplate":ctype_posttemplate
                             },
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
        city = request.data["selectedCity"]
        city_ToSend = City.objects.get(name=city)

        try:
            community = Community.objects.create(name=name, description=description, created_by=request.user,
                                                 city_id=city_ToSend)
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


# Class for Joined Communities List
class JoinedCommunitiesListTemplateView(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'user/joined_communities.html'

    def get(self, request):
        communities = Community.objects.filter(joined_users=request.user)  # For My Communities Panel
        queryset = Community.objects.filter(joined_users=self.request.user)
        return Response({'comms': queryset, "user": request.user, "communities": communities})


# User Notification View with Simple Template
USER_MODEL = get_user_model()


def notification(request):
    communities = Community.objects.filter(joined_users=request.user)
    posts = Post.objects.filter(created_by=request.user)

    # https://django-activity-stream.readthedocs.io/en/latest/_modules/actstream/managers.html#FollowManager.following
    following_communities = following(request.user, Community)
    following_posts = following(request.user, Post)
    following_posttemplates = following(request.user, PostTemplate)
    following_users = following(request.user, CommunityUser)

    ctype_community = ContentType.objects.get_for_model(Community)
    ctype_post = ContentType.objects.get_for_model(Post)
    ctype_posttemplate = ContentType.objects.get_for_model(PostTemplate)

    print("Following Users=" + str(following_users))
    print("Following Communities=" + str(following_communities))
    print("Following Post Templates=" + str(following_posttemplates))
    print("Following Posts=" + str(following_posts))

    id_users = []
    for i in following_users:
        id_users.append(i.id)

    id_communities = []
    for i in following_communities:
        id_communities.append(i.id)

    id_posts = []
    for i in following_posts:
        id_posts.append(i.id)

    id_posttemplates = []
    for i in following_posttemplates:
        id_posttemplates.append(i.id)

    # https://docs.djangoproject.com/en/dev/topics/db/queries/#spanning-multi-valued-relationships
    user_activities = Action.objects.filter(actor_object_id__in=id_users).order_by("-timestamp")[:4]
    model_community_activities = Action.objects.filter(target_object_id__in=id_communities).filter(
        target_content_type=ctype_community).exclude(actor_object_id=request.user.id).order_by("-timestamp")[:4]
    model_post_activities = Action.objects.filter(target_object_id__in=id_posts).filter(
        target_content_type=ctype_post).exclude(actor_object_id=request.user.id).order_by("-timestamp")[:4]
    model_posttemplate_activities = Action.objects.filter(target_object_id__in=id_posttemplates).filter(
        target_content_type=ctype_posttemplate).exclude(actor_object_id=request.user.id).order_by("-timestamp")[:4]
    return render(request, 'user/activity.html',
                  context={
                      'ctype': ContentType.objects.get_for_model(USER_MODEL),
                      'actor': request.user,
                      'user_activities': user_activities,
                      'communitiy_activities': model_community_activities,
                      'posttemplate_activities': model_posttemplate_activities,
                      'post_activities': model_post_activities,
                      'communities': communities,
                      'posts': posts
                  }
                  )


def notification_user(request):
    communities = Community.objects.filter(joined_users=request.user)
    posts = Post.objects.filter(created_by=request.user)

    # https://django-activity-stream.readthedocs.io/en/latest/_modules/actstream/managers.html#FollowManager.following
    following_users = following(request.user, CommunityUser)

    print(following_users)

    id_users = []
    for i in following_users:
        id_users.append(i.id)

    # https://docs.djangoproject.com/en/dev/topics/db/queries/#spanning-multi-valued-relationships
    user_activities = Action.objects.filter(actor_object_id__in=id_users).order_by("-timestamp")[:50]

    return render(request, 'user/activity_user.html',
                  context={
                      'ctype': ContentType.objects.get_for_model(USER_MODEL),
                      'actor': request.user,
                      'user_activities': user_activities,
                      'communities': communities,
                      'posts': posts
                  }
                  )


def notification_community(request):
    communities = Community.objects.filter(joined_users=request.user)
    posts = Post.objects.filter(created_by=request.user)

    # https://django-activity-stream.readthedocs.io/en/latest/_modules/actstream/managers.html#FollowManager.following
    following_communities = following(request.user, Community)

    print(following_communities)

    ctype_community = ContentType.objects.get_for_model(Community)

    id_communities = []
    for i in following_communities:
        id_communities.append(i.id)

    # https://docs.djangoproject.com/en/dev/topics/db/queries/#spanning-multi-valued-relationships

    model_community_activities = Action.objects.filter(target_object_id__in=id_communities).filter(
        target_content_type=ctype_community).exclude(actor_object_id=request.user.id).order_by("-timestamp")[:50]

    return render(request, 'user/activity_community.html',
                  context={
                      'ctype': ContentType.objects.get_for_model(USER_MODEL),
                      'actor': request.user,
                      'communitiy_activities': model_community_activities,
                      'communities': communities,
                      'posts': posts
                  }
                  )


def notification_post(request):
    communities = Community.objects.filter(joined_users=request.user)
    posts = Post.objects.filter(created_by=request.user)

    # https://django-activity-stream.readthedocs.io/en/latest/_modules/actstream/managers.html#FollowManager.following
    following_posts = following(request.user, Post)

    print(following_posts)

    ctype_post = ContentType.objects.get_for_model(Post)

    id_posts = []
    for i in following_posts:
        id_posts.append(i.id)

    # https://docs.djangoproject.com/en/dev/topics/db/queries/#spanning-multi-valued-relationships

    model_post_activities = Action.objects.filter(target_object_id__in=id_posts).filter(
        target_content_type=ctype_post).exclude(actor_object_id=request.user.id).order_by("-timestamp")[:50]

    return render(request, 'user/activity_post.html',
                  context={
                      'ctype': ContentType.objects.get_for_model(USER_MODEL),
                      'actor': request.user,
                      'post_activities': model_post_activities,
                      'communities': communities,
                      'posts': posts
                  }
                  )


def notification_posttemplate(request):
    communities = Community.objects.filter(joined_users=request.user)
    posts = Post.objects.filter(created_by=request.user)

    # https://django-activity-stream.readthedocs.io/en/latest/_modules/actstream/managers.html#FollowManager.following
    following_posttemplates = following(request.user, PostTemplate)

    ctype_posttemplate = ContentType.objects.get_for_model(PostTemplate)

    print("Following Post Templates=" + str(following_posttemplates))

    id_posttemplates = []
    for i in following_posttemplates:
        id_posttemplates.append(i.id)

    # https://docs.djangoproject.com/en/dev/topics/db/queries/#spanning-multi-valued-relationships
    model_posttemplate_activities = Action.objects.filter(target_object_id__in=id_posttemplates).filter(
        target_content_type=ctype_posttemplate).exclude(actor_object_id=request.user.id).order_by("-timestamp")[:50]

    return render(request, 'user/activity_posttemplate.html',
                  context={
                      'ctype': ContentType.objects.get_for_model(USER_MODEL),
                      'actor': request.user,
                      'posttemplate_activities': model_posttemplate_activities,
                      'communities': communities,
                      'posts': posts
                  }
                  )


def followings(request):
    communities = Community.objects.filter(joined_users=request.user)
    posts = Post.objects.filter(created_by=request.user)

    # https://django-activity-stream.readthedocs.io/en/latest/_modules/actstream/managers.html#FollowManager.following
    following_communities = following(request.user, Community)[:8]
    following_posts = following(request.user, Post)[:8]
    following_users = following(request.user, CommunityUser)[:8]

    print(following_communities)
    print(following_posts)
    print(following_users)

    return render(request, 'user/followings.html',
                  context={
                      'ctype': ContentType.objects.get_for_model(USER_MODEL),
                      'actor': request.user,
                      'following_users': following_users,
                      'following_communities': following_communities,
                      'following_posts': following_posts,
                      'communities': communities,
                      'posts': posts
                  }
                  )


def followings_user(request):
    communities = Community.objects.filter(joined_users=request.user)
    posts = Post.objects.filter(created_by=request.user)

    # https://django-activity-stream.readthedocs.io/en/latest/_modules/actstream/managers.html#FollowManager.following
    following_users = following(request.user, CommunityUser)[:50]

    print(following_users)

    return render(request, 'user/followings_user.html',
                  context={
                      'ctype': ContentType.objects.get_for_model(USER_MODEL),
                      'actor': request.user,
                      'following_users': following_users,
                      'communities': communities,
                      'posts': posts
                  }
                  )


def followings_community(request):
    communities = Community.objects.filter(joined_users=request.user)
    posts = Post.objects.filter(created_by=request.user)

    # https://django-activity-stream.readthedocs.io/en/latest/_modules/actstream/managers.html#FollowManager.following
    following_communities = following(request.user, Community)[:50]

    print(following_communities)

    return render(request, 'user/followings_community.html',
                  context={
                      'ctype': ContentType.objects.get_for_model(USER_MODEL),
                      'actor': request.user,
                      'following_communities': following_communities,
                      'communities': communities,
                      'posts': posts
                  }
                  )


def followings_post(request):
    communities = Community.objects.filter(joined_users=request.user)
    posts = Post.objects.filter(created_by=request.user)

    # https://django-activity-stream.readthedocs.io/en/latest/_modules/actstream/managers.html#FollowManager.following
    following_posts = following(request.user, Post)[:50]

    print(following_posts)

    return render(request, 'user/followings_post.html',
                  context={
                      'ctype': ContentType.objects.get_for_model(USER_MODEL),
                      'actor': request.user,
                      'following_posts': following_posts,
                      'communities': communities,
                      'posts': posts
                  }
                  )


def followers(request):
    communities = Community.objects.filter(joined_users=request.user)
    posts = Post.objects.filter(created_by=request.user)

    ctype_user = ContentType.objects.get_for_model(USER_MODEL)
    user_followers_ids = Follow.objects.filter(object_id=request.user.id).filter(content_type=ctype_user).values_list(
        "user_id")[:50]

    followers_usernames = CommunityUser.objects.filter(id__in=user_followers_ids)

    print(user_followers_ids)
    print(followers_usernames)

    return render(request, 'user/followers.html',
                  context={
                      'ctype': ContentType.objects.get_for_model(USER_MODEL),
                      'followers': followers_usernames,
                      'communities': communities,
                      'posts': posts
                  }
                  )


class FlagPostAsInappropriate(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PostSerializer

    def post(self, request):
        print("Inside the inAppropriate")
        flagged = True;
        post = Post.objects.get(id=request.data["post_id"])
        post.flags += 1
        print(request.user)
        post.flaggedUsers.add(request.user)
        print(post)
        post.save()
        return Response({'flags_count': post.flags, 'flagged': flagged})


class FlagPostAsAppropriate(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PostSerializer

    def post(self, request):
        print("Inside the Appropriate")
        flagged = False
        post = Post.objects.get(id=request.data["post_id"])
        post.flags -= 1
        post.flaggedUsers.remove(request.user)
        post.save()
        return Response({'flags_count': post.flags, 'flagged': flagged})


class GetAllUsersTemplateView(APIView):
    def get(self, request):
        queryset = CommunityUser.objects.all()
        serialized_qs = serializers.serialize('json', queryset)
        return Response({'users': serialized_qs})


class CommunityDashboardTemplateView(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'user/dashboard.html'

    def get(self, request):
        communities = Community.objects.filter(joined_users=self.request.user)
        created_posts = Post.objects.filter(created_by=request.user)
        created_post_count = created_posts.count()

        posts = Post.objects.filter(community__in=communities)

        ctype_user = ContentType.objects.get_for_model(USER_MODEL)
        user_followers_ids = Follow.objects.filter(object_id=request.user.id).filter(
            content_type=ctype_user).values_list("user_id")

        follower_count = user_followers_ids.count()

        following_users = following(request.user, CommunityUser)
        id_users = []
        for i in following_users:
            id_users.append(i.id)
        following_users_count = len(id_users)

        popular_communities = Community.objects.annotate(number_of_posts=Count('post'))[:5]
        for i in range(0, len(popular_communities)):
            print(popular_communities[i].name)

        return Response(
            {"user": request.user, "communities": communities, "created_post_count": created_post_count,
             "follower_count": follower_count, "following_users_count": following_users_count,
             "popular_communities": popular_communities, "posts": posts})

    def post(self, request):
        old_password = request.POST.get("old_password")
        new_password = request.POST.get("new_password")
        re_new_password = request.POST.get("re_new_password")

        user = request.user
        success = user.check_password(old_password)

        if not success:
            return JsonResponse({"error": "False Old Password"}, status=403)
        elif re_new_password != new_password:
            return JsonResponse({"error": "Passwords not matching"}, status=403)
        else:
            user.set_password(new_password)
            user.save()
            return JsonResponse({"success": "Passwords changed successfully"}, status=200)


class UserCreatedPostsTemplateView(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'user/user_created_posts.html'

    def get(self, request, user_id):
        posts = Post.objects.filter(created_by__id=user_id)
        communities = Community.objects.filter(joined_users=self.request.user)
        user_page = CommunityUser.objects.filter(id=user_id).first()
        return Response({'posts': posts, "user": request.user, "communities": communities, "user_page": user_page})


class DashboardSearch(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        query = self.request.query_params.get('query', None)
        query_post_templates = PostTemplate.objects.filter(
            Q(custom_template__contains=query) | Q(tags__name__contains=query) | Q(name__contains=query) | Q(
                description__contains=query) | Q(
                community__name__contains=query))

        query_posts = Post.objects.filter(
            Q(post_template__in=query_post_templates) | Q(name__contains=query) | Q(description__contains=query) | Q(
                community__name__contains=query) | Q(tags__name__contains=query))

        query_communities = Community.objects.filter(
            Q(name__contains=query) | Q(description__contains=query) | Q(tags__name__contains=query))

        return JsonResponse(
            {'query_post_templates': query_post_templates, "query_posts": query_posts.user,
             "query_communities": query_communities,
             })


def PopularItems(request):
    communities = Community.objects.filter(joined_users=request.user)
    posts = Post.objects.all()

    # The Most Popular Community, Post Template and Posts
    popular_communities = Community.objects.annotate(number_of_posts=Count("post")).order_by("-number_of_posts")[:6]
    popular_post_templates = PostTemplate.objects.annotate(number_of_posts=Count("post_template")).order_by("-number_of_posts")[:4]
    popular_posts = Post.objects.annotate(number_of_comments=Count("related_post")).order_by("-number_of_comments")[:6]

    print("The Most Popular Communities = " + str(popular_communities))
    print("The Most Popular Post Templates = " + str(popular_post_templates))
    print("The Most Popular Posts = " + str(popular_posts))

    # The Most Content Creator User
    users = CommunityUser.objects.all()
    the_most_creative_users = []
    for user in users:
        created_communities = Community.objects.filter(created_by=user.id)
        #print("Created Communities = " + str(created_communities))
        created_community_count = created_communities.count()

        created_posts_templates = PostTemplate.objects.filter(created_by=user.id)
        #print("Created Post Templates = " + str(created_posts_templates))
        created_post_template_count = created_posts_templates.count()

        created_posts = Post.objects.filter(created_by=user.id)
        #print("Created Posts = " + str(created_posts))
        created_post_count = created_posts.count()

        created_comment = Comment.objects.filter(created_by=user.id)
        #print("Created Comments = " + str(created_comment))
        created_comment_count = created_comment.count()

        created_content = created_community_count + created_post_template_count + created_post_count + created_comment_count
        print("Created Content Count = " + str(created_content))
        the_most_creative_users.append((user, created_content))

    # https://stackoverflow.com/questions/10695139/sort-a-list-of-tuples-by-2nd-item-integer-value
    print("List = " + str(the_most_creative_users))
    print("List Sorted= " + str(sorted(the_most_creative_users, key=lambda x: x[1], reverse=True)))

    the_most_creative_users_completed = sorted(the_most_creative_users,key=lambda x: x[1], reverse=True)[:6]

    following_objects = following(request.user)
    ctype_community = ContentType.objects.get_for_model(Community)
    ctype_post = ContentType.objects.get_for_model(Post)
    ctype_posttemplate = ContentType.objects.get_for_model(PostTemplate)
    ctype_user = ContentType.objects.get_for_model(USER_MODEL)


    return render(request, 'user/popular_items.html',
                  context={
                      'ctype': ContentType.objects.get_for_model(USER_MODEL),
                      'communities': communities,
                      'popular_communities': popular_communities,
                      'popular_post_templates': popular_post_templates,
                      'popular_posts': popular_posts,
                      'creative_users': the_most_creative_users_completed,
                      'following': following_objects,
                      'ctype_community': ctype_community,
                      'ctype_posttemplate': ctype_posttemplate,
                      'ctype_post': ctype_post,
                      'ctype_user': ctype_user,
                      'posts': posts,
                      'user': request.user
                  }
                  )
# Override From <Actstream View> In Order To Enable <User Stopped Following> Notification
def follow_unfollow(request, content_type_id, object_id, flag=None, do_follow=True, actor_only=True):
    """
    Creates or deletes the follow relationship between ``request.user`` and the
    actor defined by ``content_type_id``, ``object_id``.
    """
    ctype = get_object_or_404(ContentType, pk=content_type_id)
    instance = get_object_or_404(ctype.model_class(), pk=object_id)

    # If flag was omitted in url, None will pass to flag keyword argument
    flag = flag or ''

    if do_follow:
        actions.follow(request.user, instance, actor_only=actor_only, flag=flag)
        return respond(request, 201)   # CREATED

    actions.unfollow(request.user, instance, flag=flag, send_action=True)
    return respond(request, 204)   # NO CONTENT