from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render

from .forms import addCompanyForm
from .forms import addProjectForm
from .forms import addTechnologyForm
from .forms import addBusinessModelForm
from .forms import addMarketForm

import grakn
import uuid

client = grakn.Client(uri='http://35.197.194.67:4567', keyspace='dsvgraph')

# Create your views here.

def index(request):
	return render(request, 'interface/index.html')
	# database access here

def allcompanies(request):
	graknData=client.execute('match $x isa company, has name $y, has identifier $z; get $y,$z;') # dictionaries are nested structures
	
	# itterate thought results and put into dict -don't know why cna't access dict in the teplate when can on the command line
	companies=[]
	for entry in graknData:
		company={'name':entry['y']['value'],'id':entry['z']['value']}
		companies.append(company)

	context = {'graknData': companies, 'title': 'All Companies'}
	return render(request, 'interface/viewall.html', context)
	# database access here	



def allprojects(request):
	graknData=client.execute('match $x isa product, has name $y, has identifier $z; get $y,$z;') # dictionaries are nested structures
	
	# itterate thought results and put into dict -don't know why cna't access dict in the teplate when can on the command line
	projects=[]
	for x in graknData:
		project={'name':x['y']['value'],'id':x['z']['value']}
		projects.append(project)

	context = {'graknData': projects,'title': 'All Projects'}
	return render(request, 'interface/viewall.html', context)
	# database access here	



def allbusinessmodels(request):
	graknData=client.execute('match $x isa businessmodel, has name $y, has identifier $z; get $y, $z;') # dictionaries are nested structures
	
	# itterate thought results and put into dict -don't know why cna't access dict in the teplate when can on the command line
	allentities=[]
	for x in graknData:
		singleentity={'name':x['y']['value'],'id':x['z']['value']}
		allentities.append(singleentity)

	context = {'graknData': allentities,'title': 'All Business Models'}
	return render(request, 'interface/viewall.html', context)
	# database access here		


def allmarkets(request):
	graknData=client.execute('match $x isa market, has name $y, has identifier $z; get $y,$z;') # dictionaries are nested structures
	
	# itterate thought results and put into dict -don't know why cna't access dict in the teplate when can on the command line
	allentities=[]
	for x in graknData:
		singleentity={'name':x['y']['value'],'id':x['z']['value']}
		allentities.append(singleentity)

	context = {'graknData': allentities,'title': 'All Markets'}
	return render(request, 'interface/viewall.html', context)
	# database access here	


def alltechnologies(request):
	graknData=client.execute('match $x isa technology, has name $y, has identifier $z; get $y,$z;') # dictionaries are nested structures
	
	# itterate thought results and put into dict -don't know why cna't access dict in the teplate when can on the command line
	allentities=[]
	for x in graknData:
		singleentity={'name':x['y']['value'],'id':x['z']['value']}
		allentities.append(singleentity)

	context = {'graknData': allentities,'title': 'All Technolgies'}
	return render(request, 'interface/viewall.html', context)
	# database access here		



def addcompany(request):
	action = 'addcompany'
	print("made it to add company")
	if request.method == 'POST':
		form = addCompanyForm(data=request.POST) 
		print("recognised as post")
		if form.is_valid():
			print("form is valid")
			print(form.cleaned_data)
			name = form.cleaned_data['name']
			summary = form.cleaned_data['summary']
			protocompany = form.cleaned_data['protocompany'] #NOT CURRENTLY USED
			marketchoice = form.cleaned_data['marketchoice']
			identifier = str(uuid.uuid4())
			client.execute('insert $x isa company, has name "' +name+'", has summary "' +summary+'", has identifier "' +identifier+'";')

	else:
		print("new form")
		form = 	addCompanyForm() 
		
	return render(request, 'interface/addentity.html', {'form': form, 'action': action})


def addproject(request):
	action = 'addproject'
	if request.method == 'POST':
		form = addProjectForm(data=request.POST) 
		if form.is_valid():

			name = form.cleaned_data['name']
			summary = form.cleaned_data['summary']
			technologychoice = form.cleaned_data['technologychoice']
			companychoice = form.cleaned_data['companychoice']
			marketchoice = form.cleaned_data['marketchoice']

			identifier = str(uuid.uuid4())
			client.execute('insert $x isa product, has name "' +name+'", has summary "' +summary+'", has identifier "' +identifier+'";')

	else:
		form = 	addProjectForm() 
		
	return render(request, 'interface/addentity.html', {'form': form, 'action': action})	



# business model
def addbusinessmodel(request):
	action = 'addbusinessmodel'
	if request.method == 'POST':
		form = addBusinessModelForm(data=request.POST) 
		if form.is_valid():

			name = form.cleaned_data['name']
			summary = form.cleaned_data['summary']
			top = form.cleaned_data['top']

			identifier = str(uuid.uuid4())
			client.execute('insert $x isa businessmodel, has name "' +name+'", has summary "' +summary+'", has identifier "' +identifier+'";')


	else:
		form = addBusinessModelForm() 
		
	return render(request, 'interface/addentity.html', {'form': form, 'action': action})


# market


def addmarket(request):
	action = 'addmarket'
	if request.method == 'POST':
		form = addMarketForm(data=request.POST) 
		if form.is_valid():

			name = form.cleaned_data['name']
			summary = form.cleaned_data['summary']
			top = form.cleaned_data['top']

			identifier = str(uuid.uuid4())
			client.execute('insert $x isa market, has name "' +name+'", has summary "' +summary+'", has identifier "' +identifier+'";')


	else:
		form = addMarketForm() 
		
	return render(request, 'interface/addentity.html', {'form': form, 'action': action})


# technology

def addtechnology(request):
	action = 'addtechnology'
	if request.method == 'POST':
		form = addTechnologyForm(data=request.POST) 
		if form.is_valid():

			name = form.cleaned_data['name']
			summary = form.cleaned_data['summary']
			top = form.cleaned_data['top']

			identifier = str(uuid.uuid4())
			client.execute('insert $x isa technology, has name "' +name+'", has summary "' +summary+'", has identifier "' +identifier+'";')


	else:
		form = addTechnologyForm() 
		
	return render(request, 'interface/addentity.html', {'form': form, 'action': action})


def deleteentity(request):
	if request.method=='GET':
		identifier = request.GET.get('id')
		print("deleting: ", id)
		client.execute('match $y has identifier"'+identifier+'"; delete $y;')

		# need some error handling!
	return render(request, 'interface/index.html')
		

# people

# development strategy

# defensibility strategy

# Funding strategy
