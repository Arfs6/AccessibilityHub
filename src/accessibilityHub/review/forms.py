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
