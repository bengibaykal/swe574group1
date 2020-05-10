import json

from actstream.feeds import UserActivityMixin, AbstractActivityStream
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.utils.feedgenerator import Atom1Feed, rfc3339_date
from django.contrib.contenttypes.models import ContentType
from django.contrib.syndication.views import Feed, add_domain
from django.contrib.sites.models import Site
from django.utils.encoding import force_str
from django.utils import datetime_safe
from django.views.generic import View
from django.http import HttpResponse, Http404
from django.urls import reverse

from actstream.models import Action, model_stream, user_stream, any_stream


class AbstractActivityStream_W3C2(AbstractActivityStream):

    def format(self, action):
        """
        Returns a formatted dictionary for the given action.
        """
        item = {
            '@context': 'https://www.w3.org/ns/activitystreams',
            'summary': str(action),
            'type': str(action.description),
            'id': self.get_uri(action),
            'url': self.get_url(action),
            'verb': action.verb,
            'published': rfc3339_date(action.timestamp),
            'actor': self.format_actor(action),

        }
        if action.target:
            item['target'] = self.format_target(action)
        if action.action_object:
            item['object'] = self.format_action_object(action)
        return item

    def format_item(self, action, item_type='actor'):
        """
        Returns a formatted dictionary for an individual item based on the action and item_type.
        """
        obj = getattr(action, item_type)
        return {
            'id': self.get_uri(action, obj),
            'url': self.get_url(action, obj),
            'type': ContentType.objects.get_for_model(obj).name,
            'name': str(obj)
        }


class ActivityStreamsBaseFeed_V2(AbstractActivityStream_W3C2, Feed):

    def feed_extra_kwargs(self, obj):
        """
        Returns an extra keyword arguments dictionary that is used when
        initializing the feed generator.
        """
        return {}

    def item_extra_kwargs(self, action):
        """
        Returns an extra keyword arguments dictionary that is used with
        the `add_item` call of the feed generator.
        Add the 'content' field of the 'Entry' item, to be used by the custom
        feed generator.
        """
        item = self.format(action)
        item.pop('title', None)
        item['uri'] = item.pop('url')
        item['activity:verb'] = item.pop('verb')
        return item

    def format_item(self, action, item_type='actor'):
        name = item_type == 'actor' and 'name' or 'title'
        item = super(ActivityStreamsBaseFeed, self).format_item(action, item_type)
        item[name] = item.pop('displayName')
        item['activity:object-type'] = item.pop('objectType')
        item.pop('url')
        return item

    def item_link(self, action):
        return self.get_url(action)

    def item_description(self, action):
        if action.description:
            return force_str(action.description)

    def items(self, obj):
        return self.get_stream()(obj)[:30]



class JSONActivityFeed_V2(AbstractActivityStream_W3C2, View):
    """
    Feed that generates feeds compatible with the v1.0 JSON Activity Stream spec
    """
    def dispatch(self, request, *args, **kwargs):
        return HttpResponse(self.serialize(request, *args, **kwargs),
                            content_type='application/json')

    def serialize(self, request, *args, **kwargs):
        items = self.items(request, *args, **kwargs)
        return json.dumps({
            'totalItems': len(items),
            'items': [self.format(action) for action in items]
        }, indent=4 if 'pretty' in request.GET or 'pretty' in request.POST else None)



# Main Class Where Activity Feed URL Use
class UserJSONActivityFeed_V2(UserActivityMixin, JSONActivityFeed_V2):
    """
    JSON feed of Activity for a given user (where actions are those that the given user follows).
    """
    pass

