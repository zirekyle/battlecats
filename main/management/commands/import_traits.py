from django.core.management.base import BaseCommand
from bs4 import BeautifulSoup

import re
import requests

from main import models


def strip_bad_apostrophe(string):
    """
    Strip bad apostrophes from strings
    :return: stripped string
    """

    new_string = ''

    for character in string:
        if ord(character) == 226:
            new_string += chr(39)
            continue
        elif ord(character) == 128 or ord(character) == 153:
            continue
        else:
            new_string += character
            continue

    return new_string


class Command(BaseCommand):
    help = 'Import battlecat trait information to the database'

    def handle(self, *args, **options):

        trait_list_url = 'http://www.d20pfsrd.com/traits/combat-traits/'

        regex = re.compile('[+]')

        main_list = BeautifulSoup(requests.get(trait_list_url).text, 'html.parser')

        trait_pages = main_list.find_all('li', {'class': 'page'})

        for trait_page in trait_pages:

            trait_name = trait_page.get_text()

            trait_name = trait_name.split('(')[0].strip() if '(' in trait_name else trait_name

            trait_url = trait_page.find('a').get('href')

            try:

                desc = BeautifulSoup(
                    requests.get(trait_url).text, 'html.parser').find_all(
                    'p', {'class': 'description'})[0].get_text()

            except IndexError:
                desc = ''

            if regex.search(desc):
                continue

            desc = desc.replace('Your', 'Their').replace('your', 'their').replace('you', 'them').replace('You', 'They')

            trait_name = strip_bad_apostrophe(trait_name)
            desc = strip_bad_apostrophe(desc)

            if desc and not models.Trait.objects.filter(name=trait_name).count():
                trait = models.Trait(name=trait_name, desc=desc)
                trait.save()

