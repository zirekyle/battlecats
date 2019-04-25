from django.core.management.base import BaseCommand

from main import models


class Command(BaseCommand):
    help = 'Generate a random temporary cat for testing'

    def handle(self, *args, **options):

        bc = models.Battlecat.create()

        print('')
        print('    Name: {}'.format(bc.name))
        print('   Image: {}'.format(bc.image))
        print('Image ID: {}'.format(bc.image_id))
        print('   Breed: {}'.format(bc.breed))
        print('')

        for trait in bc.traits.all():
            print('   Trait: {}'.format(trait))

        print('Strength: {}'.format(bc.strength))
        print(' Agility: {}'.format(bc.agility))
        print(' Cunning: {}'.format(bc.cunning))
        print(' Defense: {}'.format(bc.defense))
        print('')
        print('   POWER: {}'.format(bc.power_level()))
        print('')


