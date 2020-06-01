from datetime import datetime

from actstream.managers import ActionManager, stream


# Generic Django-Activity-Stream Config Code
class MyActionManager(ActionManager):
    @stream
    def mystream(self, obj, verb='posted', time=None):
        if time is None:
            time = datetime.now()
        return obj.actor_actions.filter(verb=verb, timestamp__lte=time)