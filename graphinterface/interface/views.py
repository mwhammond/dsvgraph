from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
import grakn

client = grakn.Client(uri='http://localhost:4567', keyspace='dsvgraph')

# Create your views here.

def index(request):
	graknData=client.execute('match $x isa company')
	companyName=graknData[0]["name"]["value"] # dictionaries are nested structures
	context = {'graknData': companyName}
	return render(request, 'interface/index.html', context)
	# database access here

def addcompany(request):
	return render(request, 'interface/addcompany.html')

def allcompanies(request):
	return HttpResponse("All the companies")


def addbusinessmodel(request):	
	return HttpResponse("Add a business model")