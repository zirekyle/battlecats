# Utility functions

import ast
import os
import requests
import random

from bs4 import BeautifulSoup

from . import models
from .resources.temp_db import temp_db


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


def random_image(breed):

    api_key = os.environ.get('THECATAPI_KEY')

    url = 'https://api.thecatapi.com/v1/images/search?size=thumb&mime_types=jpg,png&breed_id={}'.format(breed.slug)

    json = requests.get(url, headers={'x-api-key': api_key}).json()[0]

    image = json['url']
    image_id = json['id']

    return image, image_id


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


def generate_traits():
    """
    Generate semi-random traits for a battlecat
    :return: list of trait objects
    """

    trait_list = []

    for count, trait in enumerate(models.Trait.objects.all().order_by('?')):

        if count == 0:
            threshold = 1

        elif count == 1:
            threshold = 25

        elif count == 2:
            threshold = 75

        else:
            break

        if random.randrange(1, 101) > threshold:
            trait_list.append(trait)

    return trait_list


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


def apply_temperament_modifiers(stats, temperaments):
    """
    Apply temperament modifiers to existing stats
    :param stats: current stats
    :param temperaments: list of temperaments
    :return: resultant stats
    """

    for temperament in temperaments:

        if temperament.capitalize() in temp_db.keys():
            stats[temp_db[temperament]['stat']] += temp_db[temperament]['modifier']
            print('Temperament bonus: {}: {} {}'.format(temperament, temp_db[temperament]['modifier'], temp_db[temperament]['stat']))

    return stats


def apply_breed_modifiers(stats, breed):
    """
    Apply breed modifiers to existing stats
    :param stats: current stats of the battlecat
    :param breed: breed of the battlecat
    :return: resultant stats of the battlecat
    """

    bs = ast.literal_eval(breed.stats)

    # weight({'imperial': '7  -  10', 'metric': '3 - 5'})

    weight = bs['weight']['imperial'].split(' - ')
    weight = (weight[0] + weight[1]) / 2

    stats['strength'] += (5 * weight)
    stats['defense'] += (5 * weight)
    stats['agility'] -= (2.5 * weight)

    # temperament(Active, Energetic, Independent, Intelligent, Gentle)
    # origin(Egypt)
    # country_codes(EG)
    # country_code(EG)
    # life_span(14 - 15)
    # indoor(0)
    # lap(1)
    # alt_names()
    # adaptability(5)
    # affection_level(5)
    # child_friendly(3)
    # dog_friendly(4)
    # energy_level(5)
    # grooming(1)
    # health_issues(2)
    # intelligence(5)
    # shedding_level(2)
    # social_needs(5)
    # stranger_friendly(5)
    # vocalisation(1)
    # experimental(0)
    # hairless(0)
    # natural(1)
    # rare(0)
    # rex(0)
    # suppressed_tail(0)
    # short_legs(0)
    # wikipedia_url(https: // en.wikipedia.org / wiki / Abyssinian_(cat))
    # hypoallergenic(0)




