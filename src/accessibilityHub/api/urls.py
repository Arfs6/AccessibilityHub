# -*- coding: utf-8 -*-
"""End points for api."""
from django.urls import path

from . import views

app_name = 'api'
urlpatterns = [
    path(
        "tools/<int:toolId>/reviews",
        views.createReview,
        name='createReview'
    ),
]
