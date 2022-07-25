from unicodedata import name
from  django.urls import path

from . import views

app_name = 'frontapp'
urlpatterns = [
    path('', views.index, name='index'),
    path('privacy', views.privacy, name='privacy'),
    path('terms', views.terms, name='terms'),
    path('create-new-account', views.register, name='create-new-account'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
]