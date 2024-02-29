from urllib.parse import unquote
from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, HttpResponse, Http404, QueryDict
from django.views.decorators.http import require_http_methods

from .forms import ReviewForm, OwnerForm
from .models import Tool, Owner, Review
from utils import base362Decimal


def index(request: HttpRequest) -> HttpResponse:
    """Index page for reviews.
    Should make finding tools easier.
    """
    tools = Tool.allVerified().all()
    context = {
        "tools": tools,
    }
    return render(request, "reviews/index.html", context)


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
        "owner": owner,
        "tools": owner.tools.filter(verified=True).all(),
    }
    return render(request, "reviews/owner.html", context)


@require_http_methods(['GET', 'POST', 'PUT'])
def tool(request: HttpRequest, ownerBase36Id: str, toolSlug: str) -> HttpResponse:
    """Displays a tool and it's reviews if any.
    parameters:
    - request: request object passed by django.
    - slug: slug name of tool, gotten from url.
    """
    try:
        owner = Owner.allVerified().get(pk=base362Decimal(ownerBase36Id))
    except Owner.DoesNotExist:
        raise Http404(f"Owner with id <{ownerBase36Id}> could not be found.")
    tool = get_object_or_404(owner.tools, slug=toolSlug, verified=True)
    userReview = Review.objects.filter(tool=tool, user=request.user).first() if request.user.is_authenticated else None
    if request.method == "GET":
        form = None
        if request.user.is_authenticated:
            # display form for editing / creating reviews.
            form = ReviewForm(instance=userReview) if userReview else ReviewForm()
    elif request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.instance.tool = tool
            form.instance.user = request.user
            form.save()
    else:  # Put method
        if userReview is None:
            raise Http404("Cannot find review to update.")
        data = QueryDict(request.body)
        form = ReviewForm(data, instance=userReview)
        if form.is_valid():
            form.save()
    return render(request, "reviews/tool.html", context={
        "owner": owner,
        "tool": tool,
        "reviews": tool.reviews.exclude(comment='').all(),
        "form": form,
        "formInstanceState": form.instance._state if form is not None else None,
    })


def newTool(request: HttpRequest) -> HttpResponse:
    """This view allows a user to request for creation of new tools to be reviewd."""
    form = OwnerForm()
    context = {
        "title": "Request New Tool",
        "form": form,
    }
    return render(request, "reviews/new_tool.html", context)


def userReview(request: HttpRequest, ownerBase36Id: str, toolSlug: str, userId: int):
    """A user's review.
    Parameters:
    - ownerBase36Id: The base 36 id of an owner
    - toolSlug: The slug of a tool owned by @owner.
    - userId: Id of a user.
    """


@require_http_methods(["GET"])
def search(request: HttpRequest) -> HttpResponse:
    """Search view.
    """
    if request.GET.get('searchTerm') is None:
        return HttpResponse("Search term not provided.".encode(), status=400)
    tools = Tool.objects.filter(name__icontains=request.GET['searchTerm']).all()
    return render(request, "reviews/search.html", {
        "tools": tools,
    })
