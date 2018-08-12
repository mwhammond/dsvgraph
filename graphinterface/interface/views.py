from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render

from .forms import addCompanyForm
from .forms import addProjectForm
from .forms import addTechnologyForm
from .forms import addBusinessModelForm
#from .forms import addMarketForm
from .forms import addMarketNeedForm
from .forms import addRiskForm
from .forms import addCustomerForm
from .forms import addCompetitorForm
from .forms import addRequirementForm
from .forms import addSolutionForm


from django.contrib import messages

from django.shortcuts import redirect, render

import grakn
import uuid

client = grakn.Client(uri='http://35.197.194.67:4567', keyspace='dsvgraph')

# Create your views here.

def index(request):
	if not request.user.is_authenticated:
		return redirect('/')
	else:
		return render(request, 'interface/index.html')	
			
	# database access here

def allcompanies(request):
	if not request.user.is_authenticated:
		return redirect('/')
	else:	
		graknData=client.execute('match $x isa company, has name $y, has identifier $z; get $y,$z;') # dictionaries are nested structures
		
		# itterate thought results and put into dict -don't know why cna't access dict in the teplate when can on the command line
		companies=[]
		for entry in graknData:
			company={'name':entry['y']['value'],'id':entry['z']['value']}
			companies.append(company)

		context = {'graknData': companies, 'title': 'All Companies','link': 'addcompany'}
		return render(request, 'interface/viewall.html', context)
	# database access here	


def marketanalysis(request):
	if not request.user.is_authenticated:
		return redirect('/')
	else:
		identifier = request.GET.get('id')
		print(identifier)
		if identifier:
			graknData=client.execute('match $x isa marketneed, has name $n, has summary $s, has identifier "'+identifier+'", has marketsize $m, has CAGR $c; get $n, $s, $m, $c;') # dictionaries are nested structures
			

			# itterate thought results and put into dict -don't know why cna't access dict in the teplate when can on the command line
			#companies=[]
			#for entry in graknData:
			#	company={'name':entry['y']['value'],'id':entry['z']['value']}
			#	companies.append(company)
			name = graknData[0]['n']['value']
			summary = graknData[0]['s']['value']
			size = graknData[0]['m']['value']
			CAGR = graknData[0]['c']['value']
			#competitors = ['Competitor 1 | Status: Selling | Tech: CRISPR Editing | Customers: Novartis | Funding: £26m | Exit: N/A','competitor2','competitor3']
			
			competitors=client.execute('match $x isa marketneed, has identifier "'+identifier+'"; (solvedby:$b, $x); $b has name $n, has identifier $i; get $n, $i;')
			
			customers=client.execute('match $x isa marketneed, has identifier "'+identifier+'"; (customer:$b, $x); $b has name $n, has identifier $i; get $n, $i;')

			requirements=client.execute('match $x isa marketneed, has identifier "'+identifier+'"; (requiremententity:$b, $x); $b has name $n, has identifier $i; get $n, $i;')


			customersarray=[]
			if customers:
				for cust in customers:
					customersarray.append({'name':cust['n']['value'],'id':cust['i']['value']})

			competitorsarray=[]
			if competitors:
				for comp in competitors:
					competitorsarray.append({'name':comp['n']['value'],'id':comp['i']['value']})	# !!!!! THIS NEEDS TO BE AN ABLE TO HANDLE AN ARRAY IN THE TEMPLATE !!!!!	

			requirementssarray=[]
			if requirements:
				for req in requirements:
					requirementssarray.append({'name':req['n']['value'],'id':req['i']['value']})		


			#directriskssarray=[]		
			#directrisks=client.execute('match $x isa marketneed, has identifier "'+identifier+'"; (riskaffects:$x, $b); $b has name $n, has summary $s, has identifier $i, has rating $r; get $n, $i, $s, $r;')
			#if directrisks:
			#	for drisk in directrisks:
			#		directriskssarray.append({'name':drisk['n']['value'],'id':drisk['i']['value'],'summary':drisk['s']['value'],'rating':drisk['r']['value']})	# !!!!! THIS NEEDS TO BE AN ABLE TO HANDLE AN ARRAY IN THE TEMPLATE !!!!!		
			#		print(directriskssarray)


			#relatedrisks = ['related risk1', 'related risk 2']


			marketneeddata = {'id': identifier, 'name': name, 'summary': summary, 'size': size, 'CAGR': CAGR, 'customers': customersarray, 'competitors': competitorsarray, 'requirements': requirementssarray}

			context = {'title': 'Define Venture Backable Problem','link': 'addmarketneed', 'marketneeddata': marketneeddata}
		return render(request, 'interface/analysis.html', context)
		# database access here	



def allrisk(request):
	if not request.user.is_authenticated:
		return redirect('/')
	else:
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
	if not request.user.is_authenticated:
		return redirect('/')
	else:
		graknData=client.execute('match $x isa product, has name $y, has identifier $z; get $y,$z;') # dictionaries are nested structures
		
		# itterate thought results and put into dict -don't know why cna't access dict in the teplate when can on the command line
		projects=[]
		for x in graknData:
			project={'name':x['y']['value'],'id':x['z']['value']}
			projects.append(project)

		context = {'graknData': projects,'title': 'All Projects','link': 'addcompetitor'}
		return render(request, 'interface/viewall.html', context)
		# database access here	



def allbusinessmodels(request):
	
	if not request.user.is_authenticated:
		return redirect('/')
	else:
		graknData=client.execute('match $x isa businessmodel, has name $y, has identifier $z; get $y, $z;') # dictionaries are nested structures
		
		# itterate thought results and put into dict -don't know why cna't access dict in the teplate when can on the command line
		allentities=[]
		for x in graknData:
			singleentity={'name':x['y']['value'],'id':x['z']['value']}
			allentities.append(singleentity)

		context = {'graknData': allentities,'title': 'All Business Models','link': 'addbusinessmodel'}
		return render(request, 'interface/viewall.html', context)
		# database access here		


#def allmarkets(request):
#	graknData=client.execute('match $x isa market, has name $y, has identifier $z; get $y,$z;') # dictionaries are nested structures
	
	# itterate thought results and put into dict -don't know why cna't access dict in the teplate when can on the command line
#	allentities=[]
#	for x in graknData:
#		singleentity={'name':x['y']['value'],'id':x['z']['value']}
#		allentities.append(singleentity)

#	context = {'graknData': allentities,'title': 'All Markets','link': 'addmarket', 'analysislink': 'marketanalysis'}
#	return render(request, 'interface/viewall.html', context)
#	# database access here	



def allmarketneeds(request):
	if not request.user.is_authenticated:
		return redirect('/')
	else:
		graknData=client.execute('match $x isa marketneed, has name $y, has identifier $z; get $y,$z;') # dictionaries are nested structures
		
		# itterate thought results and put into dict -don't know why cna't access dict in the teplate when can on the command line
		allentities=[]
		for x in graknData:
			singleentity={'name':x['y']['value'],'id':x['z']['value']}
			allentities.append(singleentity)

		context = {'graknData': allentities,'title': 'All Market Needs','link': 'marketanalysis'}
		return render(request, 'interface/viewall.html', context)
		# database access here	




def alltechnologies(request):
	if not request.user.is_authenticated:
		return redirect('/')
	else:
		graknData=client.execute('match $x isa technology, has name $y, has identifier $z; get $y,$z;') # dictionaries are nested structures
		
		# itterate thought results and put into dict -don't know why cna't access dict in the teplate when can on the command line
		allentities=[]
		for x in graknData:
			singleentity={'name':x['y']['value'],'id':x['z']['value']}
			allentities.append(singleentity)

		context = {'graknData': allentities,'title': 'All Technolgies','link': 'addtechnology'}
		return render(request, 'interface/viewall.html', context)
		# database access here		



def addcompetitor(request):
	if not request.user.is_authenticated:
		return redirect('/')
	else:

		action = 'addcompetitor'
		pagetitle='Add Competitor'

		requirementssarray=[]
		marketid = request.GET.get('marketid')

		if request.method == 'POST':
			form = addCompetitorForm(data=request.POST) 
			print(form.mystryvalue)
			if form.is_valid():	
				messages.success(request, 'Saved')
				identifier = form.cleaned_data['mode'] # passed over only if form was in edit mode
				print("identifier:",identifier)

				if identifier: # i.e. we're in edit mode delete previous entity first
					client.execute('match $r ($x) has identifier"'+identifier+'"; delete $r;') # I think you need to delete all the relationships first
					client.execute('match $y has identifier"'+identifier+'"; delete $y;') # then delete the thing, but still leaves the attributes floating - fix later
					print("Warning - delete before rewrite (edit mode")

				name = form.cleaned_data['name'].encode('utf-8').decode('latin-1')
				summary = form.cleaned_data['summary'].encode('utf-8').decode('latin-1')

				companychoice = form.cleaned_data['companychoice']
				#technologychoice = form.cleaned_data['technologychoice']
				marketneedchoice = form.cleaned_data['marketneedchoice']
				#businessmodelchoice = form.cleaned_data['businessmodelchoice']


				######
				######
				######
				# Add handling for new choices

				identifier = str(uuid.uuid4())
				client.execute('insert $x isa product, has name "' +name+'", has summary "' +summary+'", has identifier "' +identifier+'";')

				client.execute('match $x has identifier "'+identifier+'"; $y has identifier "'+companychoice+'"; insert (productowner: $y, companyproduct: $x) isa productownership;')
				
				#client.execute('match $x has identifier "'+identifier+'"; $y has identifier "'+businessmodelchoice+'"; insert (modelused: $y, usesmodel: $x) isa productbusinessmodel;')

				client.execute('match $x isa person, has email "'+request.user.email+'"; $y isa product, has identifier "'+identifier+'"; insert (createdby: $y, creator: $x) isa owner;') # NOTE THIS RELATIONSHIP IS SPELT INCORRECLTY IN THE GRAPH

				client.execute('match $x has identifier "'+identifier+'"; $y has identifier "'+marketneedchoice+'"; insert (need: $y, solvedby: $x) isa producstisinmarket;') # NOTE THIS RELATIONSHIP IS SPELT INCORRECLTY IN THE GRAPH

				#for th in technologychoice:	
				#	client.execute('match $x has identifier "'+identifier+'"; $y has identifier "'+th+'"; insert (usedinproduct: $y, usestech: $x) isa technologystack;')


				# quick way of seeing if these are working: match (productowner: $y, companyproduct: $x) isa productownership; offset 0; limit 30; get;
		else:
			identifier = request.GET.get('id')

			if identifier:
				form = 	addCompetitorForm(identifier=identifier) #THIS IS PASSING BACK TO THE FORM, BIT WEIRD

				# do have market ID because came from market form - get here
				#requirements=client.execute('match $x isa marketneed, has identifier "'+identifier+'"; (requiremententity:$b, $x); $b has name $n, has identifier $i; get $n, $i;')

				

				# find the market need associated with this product
	
				# ------------- THE REQUIREMENTS MATCH UP AT THE BOTTOM --------------------

				marketids=client.execute('match $x isa product, has identifier "'+identifier+'"; (need:$b, $x); $b has name $n, has identifier $i; get $n, $i;')
			
				if marketids:
					marketid = marketids[0]['i']['value'] # IS THERE A CHANCE OF MULTIPLE MARKETS FOR ONE PRODUCT? - ALMOST CERTAINLY, NEEDS TO LOOP

				# find all the requirements associated with that marketneed
					requirements=client.execute('match $x isa marketneed, has identifier "'+marketid+'"; (requiremententity:$b, $x); $b has name $n, has identifier $i, has category $c, has importance $p; get $n, $i, $c, $p;')
					requirementssarray=[]
					if requirements:
						for req in requirements:
							# find if the requirement has any solutions associated specifically for this product (built the relationship but couldn't get to work in one command so using product id as a key, could be better)
							sol = client.execute('match $x isa requirement, has identifier "'+req['i']['value']+'"; (solution:$b, $x); $b has name $n, has productid "'+identifier+'", has identifier $i, has category $c, has status $s, has confidence $co; get $n, $i, $c, $s, $co;')
							
							if sol:

								print("sol: ",sol)	
								sol=sol[0]

								requirementssarray.append({'name':req['n']['value'],'requirementid':req['i']['value'],'category':req['c']['value'], 'importance':req['p']['value'],
								'solutionname': sol['n']['value'],'solutionid': sol['i']['value'], 'status': sol['s']['value'], 'confidence': sol['co']['value'], 'productid':identifier, 'marketid':marketid})		
							else:
								requirementssarray.append({'name':req['n']['value'],'requirementid':req['i']['value'],'category':req['c']['value'], 'importance':req['p']['value'],
								'solutionname': 'Add new','solutionid': "", 'status': 'None', 'confidence': 'None','productid':identifier, 'marketid':marketid})		
											

					pagetitle='Edit Solutuion'		
		


			else:
				#marketid = request.GET.get('marketid')
				if marketid:
					form = 	addCompetitorForm(marketid=marketid) # i.e. we've just asked for a fresh form
					print(form.mystryvalue)
				else:
					form = addCompetitorForm()
					print(form.mystryvalue)



		return render(request, 'interface/addCompetitor.html', {'form': form, 'action': action, 'pagetitle': pagetitle, 'requirements': requirementssarray, 'marketid': marketid})	
			


def addcustomer(request):

	if not request.user.is_authenticated:
		return redirect('/')
	else:
		action = 'addcustomer'
		pagetitle='Add Customer'

		if request.method == 'POST':
			form = addCustomerForm(data=request.POST) 
			if form.is_valid():	
				messages.success(request, 'Saved')
				identifier = form.cleaned_data['mode'] # passed over only if form was in edit mode
				print("identifier:",identifier)

				if identifier: # i.e. we're in edit mode delete previous entity first
					client.execute('match $r ($x) has identifier"'+identifier+'"; delete $r;') # I think you need to delete all the relationships first
					client.execute('match $y has identifier"'+identifier+'"; delete $y;') # then delete the thing, but still leaves the attributes floating - fix later
					print("Warning - delete before rewrite (edit mode")

				name = form.cleaned_data['name'].encode('utf-8').decode('latin-1')
				summary = form.cleaned_data['summary'].encode('utf-8').decode('latin-1')

				companychoice = form.cleaned_data['companychoice']
				marketneedchoice = form.cleaned_data['marketneedchoice']
				businessmodelchoice = form.cleaned_data['businessmodelchoice']

				financialimpact = form.cleaned_data['financialimpact']
				userbudget= form.cleaned_data['userbudget']
				riskadversion = form.cleaned_data['riskadversion']

				identifier = str(uuid.uuid4())
				client.execute('insert $x isa product, has name "' +name+'", has summary "' +summary+'", has finimpact ' +financialimpact+', has userbudget ' +userbudget+', has riskscore ' +riskadversion+', has identifier "' +identifier+'";')

				client.execute('match $x has identifier "'+identifier+'"; $y has identifier "'+companychoice+'"; insert (productowner: $y, companyproduct: $x) isa productownership;')
				
				client.execute('match $x has identifier "'+identifier+'"; $y has identifier "'+businessmodelchoice+'"; insert (modelused: $y, usesmodel: $x) isa productbusinessmodel;')

				client.execute('match $x isa person, has email "'+request.user.email+'"; $y isa product, has identifier "'+identifier+'"; insert (createdby: $y, creator: $x) isa owner;') # NOTE THIS RELATIONSHIP IS SPELT INCORRECLTY IN THE GRAPH


				for ch in marketneedchoice:
					#print("choice:",ch)
					client.execute('match $x has identifier "'+identifier+'"; $y has identifier "'+ch+'"; insert (buyer: $y, customer: $x) isa custom;') # NOTE THIS RELATIONSHIP IS SPELT INCORRECLTY IN THE GRAPH

			#	for th in technologychoice:	
			#		client.execute('match $x has identifier "'+identifier+'"; $y has identifier "'+th+'"; insert (usedinproduct: $y, usestech: $x) isa technologystack;')


			# quick way of seeing if these are working: match (productowner: $y, companyproduct: $x) isa productownership; offset 0; limit 30; get;
		else:
			identifier = request.GET.get('id')
			if identifier:
				form = 	addCustomerForm(identifier=identifier) #THIS IS PASSING BACK TO THE FORM, BIT WEIRD
			else:
				marketid = request.GET.get('marketid')
				if marketid:
					form = 	addCustomerForm(marketid=marketid) # i.e. we've just asked for a fresh form
				else:
					form = addCustomerForm()	

		return render(request, 'interface/addentity.html', {'form': form, 'action': action, 'pagetitle': pagetitle})	




def addproject(request):
	
	if not request.user.is_authenticated:
		return redirect('/')
	else:
		action = 'addproject'
		pagetitle='Add Competitor'

		if request.method == 'POST':
			form = addProjectForm(data=request.POST) 
			if form.is_valid():	
				messages.success(request, 'Saved')
				identifier = form.cleaned_data['mode'] # passed over only if form was in edit mode
				print("identifier:",identifier)

				if identifier: # i.e. we're in edit mode delete previous entity first
					client.execute('match $r ($x) has identifier"'+identifier+'"; delete $r;') # I think you need to delete all the relationships first
					client.execute('match $y has identifier"'+identifier+'"; delete $y;') # then delete the thing, but still leaves the attributes floating - fix later
					print("Warning - delete before rewrite (edit mode")

				name = form.cleaned_data['name'].encode('utf-8').decode('latin-1')
				summary = form.cleaned_data['summary'].encode('utf-8').decode('latin-1')

				companychoice = form.cleaned_data['companychoice']
				technologychoice = form.cleaned_data['technologychoice']
				marketneedchoice = form.cleaned_data['marketneedchoice']
				businessmodelchoice = form.cleaned_data['businessmodelchoice']



				identifier = str(uuid.uuid4())
				client.execute('insert $x isa product, has name "' +name+'", has summary "' +summary+'", has identifier "' +identifier+'";')

				client.execute('match $x has identifier "'+identifier+'"; $y has identifier "'+companychoice+'"; insert (productowner: $y, companyproduct: $x) isa productownership;')
				
				client.execute('match $x has identifier "'+identifier+'"; $y has identifier "'+businessmodelchoice+'"; insert (modelused: $y, usesmodel: $x) isa productbusinessmodel;')

				client.execute('match $x isa person, has email "'+request.user.email+'"; $y isa product, has identifier "'+identifier+'"; insert (createdby: $y, creator: $x) isa owner;') # NOTE THIS RELATIONSHIP IS SPELT INCORRECLTY IN THE GRAPH



				for ch in marketneedchoice:
					#print("choice:",ch)
					client.execute('match $x has identifier "'+identifier+'"; $y has identifier "'+ch+'"; insert (need: $y, solvedby: $x) isa producstisinmarket;') # NOTE THIS RELATIONSHIP IS SPELT INCORRECLTY IN THE GRAPH

				for th in technologychoice:	
					client.execute('match $x has identifier "'+identifier+'"; $y has identifier "'+th+'"; insert (usedinproduct: $y, usestech: $x) isa technologystack;')


				# quick way of seeing if these are working: match (productowner: $y, companyproduct: $x) isa productownership; offset 0; limit 30; get;
		else:
			identifier = request.GET.get('id')
			if identifier:
				form = 	addProjectForm(identifier=identifier) #THIS IS PASSING BACK TO THE FORM, BIT WEIRD
			else:
				form = 	addProjectForm() # i.e. we've just asked for a fresh form
		

		# DO THE WORK HERE TO PULL THE RELATIONS EITHER WAY WITH A LINK TO EDIT THEM - PASS BACK IN AS AN ARRAY
					
		#match (productowner: $y, companyproduct: $x) isa productownership; $x has identifier "f727c8e0-eb58-48c8-8f70-903461b84419"; offset 0; limit 30; get %y;
		#^^ get the compant that owns this prouduct
		# NOTE WILL NEED TO TURN INFERENCE ON

		return render(request, 'interface/addentity.html', {'form': form, 'action': action, 'pagetitle': pagetitle})	




def addrequirement(request):
	
	if not request.user.is_authenticated:
		return redirect('/')
	else:
		action = 'addrequirement'
		pagetitle='Add Requirement'

		if request.method == 'POST':
			form = addRequirementForm(data=request.POST) 
			if form.is_valid():	
				messages.success(request, 'Saved')
				identifier = form.cleaned_data['mode'] # passed over only if form was in edit mode
				print("identifier:",identifier)

				if identifier: # i.e. we're in edit mode delete previous entity first
					client.execute('match $r ($x) has identifier"'+identifier+'"; delete $r;') # I think you need to delete all the relationships first
					client.execute('match $y has identifier"'+identifier+'"; delete $y;') # then delete the thing, but still leaves the attributes floating - fix later
					print("Warning - delete before rewrite (edit mode")

				name = form.cleaned_data['name'].encode('utf-8').decode('latin-1')
				summary = form.cleaned_data['summary'].encode('utf-8').decode('latin-1')
				importance = form.cleaned_data['importance'].encode('utf-8').decode('latin-1')
				confidence = form.cleaned_data['confidence'].encode('utf-8').decode('latin-1')
				marketchoice = form.cleaned_data['marketchoice'].encode('utf-8').decode('latin-1')
				category = form.cleaned_data['category'].encode('utf-8').decode('latin-1')



				identifier = str(uuid.uuid4())
				client.execute('insert $x isa requirement, has name "' +name+'", has summary "' +summary+'", has identifier "' +identifier+'", has importance ' +importance+', has confidence ' +confidence+', has category "' +category+'";')

				client.execute('match $x has identifier "'+identifier+'"; $y has identifier "'+marketchoice+'"; insert (hasrequirement: $y, requiremententity: $x) isa requirementconnection;')
				
				client.execute('match $x isa person, has email "'+request.user.email+'"; $y isa requirement, has identifier "'+identifier+'"; insert (createdby: $y, creator: $x) isa owner;') # NOTE THIS RELATIONSHIP IS SPELT INCORRECLTY IN THE GRAPH


				# quick way of seeing if these are working: match (productowner: $y, companyproduct: $x) isa productownership; offset 0; limit 30; get;
		else:
			identifier = request.GET.get('reqid')
			if identifier:
				form = 	addRequirementForm(identifier=identifier) #THIS IS PASSING BACK TO THE FORM, BIT WEIRD
			else:
				marketid = request.GET.get('marketid')
				if marketid:
					form = 	addRequirementForm(marketid=marketid) # i.e. we've just asked for a fresh form
				else:
					form = 	addRequirementForm()
		

		# DO THE WORK HERE TO PULL THE RELATIONS EITHER WAY WITH A LINK TO EDIT THEM - PASS BACK IN AS AN ARRAY
					
		#match (productowner: $y, companyproduct: $x) isa productownership; $x has identifier "f727c8e0-eb58-48c8-8f70-903461b84419"; offset 0; limit 30; get %y;
		#^^ get the compant that owns this prouduct
		# NOTE WILL NEED TO TURN INFERENCE ON

		return render(request, 'interface/addentity.html', {'form': form, 'action': action, 'pagetitle': pagetitle})	






def addsolution(request):
	
	if not request.user.is_authenticated:
		return redirect('/')
	else:
		action = 'addsolution'
		pagetitle='Add Solution'

		if request.method == 'POST':
			form = addSolutionForm(data=request.POST) 
			if form.is_valid():	
				messages.success(request, 'Saved')
				identifier = form.cleaned_data['mode'] # passed over only if form was in edit mode

				reqid = form.cleaned_data['mode']
				productid = form.cleaned_data['productid']

				print("reqid", reqid)
				print("product id", productid)

				print("identifier:",identifier)

				if identifier: # i.e. we're in edit mode delete previous entity first
					client.execute('match $r ($x) has identifier"'+identifier+'"; delete $r;') # I think you need to delete all the relationships first
					client.execute('match $y has identifier"'+identifier+'"; delete $y;') # then delete the thing, but still leaves the attributes floating - fix later
					print("Warning - delete before rewrite (edit mode")

				name = form.cleaned_data['name'].encode('utf-8').decode('latin-1')
				summary = form.cleaned_data['summary'].encode('utf-8').decode('latin-1')
				confidence = form.cleaned_data['confidence'].encode('utf-8').decode('latin-1')
				state = form.cleaned_data['state'].encode('utf-8').decode('latin-1')
				category = form.cleaned_data['category'].encode('utf-8').decode('latin-1')
				requirement = form.cleaned_data['requirement'].encode('utf-8').decode('latin-1')




				identifier = str(uuid.uuid4())

				# go a step back and find what product the requirement was linked to


				if productid:

					client.execute('insert $x isa solutioncomponent, has name "'+name+'", has summary "' +summary+'", has productid "'+productid+'", has identifier "' +identifier+'", has category "' +category+'", has confidence ' +confidence+', has status ' +state+';')

					client.execute('match $x has identifier "'+identifier+'"; $y has identifier "'+requirement+'"; insert (requiressolution: $y, solution: $x) isa requirementmatch;')

					#client.execute('match $x has identifier "'+identifier+'"; $y has identifier "'+productid+'"; insert (productincludessolution: $y, solution: $x) isa relatedtoproduct;')

					client.execute('match $x isa person, has email "'+request.user.email+'"; $y isa solutioncomponent, has identifier "'+identifier+'"; insert (createdby: $y, creator: $x) isa owner;') # NOTE THIS RELATIONSHIP IS SPELT INCORRECLTY IN THE GRAPH

				else:
				
					print("could find product to associate to?")	

		else:

			reqid = ""
			productid = ""
			solutionid = ""
			reqid = request.GET.get('reqid')
			productid = request.GET.get('productid')
			solutionid = request.GET.get('solutionid')
			form = addSolutionForm(reqid=reqid, productid=productid, solutionid=solutionid) #THIS IS PASSING BACK TO THE FORM, BIT WEIRD



		return render(request, 'interface/addentity.html', {'form': form, 'action': action, 'pagetitle': pagetitle})	














# business model
def addbusinessmodel(request):
	if not request.user.is_authenticated:
		return redirect('/')
	else:
		action = 'addbusinessmodel'
		if request.method == 'POST':
			form = addBusinessModelForm(data=request.POST) 
			if form.is_valid():
				messages.success(request, 'Saved')

				identifier = form.cleaned_data['mode'] # passed over only if form was in edit mode


				if identifier: # i.e. we're in edit mode delete previous entity first
					client.execute('match $r ($x) has identifier"'+identifier+'"; delete $r;') # I think you need to delete all the relationships first
					client.execute('match $y has identifier"'+identifier+'"; delete $y;') # then delete the thing, but still leaves the attributes floating - fix later
					print("Warning - delete before rewrite (edit mode")


				name = form.cleaned_data['name']
				summary = form.cleaned_data['summary']
				top = form.cleaned_data['top']

				identifier = str(uuid.uuid4())
				client.execute('insert $x isa businessmodel, has name "' +name+'", has summary "' +summary+'", has identifier "' +identifier+'";')
				client.execute('match $x has identifier "'+identifier+'"; $y has identifier "'+top+'"; insert (subbusinessmodel: $y, topbusinessmodel: $x) isa businessmodelgroup;')
				client.execute('match $x isa person, has email "'+request.user.email+'"; $y isa businessmodel, has identifier "'+identifier+'"; insert (createdby: $y, creator: $x) isa owner;') # NOTE THIS RELATIONSHIP IS SPELT INCORRECLTY IN THE GRAPH



		else:
			identifier = request.GET.get('id')
			if identifier:
				form = 	addBusinessModelForm(identifier=identifier) #so that the form can load the existing data
			else:
				form = 	addBusinessModelForm() # i.e. we've just asked for a fresh form
			
		return render(request, 'interface/addentity.html', {'form': form, 'action': action})



def addrisk(request):
	if not request.user.is_authenticated:
		return redirect('/')
	else:
		action = 'addrisk'
		if request.method == 'POST':
			form = addRiskForm(data=request.POST) 
			if form.is_valid():
				messages.success(request, 'Saved')

				identifier = form.cleaned_data['mode'] # passed over only if form was in edit mode


				if identifier: # i.e. we're in edit mode delete previous entity first
					client.execute('match $r ($x) has identifier"'+identifier+'"; delete $r;') # I think you need to delete all the relationships first
					client.execute('match $y has identifier"'+identifier+'"; delete $y;') # then delete the thing, but still leaves the attributes floating - fix later
					print("Warning - delete before rewrite (edit mode")


				name = form.cleaned_data['name'].encode('utf-8').decode('latin-1')
				summary = form.cleaned_data['summary'].encode('utf-8').decode('latin-1')

				marketchoice = form.cleaned_data['marketchoice']
				businesschoice = form.cleaned_data['businesschoice']
				technologychoice = form.cleaned_data['technologychoice']
				rating = form.cleaned_data['score']

				identifier = str(uuid.uuid4())
				client.execute('insert $x isa risk, has name "' +name+'", has summary "' +summary+'", has identifier "' +identifier+'", has rating '+rating+';')

				client.execute('match $x isa person, has email "'+request.user.email+'"; $y isa risk, has identifier "'+identifier+'"; insert (createdby: $y, creator: $x) isa owner;') # NOTE THIS RELATIONSHIP IS SPELT INCORRECLTY IN THE GRAPH


				if marketchoice is not "N/A":
					print(marketchoice)
					client.execute('match $x has identifier "'+identifier+'"; $y has identifier "'+marketchoice+'"; insert (riskaffects: $y, riskfactor: $x) isa hasrisk;')


				if businesschoice is not "N/A":
					print(marketchoice)
					client.execute('match $x has identifier "'+identifier+'"; $y has identifier "'+businesschoice+'"; insert (riskaffects: $y, riskfactor: $x) isa hasrisk;')
			

				if technologychoice is not "N/A":
					print(technologychoice)	
					client.execute('match $x has identifier "'+identifier+'"; $y has identifier "'+technologychoice+'"; insert (riskaffects: $y, riskfactor: $x) isa hasrisk;')
				


		else:
			identifier = request.GET.get('id')
			if identifier:
				form = 	addRiskForm(identifier=identifier) #so that the form can load the existing data
			else:
				form = 	addRiskForm() # i.e. we've just asked for a fresh form
			
			
		return render(request, 'interface/addentity.html', {'form': form, 'action': action})




# market


#def addmarket(request):
#	action = 'addmarket'
#	if request.method == 'POST':
#		form = addMarketForm(data=request.POST) 
#		if form.is_valid():

#			identifier = form.cleaned_data['mode'] # passed over only if form was in edit mode

#			if identifier: # i.e. we're in edit mode delete previous entity first
#				client.execute('match $r ($x) has identifier"'+identifier+'"; delete $r;') # I think you need to delete all the relationships first
#				client.execute('match $y has identifier"'+identifier+'"; delete $y;') # then delete the thing, but still leaves the attributes floating - fix later
#				print("Warning - delete before rewrite (edit mode")


#			name = form.cleaned_data['name']
#			summary = form.cleaned_data['summary']
#			top = form.cleaned_data['top']

#			identifier = str(uuid.uuid4())
#			client.execute('insert $x isa market, has name "' +name+'", has summary "' +summary+'", has identifier "' +identifier+'";')
#			client.execute('match $x has identifier "'+identifier+'"; $y has identifier "'+top+'"; insert (submarket: $y, topmarket: $x) isa withinmarket;')



#	else:
#		identifier = request.GET.get('id')
#		if identifier:
#			form = 	addMarketForm(identifier=identifier) #so that the form can load the existing data
#		else:
#			form = 	addMarketForm() # i.e. we've just asked for a fresh form
		
#	return render(request, 'interface/addentity.html', {'form': form, 'action': action})


def addmarketneed(request):
	if not request.user.is_authenticated:
		return redirect('/')
	else:
		action = 'addmarketneed'
		pagetitle = "Define venture backable problem"
		if request.method == 'POST':
			form = addMarketNeedForm(data=request.POST) 
			if form.is_valid():
				messages.success(request, 'Saved')

				identifier = form.cleaned_data['mode'] # passed over only if form was in edit mode

				if identifier: # i.e. we're in edit mode delete previous entity first
					client.execute('match $r ($x) has identifier"'+identifier+'"; delete $r;') # I think you need to delete all the relationships first
					client.execute('match $y has identifier"'+identifier+'"; delete $y;') # then delete the thing, but still leaves the attributes floating - fix later
					print("Warning - delete before rewrite (edit mode")



				name = form.cleaned_data['name'].encode('utf-8').decode('latin-1')
				summary = form.cleaned_data['summary'].encode('utf-8').decode('latin-1')
				marketchoice = form.cleaned_data['marketchoice']
				marketsize = form.cleaned_data['marketsize']
				marketcagr = form.cleaned_data['marketcagr']

				identifier = str(uuid.uuid4())
				client.execute('insert $x isa marketneed, has name "' +name+'", has summary "' +summary+'", has marketsize '+marketsize+', has CAGR '+marketcagr+', has identifier "' +identifier+'";')
				client.execute('match $x has identifier "'+identifier+'"; $y has identifier "'+marketchoice+'"; insert (topmarket: $y, submarket: $x) isa withinmarket;')
				client.execute('match $x isa person, has email "'+request.user.email+'"; $y isa marketneed, has identifier "'+identifier+'"; insert (createdby: $y, creator: $x) isa owner;') # NOTE THIS RELATIONSHIP IS SPELT INCORRECLTY IN THE GRAPH

				# relate to a market

		else:
			identifier = request.GET.get('id')
			if identifier:
				form = 	addMarketNeedForm(identifier=identifier) #so that the form can load the existing data
			else:
				form = 	addMarketNeedForm() # i.e. we've just asked for a fresh form
			
			
		return render(request, 'interface/addentity.html', {'form': form, 'action': action, 'pagetitle': pagetitle})



# technology

def addtechnology(request):
	if not request.user.is_authenticated:
		return redirect('/')
	else:
		action = 'addtechnology'
		if request.method == 'POST':
			form = addTechnologyForm(data=request.POST) 
			if form.is_valid():
				messages.success(request, 'Saved')

				identifier = form.cleaned_data['mode'] # passed over only if form was in edit mode


				if identifier: # i.e. we're in edit mode delete previous entity first
					client.execute('match $r ($x) has identifier"'+identifier+'"; delete $r;') # I think you need to delete all the relationships first
					client.execute('match $y has identifier"'+identifier+'"; delete $y;') # then delete the thing, but still leaves the attributes floating - fix later
					print("Warning - delete before rewrite (edit mode")


				name = form.cleaned_data['name'].encode('utf-8').decode('latin-1')
				summary = form.cleaned_data['summary'].encode('utf-8').decode('latin-1')
				technologychoice = form.cleaned_data['technologychoice']

				identifier = str(uuid.uuid4())
				client.execute('insert $x isa technology, has name "' +name+'", has summary "' +summary+'", has identifier "' +identifier+'";')
				if technologychoice is not "N/A":
					client.execute('match $x has identifier "'+identifier+'"; $y has identifier "'+technologychoice+'"; insert (subtechnology: $y, toptechnology: $x) isa technologygroup;')
					client.execute('match $x isa person, has email "'+request.user.email+'"; $y isa technology, has identifier "'+identifier+'"; insert (createdby: $y, creator: $x) isa owner;') # NOTE THIS RELATIONSHIP IS SPELT INCORRECLTY IN THE GRAPH

		else:
			identifier = request.GET.get('id')
			if identifier:
				form = 	addTechnologyForm(identifier=identifier) #so that the form can load the existing data
			else:
				form = 	addTechnologyForm() # i.e. we've just asked for a fresh form
			
			
		return render(request, 'interface/addentity.html', {'form': form, 'action': action})



# DELETE SPECIFIC ENTITY - SHOULD USE THIS FOR ALL DELETING 
def deleteentity(request):
	if not request.user.is_authenticated:
		return redirect('/')
	else:
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
