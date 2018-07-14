from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render

from .forms import addCompanyForm
from .forms import addProjectForm
import grakn

client = grakn.Client(uri='http://35.197.194.67:4567', keyspace='dsvgraph')

# Create your views here.

def index(request):
	return render(request, 'interface/index.html')
	# database access here

def allcompanies(request):
	graknData=client.execute('match $x isa company, has name $y; offset 0; limit 30; get $y;') # dictionaries are nested structures
	
	# itterate thought results and put into dict -don't know why cna't access dict in the teplate when can on the command line
	companies=[]
	for x in graknData:
		company={'name':x['y']['value'],'id':x['y']['id']}
		companies.append(company)
	#graknData[0]['y']['value']

	context = {'graknData': companies}
	return render(request, 'interface/viewall.html', context)
	# database access here	

def addcompany(request):
	action = 'addcompany'
	if request.method == 'POST':
		form = addCompanyForm(data=request.POST) 
		if form.is_valid():

			print(form.cleaned_data)
			companyName = form.cleaned_data['companyName']
			print(companyName)

	else:
		form = 	addCompanyForm() 
		
	return render(request, 'interface/addentity.html', {'form': form, 'action': action})


def addproject(request):
	action = 'addproject'
	if request.method == 'POST':
		form = addProjectForm(data=request.POST) 
		if form.is_valid():

			print(form.cleaned_data)
			projectName = form.cleaned_data['projectName']
			print(projectName)

	else:
		form = 	addProjectForm() 
		
	return render(request, 'interface/addentity.html', {'form': form, 'action': action})	



