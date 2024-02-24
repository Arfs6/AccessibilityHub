from django import forms

from .models import Topic, Comment


class TopicForm(forms.ModelForm):
    """Form for topics."""

    class Meta:
        model = Topic
        fields = ["name", "description"]


class CommentForm(forms.ModelForm):
    """A form for topic comments."""
    class Meta:
        model = Comment
        fields = ["content"]
