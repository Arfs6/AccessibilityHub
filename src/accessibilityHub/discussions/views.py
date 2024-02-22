from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.views.decorators.http import require_http_methods


@require_http_methods(["GET"])
def index(request: HttpRequest) -> HttpResponse:
    """Discussions index page."""
    return render(request, "discussions/index.html")

