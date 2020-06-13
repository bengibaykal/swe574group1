# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from actstream.actions import follow, is_following
from community.actions import unfollow
from community.models import *
from community_user.models import CommunityUser
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse, reverse_lazy
from rest_framework.test import APITestCase
from community.models import Community, PostTemplate, Post

from community.views import USER_MODEL


class CreateCommunityAPIViewTestCase(APITestCase):
    url = reverse("api:create-community")

    def setUp(self):
        self.username = "test"
        self.email = "test@test1.com"
        self.password = "you_know_nothing"
        self.user = CommunityUser.objects.create_user(self.username, self.email, self.password)

    def test_create_community_without_login(self):
        response = self.client.post(self.url, {"name": "bruh"})
        self.assertEqual(403, response.status_code)


# Test Case For Follow & Unfollow Contents
class Follow_Unfollow_TestCase(APITestCase):

    login_url = reverse("api:login")
    ctype_user = ContentType.objects.get_for_model(USER_MODEL)

    def setUp(self):
        self.username_follower = "follower"
        self.email_follower = "follower@test.com"
        self.password_follower = "follower"
        self.follower = CommunityUser.objects.create_user(self.username_follower, self.email_follower, self.password_follower)

        self.username_target = "target"
        self.email_target = "target@test.com"
        self.password_target = "target"
        self.target = CommunityUser.objects.create_user(self.username_target, self.email_target, self.password_target)

        self.username_creator = "creator"
        self.email_creator = "creator@test.com"
        self.password_creator = "creator"
        self.creator = CommunityUser.objects.create_user(self.username_creator, self.email_creator, self.password_creator)

        self.community_name = "target_community"
        self.post_template_name = "target_post_template"
        self.post_name = "target_post"

    def test_follow_user(self):

        response = self.client.post(self.login_url, {"username": self.username_follower, "password": self.password_follower})
        self.assertEqual(200, response.status_code)

        follow(self.follower,self.target)
        follow_status = is_following(self.follower,self.target)

        self.assertEqual(True, follow_status)

    def test_unfollow_user(self):

        response = self.client.post(self.login_url, {"username": self.username_follower, "password": self.password_follower})
        self.assertEqual(200, response.status_code)

        follow(self.follower, self.target)
        follow_status = is_following(self.follower, self.target)
        self.assertEqual(True, follow_status)

        unfollow(self.follower, self.target)
        follow_status = is_following(self.follower, self.target)
        self.assertEqual(False, follow_status)


    def test_follow_community(self):

        print(" ")
        print("Test - Follow Community")
        print("--------------------------")
        response = self.client.post(self.login_url, {"username": self.username_follower, "password": self.password_follower})
        self.assertEqual(200, response.status_code)

        self.target_community = Community.objects.create(name= self.community_name, created_by=self.creator)
        community_list = Community.objects.all()
        status = None
        if self.target_community in community_list:
            status = True
        else:
            status = False

        print("Is Community Created=" + str(status))
        self.assertEqual(True, status) # Check Whether Community Created

        follow(self.follower, self.target_community, actor_only=False)
        follow_status = is_following(self.follower, self.target_community)
        print("Is Community Followed= " + str(follow_status))
        self.assertEqual(True, follow_status)

    def test_unfollow_community(self):

        print(" ")
        print("Test - UnFollow Community")
        print("--------------------------")
        response = self.client.post(self.login_url, {"username": self.username_follower, "password": self.password_follower})
        self.assertEqual(200, response.status_code)

        self.target_community = Community.objects.create(name= self.community_name, created_by=self.creator)
        community_list = Community.objects.all()
        status = None
        if self.target_community in community_list:
            status = True
        else:
            status = False

        print("Is Community Created=" + str(status))
        self.assertEqual(True, status) # Check Whether Community Created

        follow(self.follower, self.target_community, actor_only=False)
        follow_status = is_following(self.follower, self.target_community)
        print("Is Community Followed= " + str(follow_status))
        self.assertEqual(True, follow_status)


        unfollow(self.follower, self.target_community)
        follow_status = is_following(self.follower, self.target_community)
        print("Is Community Still Followed= " + str(follow_status))
        self.assertEqual(False, follow_status)

    def test_follow_posttemplate(self):

        print(" ")
        print("Test - Follow PostTemplate")
        print("--------------------------")
        response = self.client.post(self.login_url, {"username": self.username_follower, "password": self.password_follower})
        self.assertEqual(200, response.status_code)

        self.target_community = Community.objects.create(name= self.community_name, created_by=self.creator)
        community_list = Community.objects.all()
        status = None
        if self.target_community in community_list:
            status = True
        else:
            status = False

        print("Is Community Created=" + str(status))
        self.assertEqual(True, status) # Check Whether Community Created


        self.target_post_template = PostTemplate.objects.create(name= self.post_template_name, created_by=self.creator,
                                                                community= self.target_community)
        post_template_list = PostTemplate.objects.all()
        if self.target_post_template in post_template_list:
            status = True
        else:
            status = False

        print("Is Post Template Created=" + str(status))
        self.assertEqual(True, status) # Check Whether Post Template Created

        follow(self.follower, self.target_post_template, actor_only=False)
        follow_status = is_following(self.follower, self.target_post_template)
        print("Is Post Template Followed= " + str(follow_status))
        self.assertEqual(True, follow_status)


    def test_unfollow_posttemplate(self):

        print(" ")
        print("Test - UnFollow PostTemplate")
        print("--------------------------")
        response = self.client.post(self.login_url, {"username": self.username_follower, "password": self.password_follower})
        self.assertEqual(200, response.status_code)

        self.target_community = Community.objects.create(name= self.community_name, created_by=self.creator)
        community_list = Community.objects.all()
        status = None
        if self.target_community in community_list:
            status = True
        else:
            status = False

        print("Is Community Created=" + str(status))
        self.assertEqual(True, status) # Check Whether Community Created

        self.target_post_template = PostTemplate.objects.create(name= self.post_template_name, created_by=self.creator,
                                                                community= self.target_community)
        post_template_list = PostTemplate.objects.all()
        if self.target_post_template in post_template_list:
            status = True
        else:
            status = False

        print("Is Post Template Created=" + str(status))
        self.assertEqual(True, status) # Check Whether Post Template Created

        follow(self.follower, self.target_post_template, actor_only=False)
        follow_status = is_following(self.follower, self.target_post_template)
        print("Is Post Template Followed= " + str(follow_status))
        self.assertEqual(True, follow_status)

        unfollow(self.follower, self.target_post_template)
        follow_status = is_following(self.follower, self.target_post_template)
        print("Is Post Template Still Followed= " + str(follow_status))
        self.assertEqual(False, follow_status)


    def test_follow_post(self):

        print(" ")
        print("Test - Follow Post")
        print("--------------------------")
        response = self.client.post(self.login_url, {"username": self.username_follower, "password": self.password_follower})
        self.assertEqual(200, response.status_code)

        self.target_community = Community.objects.create(name= self.community_name, created_by=self.creator)
        community_list = Community.objects.all()
        status = None
        if self.target_community in community_list:
            status = True
        else:
            status = False

        print("Is Community Created=" + str(status))
        self.assertEqual(True, status) # Check Whether Community Created

        self.target_post_template = PostTemplate.objects.create(name= self.post_template_name, created_by=self.creator,
                                                                community= self.target_community)
        post_template_list = PostTemplate.objects.all()
        if self.target_post_template in post_template_list:
            status = True
        else:
            status = False

        print("Is Post Template Created=" + str(status))
        self.assertEqual(True, status) # Check Whether Post Template Created


        self.target_post = Post.objects.create(name= self.post_template_name, created_by=self.creator,
                                               community= self.target_community, post_template = self.target_post_template)

        post_list = Post.objects.all()
        if self.target_post in post_list:
            status = True
        else:
            status = False

        print("Is Post Created=" + str(status))
        self.assertEqual(True, status)  # Check Whether Post Created

        follow(self.follower, self.target_post, actor_only=False)
        follow_status = is_following(self.follower, self.target_post)
        print("Is Post Followed= " + str(follow_status))
        self.assertEqual(True, follow_status)

    def test_unfollow_post(self):

        print(" ")
        print("Test - UnFollow Post")
        print("--------------------------")
        response = self.client.post(self.login_url, {"username": self.username_follower, "password": self.password_follower})
        self.assertEqual(200, response.status_code)

        self.target_community = Community.objects.create(name= self.community_name, created_by=self.creator)
        community_list = Community.objects.all()
        status = None
        if self.target_community in community_list:
            status = True
        else:
            status = False

        print("Is Community Created=" + str(status))
        self.assertEqual(True, status) # Check Whether Community Created

        self.target_post_template = PostTemplate.objects.create(name= self.post_template_name, created_by=self.creator,
                                                                community= self.target_community)
        post_template_list = PostTemplate.objects.all()
        if self.target_post_template in post_template_list:
            status = True
        else:
            status = False

        print("Is Post Template Created=" + str(status))
        self.assertEqual(True, status) # Check Whether Post Template Created


        self.target_post = Post.objects.create(name= self.post_template_name, created_by=self.creator,
                                               community= self.target_community, post_template = self.target_post_template)

        post_list = Post.objects.all()
        if self.target_post in post_list:
            status = True
        else:
            status = False

        print("Is Post Created=" + str(status))
        self.assertEqual(True, status)  # Check Whether Post Created

        follow(self.follower, self.target_post, actor_only=False)
        follow_status = is_following(self.follower, self.target_post)
        print("Is Post Followed= " + str(follow_status))
        self.assertEqual(True, follow_status)

        unfollow(self.follower, self.target_post)
        follow_status = is_following(self.follower, self.target_post)
        print("Is Post Still Followed= " + str(follow_status))
        self.assertEqual(False, follow_status)