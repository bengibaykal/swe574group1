# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from community.models import *
from community_user.models import CommunityUser
from django.urls import reverse
from rest_framework.test import APITestCase


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
