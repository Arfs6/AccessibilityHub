from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse, HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, render
from reviews.forms import ReviewForm
from reviews.models import Review, Tool


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
