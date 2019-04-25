from django.core.management.base import BaseCommand

import json
import requests

from main import models


class Command(BaseCommand):
    help = 'Import battlecat trait information to the database'

    def handle(self, *args, **options):

        trait_list_url = 'http://charred.herokuapp.com/traits'

        trait_list_json = json.loads(requests.get(trait_list_url).text)

        for trait_name, trait_values in trait_list_json.items():

            if trait_values['type'] == 'character' and 'restrict' not in trait_values.keys():
                trait = models.Trait(name=trait_name, desc='')
                trait.save()

