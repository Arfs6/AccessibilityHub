# -*- coding: utf-8 -*-
"""Url config for discussions app."""
from django.urls import path

from . import views

app_name = "discussions"
urlpatterns = [
    path(
        "index.html",
        views.landing,
        name="landing",
    ),
    path(
        "topics/index.html",
        views.index,
        name="index"
    ),
    path(
        "topics/new.html",
        views.newTopic,
        name="newTopic",
    ),
    path(
        "topics/<str:base36Id>/index.html",
        views.topicPage,
        name="topicPage",
    ),
]
