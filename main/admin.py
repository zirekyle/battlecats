from . import models
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


class BattlecatAdmin(admin.ModelAdmin):
    list_display = ('name', 'wins', 'losses')
    ordering = ['name']


class BreedAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    ordering = ['name']


class TraitAdmin(admin.ModelAdmin):
    list_display = ('name', 'desc')
    ordering = ['name']


admin.site.register(models.Battlecat, BattlecatAdmin)
admin.site.register(models.Breed, BreedAdmin)
admin.site.register(models.Trait, TraitAdmin)
