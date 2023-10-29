from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, HttpResponse

from .models import Tool, Owner
from utils import base362Decimal


def index(request: HttpRequest) -> HttpResponse:
    """Index page for reviews.
    Should make finding tools easier.
    """
    tools = Tool.objects.all()
    context = {
            'tools': tools,
            }
    return render(request, 'review/index.html', context)


def owner(request: HttpRequest, slug: str, base36Id: str) -> HttpResponse:
    """Displays the owner's page.
    parameters:
    - request: request object passed by django.
    - slug: slug gotten from url, representing the owner's name.'
    - base36Id: id of owner converted to base36.
    """
    owner = get_object_or_404(Owner, pk=base362Decimal(base36Id), slug=slug)
    context = {
            'owner': owner,
            'tools': owner.tools.all(),
            }
    return render(request, 'review/owner.html', context)


def tool(request: HttpRequest, ownerSlug: str, ownerBase36Id: str, slug: str) -> HttpResponse:
    """Displays a tool and it's reviews if any.
    parameters:
    - request: request object passed by django.
    - slug: slug name of tool, gotten from url.
    """
    owner = get_object_or_404(Owner, pk=base362Decimal(ownerBase36Id), slug=ownerSlug)
    print(owner)
    tool = get_object_or_404(owner.tools, slug=slug)
    context = {
            'owner': owner,
            'tool': tool,
            'reviews': tool.reviews.all(),
            }
    return render(request, 'review/tool.html', context)
