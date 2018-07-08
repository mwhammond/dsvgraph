from django.urls import path
from django.contrib import admin

from . import views

urlpatterns = [
#/ main panel
path('', views.index, name='index'),
# add a company
path('addcompany', views.addcompany, name='Add Company'),
# all companies
path('allcompanies', views.allcompanies, name='All Company'),
# add business model
path('addbusinessmodel', views.addbusinessmodel, name='Add Business model'),


]

