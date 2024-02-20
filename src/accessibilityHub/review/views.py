from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, HttpResponse, Http404

from .forms import ReviewForm, OwnerForm
from .models import Tool, Owner, Review
from utils import base362Decimal


def index(request: HttpRequest) -> HttpResponse:
    """Index page for reviews.
    Should make finding tools easier.
    """
    tools = Tool.allVerified().all()
    context = {
            'tools': tools,
            }
    return render(request, 'review/index.html', context)


def owner(request: HttpRequest, base36Id: str) -> HttpResponse:
    """Displays the owner's page.
    parameters:
    - request: request object passed by django.
    - base36Id: id of owner converted to base36.
    """
    try:
        owner = Owner.allVerified().get(pk=base362Decimal(base36Id))
    except Owner.DoesNotExist:
        raise Http404(f"Owner with id <{base36Id}> not found.")
    context = {
            'owner': owner,
            'tools': owner.tools.filter(verified=True).all(),
            }
    return render(request, 'review/owner.html', context)


def tool(request: HttpRequest, ownerBase36Id: str, slug: str) -> HttpResponse:
    """Displays a tool and it's reviews if any.
    parameters:
    - request: request object passed by django.
    - slug: slug name of tool, gotten from url.
    """
    try:
        owner = Owner.allVerified().get(pk=base362Decimal(ownerBase36Id))
    except Owner.DoesNotExist:
        raise Http404(f"Owner with id <{ownerBase36Id}> could not be found.")
    tool = get_object_or_404(owner.tools, slug=slug, verified=True)
    if request.user.is_authenticated:
        # display form for editing / creating review.
        initial = {'userId': request.user.id}
        userReview = Review.objects.filter(tool=tool, user=request.user).first()
        if userReview:
            initial['rating'] = userReview.rating
            initial['comment'] = userReview.comment if userReview.comment else ''
        form = ReviewForm(initial=initial)
    else:
        form = None
    context = {
            'owner': owner,
            'tool': tool,
            'reviews': tool.reviews.all(),
        'form': form,
            }
    return render(request, 'review/tool.html', context)


def newTool(request: HttpRequest) -> HttpResponse:
    """This view allows a user to request for creation of new tools to be reviewd.
    """
    form = OwnerForm()
    context = {
        'title': 'Request New Tool',
        'form': form,
    }
    return render(request, "review/new_tool.html", context)
