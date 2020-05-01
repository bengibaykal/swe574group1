# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from actstream import action
from django.db.models.signals import post_save
from django.utils.encoding import smart_text as smart_unicode
from community_user.models import CommunityUser
from django.db import models
from django.utils.timezone import now
from django.forms import ModelForm, ModelChoiceField
from django.contrib.admin.widgets import RelatedFieldWidgetWrapper
from django.core.exceptions import NON_FIELD_ERRORS
from django.contrib.postgres.fields import JSONField


# Create your models here.
class TimeStamped(models.Model):
    """
    Provides created and updated timestamps on models.
    """

    class Meta:
        abstract = True

    created = models.DateTimeField(null=True, editable=False)
    updated = models.DateTimeField(null=True, editable=False)

    def save(self, *args, **kwargs):
        _now = now()
        self.updated = _now
        if not self.id:
            self.created = _now
        super(TimeStamped, self).save(*args, **kwargs)


class Tag(TimeStamped):
    name = models.CharField(max_length=55)
    created_by = models.ForeignKey(CommunityUser, related_name="tag_author", on_delete=models.CASCADE, blank=True,
                                   null=True)

    # todo field for wiki_data relation

    def __str__(self):
        return smart_unicode(self.name)


class Community(TimeStamped):
    name = models.CharField(max_length=55, unique=True)
    created_by = models.ForeignKey(CommunityUser, related_name="community_author", on_delete=models.CASCADE, blank=True,
                                   null=True)
    description = models.CharField(max_length=55, blank=True, null=True)
    joined_users = models.ManyToManyField(CommunityUser)
    tags = models.ManyToManyField(Tag, related_name="community_tags")
    public_option = models.BooleanField(default=True)

    def __str__(self):
        return smart_unicode(self.name)

# Creating Action Instances by Using Django Signals & Actstream Action
def save_community(sender, instance, **kwargs):
    action.send(instance.created_by, verb="Has Created A New Community - ", target=instance)


post_save.connect(save_community, sender=Community)


class CommunityForm(ModelForm):
    class Meta:
        model = Community
        fields = ['name', 'tags']
        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': "%(model_name)s's %(field_labels)s are not unique.",
            }
        }


class Subscription(TimeStamped):
    created_by = models.ForeignKey(CommunityUser, related_name="subscribed_user", on_delete=models.CASCADE,
                                   blank=True, null=True)
    joined_community = models.ForeignKey(Community, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return smart_unicode(self.created_by.username)


class PostTemplate(TimeStamped):
    name = models.CharField(max_length=55, blank=True, null=True)
    description = models.CharField(max_length=55, blank=True, null=True)
    community = models.ForeignKey(Community, related_name="community_template", on_delete=models.CASCADE, blank=True,
                                  null=True)
    tags = models.ManyToManyField(Tag, related_name="post_template_tags")
    custom_template = JSONField(null=True)
    created_by = models.ForeignKey(CommunityUser, related_name="template_author", on_delete=models.CASCADE, blank=True,
                                   null=True)

# Creating Action Instances by Using Django Signals & Actstream Action
def save_posttemplate(sender, instance, **kwargs):
    action.send(instance.created_by, verb="Has Created A New Post Template - ", target=instance)


post_save.connect(save_posttemplate, sender=PostTemplate)

class Post(TimeStamped):
    name = models.CharField(max_length=55, blank=True, null=True)
    created_by = models.ForeignKey(CommunityUser, related_name="post_author", on_delete=models.CASCADE, blank=True,
                                   null=True)
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    description = models.TextField(max_length=255, blank=True, null=True)
    tags = models.ManyToManyField(Tag, related_name="post_tags")
    post_template = models.ForeignKey(PostTemplate, related_name="post_template", on_delete=models.CASCADE, blank=True,
                                      null=True)
    post_content = JSONField(null=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    audio_version = models.FileField(max_length=55, null=True)

    def __str__(self):
        return smart_unicode(self.name)

# Creating Action Instances by Using Django Signals & Actstream Action
def save_post(sender, instance, **kwargs):
    action.send(instance.created_by, verb="Has Created A New Post - ", target=instance)


post_save.connect(save_post, sender=Post)

class DataFileField(TimeStamped):
    name = models.CharField(max_length=55)
    file_field = models.FileField(max_length=55, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return smart_unicode(self.name)


class Comment(TimeStamped):
    comment_text = models.TextField(max_length=255)
    created_by = models.ForeignKey(CommunityUser, related_name="comment_author", on_delete=models.CASCADE, blank=True,
                                   null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return smart_unicode("%-%".format(self.created_by.username, self.post.name))


# todo
class Recommendation(models.Model):
    name = models.CharField(max_length=55)
