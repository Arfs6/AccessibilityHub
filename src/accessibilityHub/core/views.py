from django.conf import settings
from django.contrib.auth import login, logout
from django.contrib.auth import views as authViews  # noqa: N812
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from .forms import CoreUserCreationForm


class CoreLoginView(authViews.LoginView):
    """Extends auth login view."""

    template_name = 'core/login.html'


def coreSignupView(request: HttpRequest) -> HttpResponse:
    """View for creating accounts."""
    if request.method == 'POST':
        _form = CoreUserCreationForm(request.POST)
        if _form.is_valid():
            newUser = _form.save()
            login(request, newUser)
            nextUrl = request.POST.get('next')
            if nextUrl is None:
                nextUrl = settings.LOGIN_REDIRECT_URL
            return HttpResponseRedirect(nextUrl)

        nextUrl = request.POST.get('next')
    else:
        _form = CoreUserCreationForm()
        nextUrl = request.GET.get('next')

    context = {
        'form': _form,
        'next': nextUrl,
    }
    return render(request, 'core/signup.html', context)


def coreLogoutView(request):
    """Logs the user out."""
    if request.method == 'DELETE':
        logout(request)
        response = HttpResponse(status=204)
        nextUrl = request.GET.get('next')
        if not nextUrl:
            nextUrl = settings.LOGOUT_REDIRECT_URL
        response['HX-Redirect'] = nextUrl
        return response

    return render(request, 'core/logout.html', context={'next': request.GET.get('next')})
