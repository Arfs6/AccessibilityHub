from django.shortcuts import render

def home(request):
    """Renders the home page for Accessibility Hub."""
    context = {
            "title": "HOME | Accessibility Hub"
            }
    return render(request, "core/home.html", context)
