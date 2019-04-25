from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models

from datetime import datetime

from . import utility


class PlayerManager(UserManager):
    pass


class Player(AbstractUser):
    """
    Player extension wrapper for the user
    """
    class Meta:
        verbose_name = 'Player'
        verbose_name_plural = 'Players'

    cash = models.IntegerField(default=1000)

    objects = PlayerManager()

    def __str__(self):
        return self.username


class Trait(models.Model):
    """
    Combat traits for the battlecats
    """

    def __str__(self):
        return self.name

    name = models.CharField(max_length=100)
    desc = models.TextField()

    objects = models.Manager()


class Breed(models.Model):
    """
    A battlecat breed
    """

    slug = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    stats = models.TextField()

    objects = models.Manager


class Battlecat(models.Model):
    """
    General battlecat model
    """

    # Basics
    name = models.CharField(max_length=100, unique=True)
    image = models.CharField(max_length=1000, unique=True)
    image_id = models.CharField(max_length=20, default='')
    breed = models.CharField(max_length=100, default='')

    # Individual stats
    strength = models.IntegerField()
    agility = models.IntegerField()
    cunning = models.IntegerField()
    defense = models.IntegerField()

    # Traits
    traits = models.ManyToManyField(Trait, blank=True, null=True)

    # Records
    wins = models.IntegerField()
    losses = models.IntegerField()
    debut = models.DateField()
    retired = models.DateField(blank=True, null=True)

    objects = models.Manager()

    @classmethod
    def create(cls):
        """
        Create a new random Battlecat
        :return:
        """

        name = utility.random_name()

        while Battlecat.objects.filter(name=name).count():
            name = utility.random_name()

        breed = Breed.objects.all().order_by('?').first().slug

        image, image_id = utility.random_image(breed)

        while Battlecat.objects.filter(image=image).count():
            name = utility.random_image(breed)

        stats = utility.random_stats()

        battlecat = Battlecat(name=name, breed=breed, image=image, image_id=image_id,
                              strength=stats['strength'], agility=stats['agility'],
                              cunning=stats['cunning'], defense=stats['defense'],
                              wins=0, losses=0, debut=datetime.today())

        battlecat.save()

        for trait in utility.generate_traits():
            battlecat.traits.add(trait)

        battlecat.save()

        return battlecat

    def power_level(self):
        """
        Return the combined power level of a Zirecat
        :return:
        """

        power = 0

        power += self.strength
        power += self.agility
        power += self.cunning
        power += self.defense

        return power

    def on_deck(self):
        """
        Check if a Battlecat is on deck for a match
        :return: true/false
        """

        in_match = False

        for match in Match.objects.filter(time__isnull=True):
            if self.pk == match.a.pk or self.pk == match.b.pk:
                in_match = True
                break

        return in_match

    def add_trait(self, trait):
        """
        Add a trait to a battlecat
        :param trait: trait to be added
        :return:
        """

        if trait not in self.traits.all():
            self.traits.add(trait)


class Match(models.Model):
    """
    A matchup of two battlecats
    """

    a = models.ForeignKey(Battlecat, on_delete=models.CASCADE, related_name='a')
    b = models.ForeignKey(Battlecat, on_delete=models.CASCADE, related_name='b')

    winner = models.ForeignKey(Battlecat, blank=True, null=True, on_delete=models.CASCADE)
    time = models.DateTimeField(blank=True, null=True)

    @classmethod
    def create(cls):
        """
        Create a new match between random battlecats
        :return: new match object
        """

        active_battlecats = Battlecat.objects.filter(retired__isnull=True)

        if active_battlecats.count() < 2:
            print('Failed to create match: not enough battlecats!')
            return False

        a = active_battlecats.order_by('?').first()

        while a.on_deck():
            a = active_battlecats.order_by('?').first()

        b = active_battlecats.order_by('?').first()

        while b == a or b.on_deck():
            b = active_battlecats.order_by('?').first()

        match = Match(a=a, b=b)
        match.save()

        return match

    def get_battlecats(self):
        """
        Return a list of the two battlecats in a match
        :return: [battlecat, battlecat]
        """

        battlecats = [self.a, self.b]

        return battlecats

    objects = models.Manager()
