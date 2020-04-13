# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.apps import apps
from community_user.models import CommunityUser
from community.models import *
from django.contrib import admin
from django.apps import apps

# Register your models here.


models = apps.get_models()

for model in models:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass
