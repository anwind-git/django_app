from django.urls import path
from .views import *

app_name = 'myapp'

urlpatterns = [
    path('', index),
    path('about', about, name='about')
]
