# -*- coding: utf-8 -*-
"""Urls for the reviews section of accessibility hub."""

from django.urls import path

from . import views

app_name = "review"
urlpatterns = [
        path("", views.index, name="index"),
        path(
            "<str:slug>_<str:base36Id>",
            views.owner,
            name="owner"
            ),
        path(
            "<str:ownerSlug>_<str:ownerBase36Id>/<str:slug>",
            views.tool,
            name='tool'
            )
        ]
