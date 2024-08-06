from django.urls import path
from hh_parser import views

app_name = 'hh_parser'

urlpatterns = [
    path('', views.IndexListView.as_view(), name='index'),
    path('form/', views.form, name='form'),
    path('contacts/', views.ContactsTemplateView.as_view(), name='contacts'),
    path('results/<str:vacancy>/<str:city>/', views.results, name='results')
]
