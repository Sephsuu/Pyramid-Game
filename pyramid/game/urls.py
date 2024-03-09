from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('validate/', views.validate, name='validate'),
    path('vote/', views.vote, name='vote'),
    path('results/', views.results, name='results'),
    path('vote_success/', views.vote_success, name='vote_success'),
]