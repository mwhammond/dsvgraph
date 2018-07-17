from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render

from .forms import addCompanyForm
from .forms import addProjectForm
from .forms import addTechnologyForm
from .forms import addBusinessModelForm
from .forms import addMarketForm
from .forms import addMarketNeedForm
from .forms import addRiskForm

from django.shortcuts import redirect, render

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

	context = {'graknData': companies, 'title': 'All Companies','link': 'addcompany'}
	return render(request, 'interface/viewall.html', context)
	# database access here	


def allrisk(request):
	graknData=client.execute('match $x isa risk, has name $y, has identifier $z; get $y,$z;') # dictionaries are nested structures
	
	# itterate thought results and put into dict -don't know why cna't access dict in the teplate when can on the command line
	risks=[]
	for entry in graknData:
		risk={'name':entry['y']['value'],'id':entry['z']['value']}
		risks.append(risk)

	context = {'graknData': risks, 'title': 'All Risks','link': 'addrisk'}
	return render(request, 'interface/viewall.html', context)
	# database access here	


def allprojects(request):
	graknData=client.execute('match $x isa product, has name $y, has identifier $z; get $y,$z;') # dictionaries are nested structures
	
	# itterate thought results and put into dict -don't know why cna't access dict in the teplate when can on the command line
	projects=[]
	for x in graknData:
		project={'name':x['y']['value'],'id':x['z']['value']}
		projects.append(project)

	context = {'graknData': projects,'title': 'All Projects','link': 'addproject'}
	return render(request, 'interface/viewall.html', context)
	# database access here	



def allbusinessmodels(request):
	graknData=client.execute('match $x isa businessmodel, has name $y, has identifier $z; get $y, $z;') # dictionaries are nested structures
	
	# itterate thought results and put into dict -don't know why cna't access dict in the teplate when can on the command line
	allentities=[]
	for x in graknData:
		singleentity={'name':x['y']['value'],'id':x['z']['value']}
		allentities.append(singleentity)

	context = {'graknData': allentities,'title': 'All Business Models','link': 'addbusinessmodel'}
	return render(request, 'interface/viewall.html', context)
	# database access here		


def allmarkets(request):
	graknData=client.execute('match $x isa market, has name $y, has identifier $z; get $y,$z;') # dictionaries are nested structures
	
	# itterate thought results and put into dict -don't know why cna't access dict in the teplate when can on the command line
	allentities=[]
	for x in graknData:
		singleentity={'name':x['y']['value'],'id':x['z']['value']}
		allentities.append(singleentity)

	context = {'graknData': allentities,'title': 'All Markets','link': 'addmarket'}
	return render(request, 'interface/viewall.html', context)
	# database access here	



def allmarketneeds(request):
	graknData=client.execute('match $x isa marketneed, has name $y, has identifier $z; get $y,$z;') # dictionaries are nested structures
	
	# itterate thought results and put into dict -don't know why cna't access dict in the teplate when can on the command line
	allentities=[]
	for x in graknData:
		singleentity={'name':x['y']['value'],'id':x['z']['value']}
		allentities.append(singleentity)

	context = {'graknData': allentities,'title': 'All Market Needs','link': 'addmarketneed'}
	return render(request, 'interface/viewall.html', context)
	# database access here	




def alltechnologies(request):
	graknData=client.execute('match $x isa technology, has name $y, has identifier $z; get $y,$z;') # dictionaries are nested structures
	
	# itterate thought results and put into dict -don't know why cna't access dict in the teplate when can on the command line
	allentities=[]
	for x in graknData:
		singleentity={'name':x['y']['value'],'id':x['z']['value']}
		allentities.append(singleentity)

	context = {'graknData': allentities,'title': 'All Technolgies','link': 'addtechnology'}
	return render(request, 'interface/viewall.html', context)
	# database access here		


############### end of ALL #################


def addcompany(request):
	action = 'addcompany'
	if request.method == 'POST':
		form = addCompanyForm(data=request.POST) 
		if form.is_valid():
			name = form.cleaned_data['name']
			summary = form.cleaned_data['summary']
			#protocompany = form.cleaned_data['protocompany'] #NOT CURRENTLY USED
			marketchoice = form.cleaned_data['marketchoice']
			identifier = str(uuid.uuid4())
			client.execute('insert $x isa company, has name "' +name+'", has summary "' +summary+'", has identifier "' +identifier+'";')
		#return redirect('allcompanies')

	else:

		form = 	addCompanyForm() 
	return render(request, 'interface/addentity.html', {'form': form, 'action': action})
	


def addproject(request):
	action = 'addproject'
	if request.method == 'POST':
		form = addProjectForm(data=request.POST) 
		if form.is_valid():	


			# READ HIDDEN FIELD TO DETERMINE WHETHER SOMEHING WITH THAT ID NEEDS DELETING FIRST, IF EMPTY IS'TS NEW

			#mode = form.cleaned_data['mode']
			#print("mode:",mode)

			name = form.cleaned_data['name']
			summary = form.cleaned_data['summary']

			companychoice = form.cleaned_data['companychoice']
			technologychoice = form.cleaned_data['technologychoice']
			marketneedchoice = form.cleaned_data['marketneedchoice']
			businessmodelchoice = form.cleaned_data['businessmodelchoice']

			identifier = str(uuid.uuid4())
			client.execute('insert $x isa product, has name "' +name+'", has summary "' +summary+'", has identifier "' +identifier+'";')

			client.execute('match $x has identifier "'+identifier+'"; $y has identifier "'+companychoice+'"; insert (productowner: $y, companyproduct: $x) isa productownership;')
			client.execute('match $x has identifier "'+identifier+'"; $y has identifier "'+technologychoice+'"; insert (usestech: $y, usedinproduct: $x) isa technologystack;')
			client.execute('match $x has identifier "'+identifier+'"; $y has identifier "'+marketneedchoice+'"; insert (solvedby: $y, need: $x) isa markethasneed;')
			client.execute('match $x has identifier "'+identifier+'"; $y has identifier "'+businessmodelchoice+'"; insert (modelused: $y, usesmodel: $x) isa productbusinessmodel;')



			# quick way of seeing if these are working: match (productowner: $y, companyproduct: $x) isa productownership; offset 0; limit 30; get;
	else:
		identifier = request.GET.get('id')
		if identifier:
			form = 	addProjectForm(identifier=identifier) #i.e. we've asked to edit
		else:
			form = 	addProjectForm() # i.e. we've just asked for a fresh form
	

	# DO THE WORK HERE TO PULL THE RELATIONS EITHER WAY WITH A LINK TO EDIT THEM - PASS BACK IN AS AN ARRAY
				
	#match (productowner: $y, companyproduct: $x) isa productownership; $x has identifier "f727c8e0-eb58-48c8-8f70-903461b84419"; offset 0; limit 30; get %y;
	#^^ get the compant that owns this prouduct
	# NOTE WILL NEED TO TURN INFERENCE ON

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
			client.execute('match $x has identifier "'+identifier+'"; $y has identifier "'+top+'"; insert (modelused: $y, usesmodel: $x) isa productbusinessmodel;')
			# !!!! NEEDS A MODEL TO MODEL RELATIONSHIP !!!!!

	else:
		form = addBusinessModelForm() 
		
	return render(request, 'interface/addentity.html', {'form': form, 'action': action})



def addrisk(request):
	action = 'addrisk'
	if request.method == 'POST':
		form = addRiskForm(data=request.POST) 
		if form.is_valid():

			name = form.cleaned_data['name']
			summary = form.cleaned_data['summary']

			marketchoice = form.cleaned_data['marketchoice']
			businessmodelchoice = form.cleaned_data['businesschoice']
			technologychoice = form.cleaned_data['technologychoice']

			identifier = str(uuid.uuid4())
			client.execute('insert $x isa risk, has name "' +name+'", has summary "' +summary+'", has identifier "' +identifier+'";')

			if marketchoice:
				print(marketchoice)
				client.execute('match $x has identifier "'+identifier+'"; $y has identifier "'+marketchoice+'"; insert (riskaffects: $y, riskfactor: $x) isa markethasneed;')


			if businesschoice:
				print(marketchoice)
				client.execute('match $x has identifier "'+identifier+'"; $y has identifier "'+businessmodelchoice+'"; insert (riskaffects: $y, riskfactor: $x) isa productbusinessmodel;')
		

			if technologychoice:
				print(technologychoice)	
				client.execute('match $x has identifier "'+identifier+'"; $y has identifier "'+technologychoice+'"; insert (riskaffects: $y, riskfactor: $x) isa technologystack;')
			


	else:
		form = addRiskForm() 
		
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
			client.execute('match $x has identifier "'+identifier+'"; $y has identifier "'+marketchoice+'"; insert (riskaffects: $y, riskfactor: $x) isa markethasneed;')
			# NEEDS TO BE ADAPATED TO LINK TO SELF MARKET


	else:
		form = addMarketForm() 
		
	return render(request, 'interface/addentity.html', {'form': form, 'action': action})


def addmarketneed(request):
	action = 'addmarketneed'
	if request.method == 'POST':
		form = addMarketNeedForm(data=request.POST) 
		if form.is_valid():

			name = form.cleaned_data['name']
			summary = form.cleaned_data['summary']
			marketchoice = form.cleaned_data['marketchoice']

			identifier = str(uuid.uuid4())
			client.execute('insert $x isa marketneed, has name "' +name+'", has summary "' +summary+'", has identifier "' +identifier+'";')
			client.execute('match $x has identifier "'+identifier+'"; $y has identifier "'+marketneedchoice+'"; insert (marketpull: $y, need: $x) isa markethasneed;')

			# relate to a market

	else:
		form = addMarketNeedForm() 
		
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
			##client.execute('match $x has identifier "'+identifier+'"; $y has identifier "'+technologychoice+'"; insert (riskaffects: $y, riskfactor: $x) isa technologystack;')
			#NEEDS A LINK TO SELF TECHNOLOGY

	else:
		form = addTechnologyForm() 
		
	return render(request, 'interface/addentity.html', {'form': form, 'action': action})


def deleteentity(request):
	if request.method=='GET':
		identifier = request.GET.get('id')
		print("deleting: ", id)
		client.execute('match $r ($x) has identifier"'+identifier+'"; delete $r;') # I think you need to delete all the relationships first
		client.execute('match $y has identifier"'+identifier+'"; delete $y;') # then delete the thing, but still leaves the attributes floating - fix later

		# need some error handling!
	return render(request, 'interface/index.html')
		

# people

# development strategy

# defensibility strategy

# Funding strategy
