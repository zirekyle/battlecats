from django.core.management.base import BaseCommand

from main import models


class Command(BaseCommand):
    help = 'Checks for duplicate names or images'

    def handle(self, *args, **options):

        names = []
        images = []

        for cat in models.Battlecat.objects.all():

            if cat.name in names:
                print('Duplicate Name: {}'.format(cat.name))

            else:
                names.append(cat.name)

            if cat.image in images:
                print('Duplicate Image: {}'.format(cat.image))

            else:
                images.append(cat.image)

