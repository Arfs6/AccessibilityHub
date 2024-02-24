from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, HttpResponse, HttpResponseNotAllowed
from django.contrib.auth.models import User

from reviews.forms import ReviewForm, OwnerForm, ToolForm
from reviews.models import Review, Tool, Owner


def createReview(request: HttpRequest, toolId: int) -> HttpResponse:
    """Creates a new review from a form.
    parameters:
    request: request object passed by django
    - toolId: The id of the tool being reviewed.
    """
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    form = ReviewForm(request.POST)
    tool = get_object_or_404(Tool, pk=toolId)
    if form.is_bound and form.is_valid():
        data = form.cleaned_data
        review = get_object_or_404(Review, tool=tool)
        review.rating = data['rating']
        review.comment = data['comment']
        review.user = get_object_or_404(User, pk=data['userId'])
        review.tool = tool
        review.save()

    context = {
        'form': form,
        'tool': tool,
    }
    return render(request, 'api/review_form.html', context)


def newOwner(request: HttpRequest) -> HttpResponse:
    """Verifies form for creation of owner and returns a form for creating tool."""
    if request.method != "POST":
        return HttpResponseNotAllowed(['POST'])

    form = OwnerForm(request.POST)
    if form.is_valid():
        data = form.cleaned_data
        initial = {
            'ownerName': data['name'],
            'ownerDescription': data['description'],
            'ownerUrl': data['url'],
        }
        newForm = ToolForm(initial=initial)
        context = dict(form=newForm)
        return render(request, 'api/new_tool_form.html', context)

    context = dict(form=form)
    return render(request, 'api/new_owner_form.html', context=context)


def newTool(request: HttpRequest) -> HttpResponse:
    """Creation of tools."""
    if request.method != "POST":
        return HttpResponseNotAllowed(['POST'])

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
        return render(request, 'api/new_tool_success.html')

    context = dict(form=form)
    return render(request, 'api/new_tool_form.html', context=context)
