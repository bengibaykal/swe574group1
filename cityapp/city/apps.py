from django.apps import AppConfig

class CityConfig(AppConfig):
    name = 'city'

    def ready(self):
        from django.contrib.admin.models import LogEntry
        from actstream import registry
        from community_user.models import CommunityUser
        registry.register(self.get_model('City'))
        registry.register(CommunityUser)
        registry.register(LogEntry)
