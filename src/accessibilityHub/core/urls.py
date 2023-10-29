# -*- coding: utf-8 -*-
"""Urls for the core of accessibility hub."""

from django.urls import path
from django.contrib.auth import views as authViews

from . import views

app_name = "core"
urlpatterns = [
    path("", views.home, name="home"),
    path(
        "accounts/login",
        views.CoreLoginView.as_view(),
        name="login"
    ),
    path(
        'accounts/logout',
        authViews.LogoutView.as_view(template_name='core/logout.html'),
        name='logout'
    ),
    path(
        'accounts/signup',
        views.createAccount,
        name='createAccount'
    )
]
