from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django_htmx.http import HttpResponseClientRedirect

from .forms import CommentForm, TopicForm
from .models import Topic


@require_http_methods(['GET'])
def landing(request: HttpRequest) -> HttpResponse:
    """Discussions landing page."""
    return render(request, 'discussions/landing.html')


@require_http_methods(['GET', 'POST'])
@require_http_methods(['GET'])
def index(request: HttpRequest) -> HttpResponse:
    """Index page for discussions."""
    latestTopics = Topic.objects.all()[:5]
    return render(
        request,
        'discussions/index.html',
        {
            'latestTopics': latestTopics,
        },
    )


def newTopic(request: HttpRequest) -> HttpResponse:
    """View for creating topics."""
    if request.method == 'GET':
        form = TopicForm() if request.user.is_authenticated else None
    else:
        form = TopicForm(request.POST)
        if form.is_valid():
            form.instance.createdBy = request.user
            form.instance.save()
            return HttpResponseClientRedirect(reverse('discussions:topicPage', args=(form.instance.base36Id,)))
    return render(
        request,
        'discussions/newTopic.html',
        {
            'form': form,
        },
    )


@require_http_methods(['GET', 'POST'])
def topicPage(request: HttpRequest, base36Id: str) -> HttpResponse:
    """Displays a topic.
    Parameters:
    - base36Id: base 36 id of the topic.
    """
    form = CommentForm()
    topic = get_object_or_404(Topic, pk=int(base36Id, 36))
    if request.method == 'POST':
        _form = CommentForm(request.POST)
        if _form.is_valid():
            _form.instance.createdBy = request.user
            _form.instance.topic = topic
            _form.instance.save()
        else:
            form = _form  # Show the user the errors
    return render(
        request,
        'discussions/topic.html',
        {
            'topic': topic,
            'comments': topic.comments.all(),
            'form': form,
        },
    )


@require_http_methods(['GET'])
def search(request: HttpRequest) -> HttpResponse:
    """Searches for a topic."""
    if not request.GET.get('q'):
        return HttpResponse(b'Invalid query. Query must be a non-empty string.', status=400)
    topics = Topic.objects.filter(name__icontains=request.GET.get('q')).all()
    return render(
        request,
        'discussions/searchResults.html',
        {
            'topics': topics,
        },
    )
