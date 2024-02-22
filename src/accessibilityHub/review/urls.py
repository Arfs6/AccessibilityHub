# -*- coding: utf-8 -*-
"""Urls for the reviews section of accessibility hub."""

from django.urls import path

from . import views

app_name = "review"
urlpatterns = [
        path("index.html", views.index, name="index"),
        path(
            "owners/<str:base36Id>/index.html",
            views.owner,
            name="owner"
            ),
        path(
            "owners/<str:ownerBase36Id>/<str:toolSlug>/index.html",
            views.tool,
            name='tool'
            ),
    path(
        "new",
        views.newTool,
        name="newTool"
    ),
    path(
        "owners/<str:ownerBase36Id>/<str:toolSlug>/<int:userId>.html",
        views.userReview,
        name='userReview'
    ),
    path(
        "search.html",
        views.search,
        name="search"
    ),
        ]
