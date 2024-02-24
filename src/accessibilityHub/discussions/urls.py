# -*- coding: utf-8 -*-
"""Url config for discussions app."""
from django.urls import path

from . import views

app_name = "discussions"
urlpatterns = [
    path(
        "",
        views.landing,
        name="landing",
    ),
    path(
        "topics",
        views.index,
        name="index",
    ),
    path(
        "topics/new",
        views.newTopic,
        name="newTopic",
    ),
    path(
        "topics/<str:base36Id>",
        views.topicPage,
        name="topicPage",
    ),
    path(
        "search",
        views.search,
        name="search",
    ),
]
