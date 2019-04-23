# from django.contrib import_tool admin
from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

urlpatterns = [
    path('random_zirecats/<int:count>', views.random_zirecats),

    path('', views.index, name='index'),
]

urlpatterns += staticfiles_urlpatterns()
