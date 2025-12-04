from django.contrib.auth.models import User
from django.db import models

from utils import decimal2Base36


class Topic(models.Model):
    """Topic representation.
    A topic must have a name and a description.
    It could have comments.
    """

    name = models.CharField(max_length=128, help_text='Name of the topic.')
    description = models.TextField(help_text='Description of topic.')
    createdBy = models.ForeignKey(
        User,
        models.CASCADE,
        related_name='discussionsTopics',
        help_text='Topic creator',
    )
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-createdAt',)

    @property
    def base36Id(self):
        """A base 36 representation of the id."""
        return decimal2Base36(self.pk)


class Comment(models.Model):
    """Represents a comment in a topic."""

    content = models.TextField(max_length=1024, help_text='Comment text.')
    topic = models.ForeignKey(
        Topic,
        models.CASCADE,
        related_name='comments',
        help_text='The topic this comment is part of',
    )
    createdBy = models.ForeignKey(
        User,
        models.CASCADE,
        related_name='discussionsComments',
        help_text='Comment author',
    )
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-createdAt',)
