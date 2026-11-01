from django.http import (
    Http404,
    HttpRequest,
    HttpResponse,
    HttpResponseBadRequest,
    QueryDict,
)
from django.shortcuts import get_object_or_404, render
from django.views import View
from django.views.decorators.http import require_http_methods

from .forms import OwnerForm, ReviewForm, ToolForm
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


class NewOwnerAndTool(View):
    """Create an owner and a tool using a two-step form."""

    http_method_names = ('get', 'post')

    def get(self, request: HttpRequest) -> HttpResponse:
        """This is the starting point of owner and tool creation.
        It returns a form for owner creation.
        """
        form = OwnerForm()
        context = {
            'title': 'Request New Tool',
            'form': form,
            'formName': OwnerForm.__name__,
        }
        return render(request, 'reviews/new_tool.html', context)

    def post(self, request: HttpRequest) -> HttpResponse:
        """Handle the owner form or the tool form, based on `formName`."""
        formName = request.POST.get('formName')
        if formName == OwnerForm.__name__:
            return self.newOwner(request)
        if formName == ToolForm.__name__:
            return self.newTool(request)
        return HttpResponseBadRequest(f'Invalid `formName` field: {formName}'.encode())

    def newOwner(self, request: HttpRequest) -> HttpResponse:
        """Verifies form for creation of owner and returns a form for creating tool."""
        form = OwnerForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            initial = {
                'ownerName': data['name'],
                'ownerDescription': data['description'],
                'ownerUrl': data['url'],
            }
            newForm = ToolForm(initial=initial)
            context = {'form': newForm, 'formName': ToolForm.__name__}
            return render(request, 'reviews/new_tool_form.html', context)

        context = {'form': form, 'formName': OwnerForm.__name__}
        return render(request, 'reviews/new_owner_form.html', context=context)

    def newTool(self, request: HttpRequest) -> HttpResponse:
        """Verifies the form for creating tool.
        If form is valid, it creates a new tool and owner with the given data,
        and it returns a success message.
        """
        form = ToolForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            owner = Owner()
            owner.name = data['ownerName']
            owner.description = data['ownerDescription']
            owner.url = data['ownerUrl']
            owner.save()
            tool = Tool()
            tool.name = data['name']
            tool.description = data['description']
            tool.url = data['url']
            tool.owner_id = owner.id
            tool.save()
            return render(request, 'reviews/new_tool_success.html')

        # invalid form.
        context = {'form': form, 'formName': ToolForm.__name__}
        return render(request, 'reviews/new_tool_form.html', context=context)


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
