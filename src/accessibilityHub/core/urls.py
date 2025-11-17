# -*- coding: utf-8 -*-
"""Urls for the core of accessibility hub."""

from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = "core"
urlpatterns = [
    path(
        "",
        views.home,
        name="home",
    ),
    path(
        "accounts/login",
        views.CoreLoginView.as_view(),
        name="login",
    ),
    path(
        "accounts/logout",
        views.coreLogoutView,
        name="logout",
    ),
    path(
        "accounts/signup",
        views.coreSignupView,
        name="signup",
    ),
    path(
        "about",
        TemplateView.as_view(template_name="core/about.html"),
        name="about",
    ),
]
