# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from community.models import Community, Post, PostTemplate, Comment
from django.contrib import admin

# Register your models here.

admin.site.register(Community)
admin.site.register(Post)
admin.site.register(PostTemplate)
admin.site.register(Comment)