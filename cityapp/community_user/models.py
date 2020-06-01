# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import AbstractUser, Permission
from django.db import models


# Create your models here.


class CommunityUser(AbstractUser):
    role = models.CharField(max_length=2)

