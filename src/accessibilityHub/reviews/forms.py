# -*- coding: utf-8 -*-
"""Forms for reviews app in accessibilityHub project."""

from django import forms

from .models import Review


class ReviewForm(forms.ModelForm):
    """Form for reviewing a tool."""
    class Meta:
        model = Review
        fields = ['rating', 'comment']


class OwnerForm(forms.Form):
    """Form for Owner model."""
    name = forms.CharField(max_length=128)
    url = forms.URLField()
    description = forms.CharField(widget=forms.Textarea)


class ToolForm(forms.Form):
    """Form for Tool model."""
    name = forms.CharField(max_length=128)
    description = forms.CharField(widget=forms.Textarea)
    url = forms.URLField()
    ownerName = forms.CharField(max_length=128, widget=forms.HiddenInput())
    ownerDescription = forms.CharField(widget=forms.HiddenInput())
    ownerUrl = forms.URLField(widget=forms.HiddenInput())
