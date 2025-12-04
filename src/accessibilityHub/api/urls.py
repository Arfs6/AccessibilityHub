"""End points for api."""

from django.urls import path

from . import views  # noqa: TID252

app_name = 'api'
urlpatterns = [
    path('tools/<int:toolId>/reviews', views.createReview, name='createReview'),
    path('owners', views.newOwner, name='newOwner'),
    path('tools', views.newTool, name='newTool'),
]
