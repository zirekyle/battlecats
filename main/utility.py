# Utility functions

import requests
import random

from bs4 import BeautifulSoup

from . import models


def random_name(source=None):
    """
    Generate a random name from various random API sources
    :return: random name string
    """

    sources = ['uzby', 'randomname.de', 'uinames', 'yourpetname']

    if not source:
        source = random.choice(sources)

    if source == 'uzby':

        name = requests.get('https://uzby.com/api.php?min=3&max=15').text

    elif source == 'namey':

        name_type = random.choice(['type=surname', 'with_surname=false'])

        name = requests.get('https://namey.muffinlabs.com/name.json?count=1&{}&frequency=all'.format(name_type)).json()[0]

    elif source == 'randomname.de':

        names = requests.get('https://randomname.de/?format=json').json()[0]

        name = random.choice([names['firstname'], names['lastname']])

    elif source == 'uinames':

        names = requests.get('http://uinames.com/api/').json()

        name = random.choice([names['name'], names['surname']])

    elif source == 'yourpetname':

        names = [item.get_text() for item in BeautifulSoup(requests.get('https://yourpetname.com/').text, 'html.parser').find_all(
            'li', {'class': 'list-group-item'})]

        name = random.choice(names)

    else:

        name = 'Pepper'

    return name.title()


def random_image():
    name = requests.get('https://api.thecatapi.com/v1/images/search?size=small&mime_types=jpg',
                        headers={'x-api-key': '8424f1dc-6cb8-41d8-8962-532e902207a2'}).json()[0]['url']
    return name


def random_stats():
    """
    Generate randomized stats
    :return: random stats list
    """

    stats = {
        'strength': 0,
        'agility': 0,
        'cunning': 0,
        'defense': 0,
    }

    priority = ['strength', 'agility', 'cunning', 'defense']

    for n in range(1, 40):

        stat = random.choice(priority)

        stats[stat] += random.randrange(5, 10)

    return stats


def random_quote():
    quote = requests.get('https://api.kanye.rest/').json()[0]['quote']

    return quote


def fill_matches(reset=False):
    """
    Create new matches until the maximum allowed is reached
    :return: nothing
    """

    maximum = 5

    if reset:
        models.Match.objects.all().delete()

    while models.Match.objects.filter(time__isnull=True).count() < maximum:
        if not models.Match.create():
            print('Could not fill matches')
            return

