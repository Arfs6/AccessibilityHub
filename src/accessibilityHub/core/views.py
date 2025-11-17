from http.client import HTTPResponse
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest
from django.contrib.auth import views as authViews
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import login, logout

from .forms import CoreUserCreationForm


def home(request):
    """Renders the home page for Accessibility Hub."""
    context = {}
    return render(request, "core/home.html", context)


class CoreLoginView(authViews.LoginView):
    """Extends auth login view."""

    template_name = "core/login.html"


def coreSignupView(request: HttpRequest) -> HttpResponse:
    """View for creating accounts."""
    if request.method == "POST":
        _form = CoreUserCreationForm(request.POST)
        if _form.is_valid():
            newUser = _form.save()
            login(request, newUser)
            next = request.POST.get("next")
            if next is None:
                next = settings.LOGIN_REDIRECT_URL
            return HttpResponseRedirect(next)
        else:
            next = request.POST.get("next")
    else:
        _form = CoreUserCreationForm()
        next = request.GET.get("next")

    context = {
        "form": _form,
        "next": next,
    }
    return render(request, "core/signup.html", context)


def coreLogoutView(request):
    """Logs the user out."""
    if request.method == "DELETE":
        logout(request)
        response = HttpResponse(status=204)
        next = request.GET.get("next")
        if not next:
            next = settings.LOGGIN_REDIRECT_URL
        response["HX-Redirect"] = next
        return response
    else:
        return render(
            request, "core/logout.html", context={"next": request.GET.get("next")}
        )
