from django.urls import path
from . import api

urlpatterns = [
    path('', api.idea_list, name='idea_list'),
    path('create/', api.idea_create, name='idea_create'),
]