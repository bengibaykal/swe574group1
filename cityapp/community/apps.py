from django.apps import AppConfig

class CommunityConfig(AppConfig):
    name = 'community'

    def ready(self):
        from django.contrib.admin.models import LogEntry
        from actstream import registry
        from community_user.models import CommunityUser
        registry.register(self.get_model('Community'))
        registry.register(self.get_model('Post'))
        registry.register(self.get_model('PostTemplate'))
        registry.register(self.get_model('Recommendation'))
        registry.register(CommunityUser)
        registry.register(LogEntry)
