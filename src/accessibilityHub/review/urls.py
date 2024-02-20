# -*- coding: utf-8 -*-
"""Urls for the reviews section of accessibility hub."""

from django.urls import path

from . import views

app_name = "review"
urlpatterns = [
        path("", views.index, name="index"),
        path(
            "owners/<str:base36Id>/index.html",
            views.owner,
            name="owner"
            ),
        path(
            "owners/<str:ownerBase36Id>/tools/<str:slug>/index.html",
            views.tool,
            name='tool'
            ),
    path(
        "new",
        views.newTool,
        name="newTool"
    )
        ]
