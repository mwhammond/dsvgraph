from django.urls import path
from django.contrib import admin

from . import views

urlpatterns = [
#/ main panel
path('', views.index, name='index'),
path('addcompany', views.addcompany, name='Add Company'),
path('addproject', views.addproject, name='Add Project'),
path('allcompanies', views.allcompanies, name='All Companies'),
path('allprojects', views.allprojects, name='All Projects'),
path('allbusinessmodels', views.allbusinessmodels, name='All Business Models'),
path('allmarkets', views.allmarkets, name='All Markets'),
path('alltechnologies', views.alltechnologies, name='All Technologies'),
path('addtechnology', views.addtechnology, name='Add Technology'),
path('addbusinessmodel', views.addbusinessmodel, name='Add Business Model'),
path('addmarket', views.addmarket, name='Add Market'),
path('deleteentity', views.deleteentity, name='Delete Entity'),

]

