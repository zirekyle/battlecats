from django.core.management.base import BaseCommand

from main import models

import os
import requests


class Command(BaseCommand):
    help = 'Import battlecat breed information to the database'

    def handle(self, *args, **options):

        all_breeds = requests.get('https://api.thecatapi.com/v1/breeds',
                                  headers={'x-api-key': os.environ.get('THECATAPI_KEY')}).json()

        for breed in all_breeds:

            # print('Name: {}'.format(breed['name']))
            # print('Stats: {}'.format(breed))

            if not models.Breed.objects.filter(slug=breed['id']).count():
                print('New breed: {}'.format(breed['name']))
                b = models.Breed(name=breed['name'], slug=breed['id'], stats=breed)
                b.save()
