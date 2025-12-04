import typing

from django import forms

from .models import Comment, Topic


class TopicForm(forms.ModelForm):
    """Form for topics."""

    class Meta:
        model = Topic
        fields: typing.ClassVar = ['name', 'description']


class CommentForm(forms.ModelForm):
    """A form for topic comments."""

    class Meta:
        model = Comment
        fields: typing.ClassVar = ['content']
