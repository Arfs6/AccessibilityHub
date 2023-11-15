# -*- coding: utf-8 -*-
"""Forms for review app in accessibilityHub project."""

from django import forms


class ReviewForm(forms.Form):
    RATING_CHOICES = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5')
    ]

    rating = forms.ChoiceField(
        label='Rating',
        choices=RATING_CHOICES,
        widget=forms.Select,
        required=True
    )

    comment = forms.CharField(
        label='Comment',
        widget=forms.Textarea(attrs={'rows': 4}),
        required=False  # Comment field is optional
    )
    userId = forms.CharField(widget=forms.HiddenInput())


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
