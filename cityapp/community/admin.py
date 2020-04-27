# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from community.models import Community, Post, PostTemplate

admin.site.register(Community)
admin.site.register(Post)
admin.site.register(PostTemplate)