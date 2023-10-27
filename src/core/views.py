from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import views as authViews
from django.contrib.auth.models import User

from .forms import CoreUserCreationForm

def home_page(request):
    """Renders the home page for Accessibility Hub."""
    context = {
            "title": "Home"
            }
    return render(request, "core/home_page.html", context)


class CoreLoginView(authViews.LoginView):
    """Extends auth login view."""
    template_name = 'core/login.html'

    def get_context_data(self, **kwargs):
        """Returns the context dictionary."""
        context = super().get_context_data(**kwargs)
        context['title'] = 'Login'
        return context


def createAccount(request):
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
            return HttpResponseRedirect("/")
    else:
        _form = CoreUserCreationForm()

    context = {
            "title": "Create Account",
            'form': _form,
            }
    return render(request, "core/create_account.html", context)
