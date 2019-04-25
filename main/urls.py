# from django.contrib import_tool admin
from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

urlpatterns = [
    path('traits/', views.list_all_traits),
    path('', views.index, name='index'),
]

urlpatterns += staticfiles_urlpatterns()
