from  django.urls import path

from . import views

app_name = 'applications'
urlpatterns = [
    path('new-application', views.newApplications, name='new-application'),
    path('crate-application', views.createApplication),
    path('new-form', views.newForm, name='new-form'),
]