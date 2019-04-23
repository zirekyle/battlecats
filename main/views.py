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


def random_zirecats(request, count=2):
    """
    Return a random list of battlecats
    :param request: request object
    :param count: number of battlecats to return
    :return: rendered response
    """

    zirecats = []

    for x in range(0, count):

        zirecat = models.Zirecat.objects.order_by("?").first()

        while zirecat in zirecats:
            zirecat = models.Zirecat.objects.order_by("?").first()

        zirecats.append(zirecat)

    width = (100 / count)

    return render(request, 'showdown.html', {'battlecats': zirecats, 'width': width})
