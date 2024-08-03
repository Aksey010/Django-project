from django.urls import path
from hh_parser import views

app_name = 'hh_parser'

urlpatterns = [
    path('', views.index, name='index'),
    path('form/', views.form, name='form'),
    path('contacts/', views.contacts, name='contacts'),
    path('results/<str:vacancy>/<str:city>/', views.results, name='results')
]
