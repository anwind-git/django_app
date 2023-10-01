from django.urls import path
from .views import *

app_name = 'myapp'

urlpatterns = [
    path('', ProductsHome.as_view(), name='myapp'),
    path('contacts', contacts, name='contacts'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('registration/', RegisterUser.as_view(), name='registration'),
    path('category/<slug:cat_slug>/', ProductsCategory.as_view(), name='category'),
    path('edit/<int:pk>/', UserEdit.as_view(), name='edit_user'),
    path('profile/', OpenUser.as_view(), name='profile')
]
