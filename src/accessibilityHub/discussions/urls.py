# -*- coding: utf-8 -*-
"""Url config for discussions app."""
from django.urls import path

from . import views

app_name = "discussions"
urlpatterns = [
    path(
        "index.html",
        views.index,
        name="index",
    ),
]
