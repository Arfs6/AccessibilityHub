from django.http import Http404, HttpRequest, HttpResponse, HttpResponseBadRequest, QueryDict
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_http_methods

from .forms import OwnerForm, ReviewForm
from .models import Owner, Review, Tool


def index(request: HttpRequest) -> HttpResponse:
    """Index page for reviews.
    Should make finding tools easier.
    """
    tools = Tool.allVerified().all()
    context = {
        'tools': tools,
    }
    return render(request, 'reviews/index.html', context)


def owner(request: HttpRequest, base36Id: str) -> HttpResponse:
    """Displays the owner's page.
    parameters:
    - request: request object passed by django.
    - base36Id: id of owner converted to base36.
    """
    try:
        owner = Owner.allVerified().get(pk=int(base36Id, 36))
    except Owner.DoesNotExist as error:
        errorMsg = f'Owner with id <{base36Id}> not found.'
        raise Http404(errorMsg) from error
    context = {
        'owner': owner,
        'tools': owner.tools.filter(verified=True).all(),
    }
    return render(request, 'reviews/owner.html', context)


@require_http_methods(['GET', 'POST', 'PUT'])
def tool(request: HttpRequest, ownerBase36Id: str, toolSlug: str) -> HttpResponse:
    """Displays a tool and it's reviews if any.
    parameters:
    - request: request object passed by django.
    - slug: slug name of tool, gotten from url.
    """
    try:
        owner = Owner.allVerified().get(pk=int(ownerBase36Id, 36))
    except Owner.DoesNotExist as error:
        errorMsg = f'Owner with id <{ownerBase36Id}> could not be found.'
        raise Http404(errorMsg) from error
    tool = get_object_or_404(owner.tools, slug=toolSlug, verified=True)
    userReview = Review.objects.filter(tool=tool, user=request.user).first() if request.user.is_authenticated else None
    if request.method == 'GET':
        form = None
        if request.user.is_authenticated:
            # display form for editing / creating reviews.
            form = ReviewForm(instance=userReview) if userReview else ReviewForm()
    elif request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.instance.tool = tool
            form.instance.user = request.user
            form.save()
    else:  # Put method
        if userReview is None:
            errorMsg = 'Cannot find review to update.'
            raise Http404(errorMsg)
        data = QueryDict(request.body)
        form = ReviewForm(data, instance=userReview)
        if form.is_valid():
            form.save()
    return render(
        request,
        'reviews/tool.html',
        context={
            'owner': owner,
            'tool': tool,
            'reviews': tool.reviews.exclude(comment='').all(),
            'form': form,
            'userReview': userReview,
        },
    )


def newTool(request: HttpRequest) -> HttpResponse:
    """This view allows a user to request for creation of new tools to be reviewd."""
    form = OwnerForm()
    context = {
        'title': 'Request New Tool',
        'form': form,
    }
    return render(request, 'reviews/new_tool.html', context)


@require_http_methods(['GET'])
def search(request: HttpRequest) -> HttpResponse:
    """Search view."""
    if request.GET.get('searchTerm') is None:
        return HttpResponseBadRequest(b'Search term not provided.')
    tools = Tool.objects.filter(name__icontains=request.GET['searchTerm']).all()
    return render(
        request,
        'reviews/search.html',
        {
            'tools': tools,
        },
    )
