# -*- coding: utf-8 -*-
"""Forms for core accessibility hub app."""

from django import forms
from django.contrib.auth import forms as authForm


class CoreUserCreationForm(authForm.UserCreationForm):
    """Extends the default user creation form."""
    email = forms.EmailField(
            label='Email:',
            required=True,
            )
    firstName = forms.CharField(
            label='First Name:',
            required=True,
            )
    lastName = forms.CharField(
            label='Last Name',
            required=False,
            help_text='Optional.'
            )
