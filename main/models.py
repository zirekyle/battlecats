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


class Battlecat(models.Model):
    """
    General battlecat model
    """

    # Basics
    name = models.CharField(max_length=100, unique=True)
    image = models.CharField(max_length=1000, unique=True)

    # Individual stats
    strength = models.IntegerField()
    agility = models.IntegerField()
    cunning = models.IntegerField()
    defense = models.IntegerField()

    # Abilities
    abilities = models.ManyToManyField('Ability', blank=True)

    # Records
    wins = models.IntegerField()
    losses = models.IntegerField()
    debut = models.DateField()
    retired = models.DateField(blank=True, null=True)

    objects = models.Manager()

    @classmethod
    def create(cls):
        """
        Create a new random Zirecat
        :return:
        """

        name = utility.random_name()

        while Battlecat.objects.filter(name=name).count():
            name = utility.random_name()

        image = utility.random_image()

        while Battlecat.objects.filter(image=image).count():
            name = utility.random_image()

        stats = utility.random_stats()

        battlecat = Battlecat(name=name, image=image,
                              strength=stats['strength'], agility=stats['agility'],
                              cunning=stats['cunning'], defense=stats['defense'],
                              wins=0, losses=0, debut=datetime.today())

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


class Ability(models.Model):
    """
    Combat abilities for the battlecats
    """

    styles = (
        ('MAGIC', 'Magic'),
        ('TECH', 'Tech'),
    )

    name = models.CharField(max_length=100)
    power = models.IntegerField()
    style = models.CharField(max_length=50, choices=styles)

    objects = models.Manager()


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
