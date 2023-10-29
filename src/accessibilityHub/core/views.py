from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest
from django.contrib.auth import views as authViews
from django.contrib.auth.models import User
from django.contrib.auth import login

from .forms import CoreUserCreationForm

def home(request):
    """Renders the home page for Accessibility Hub."""
    context = {
            }
    return render(request, "core/home.html", context)


class CoreLoginView(authViews.LoginView):
    """Extends auth login view."""
    template_name = 'core/login.html'


def createAccount(request: HttpRequest) -> HttpResponse:
    """View for creating accounts.
    """
    if request.method == "POST":
        _form = CoreUserCreationForm(request.POST)
        if _form.is_valid():
            # if passwords aren't equal, code execution won't reach here.
            data = _form.cleaned_data
            newUser = User.objects.create_user(data['username'], password=data['password1'], email=data['email'])
            newUser.first_name = data['firstName']
            if data['lastName']:
                newUser.last_name = data['lastName']
            newUser.save()
            login(request, newUser)
            return HttpResponseRedirect(request.POST.get("next", "/"))
    else:
        _form = CoreUserCreationForm()

    context = {
            'form': _form,
            }
    return render(request, "core/create_account.html", context)
