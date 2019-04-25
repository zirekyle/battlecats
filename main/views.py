from django.shortcuts import render

from . import models
from . import utility

# Create your views here.


def index(request):
    """
    Main index page
    :param request: request object
    :return: response
    """

    matches = []
    values = [100, 500]

    maximum_matches = 3
    count = 0

    utility.fill_matches(reset=True)

    for match in models.Match.objects.filter(time__isnull=True):
        if count < maximum_matches:
            matches.append(match)
            count += 1

        if count >= maximum_matches:
            break

    return render(request, 'index.html', {'matches': matches, 'values': values})


def list_all_traits(request):
    """
    List all traits and their descriptions
    :param request: request object
    :return: response
    """

    all_traits = models.Trait.objects.all().order_by('name')

    return render(request, 'all_traits.html', {'all_traits': all_traits})
