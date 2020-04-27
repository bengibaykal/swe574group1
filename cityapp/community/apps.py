# -*- coding: utf-8 -*-

from django.apps import AppConfig


class CommunityConfig(AppConfig):
    name = 'community'

    def ready(self):
        from actstream import registry
        from community_user.models import CommunityUser
        from community.models import Community, Post, PostTemplate
        from community_user.models import CommunityUser
        registry.register(Community)
        registry.register(CommunityUser)
        registry.register(self.get_model('Community'))
        registry.register(self.get_model('Post'))
        registry.register(self.get_model('PostTemplate'))


