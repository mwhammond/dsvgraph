from django.urls import path
from django.contrib import admin

from . import views

urlpatterns = [
#/ main panel
path('', views.index, name='index'),
# add a company
path('addcompany', views.addcompany, name='Add Company'),
# all companies
path('addproject', views.addproject, name='Add Project'),
# all companies
]

