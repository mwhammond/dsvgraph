from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render

from .forms import addCompanyForm
from .forms import addProjectForm
#import grakn

#client = grakn.Client(uri='http://localhost:4567', keyspace='dsvgraph')

# Create your views here.

def index(request):
	graknData=['1','2']	
	#graknData=client.execute('match $x isa company; get;')
	companyName=graknData # dictionaries are nested structures
	context = {'graknData': companyName}
	return render(request, 'interface/index.html', context)
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



