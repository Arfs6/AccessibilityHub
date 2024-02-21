from django.http import HttpRequest


def setBaseTemplate(request: HttpRequest) -> dict[str, str]:
    """Sets the baseTemplate context variable.
    Parameters:
    - request: Request object.
    Returns:
    - dict: A dictionary that sets either '_base.html' or '_partial.html' as the basetemplate.
    """
    baseTemplate = '_partial.html' if request.htmx else '_base.html'
    return {'baseTemplate': baseTemplate}
