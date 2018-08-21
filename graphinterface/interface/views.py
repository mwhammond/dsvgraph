from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render

from .forms import addCompanyForm
from .forms import addMarketNeedForm
from .forms import addCompanyForm
from .forms import addCompetitorForm
from .forms import addRequirementForm
from .forms import addSolutionForm


from django.contrib import messages

from django.shortcuts import redirect, render

import grakn
import uuid
import datetime
import json
import random
import html



#import plotly

client = grakn.Client(uri='http://35.197.194.67:4567', keyspace='dsvgraph')

# Create your views here.

# used for finding disctinct colours for graphs
def colours(n):
  ret = []
  r = int(random.random() * 256)
  g = int(random.random() * 256)
  b = int(random.random() * 256)
  step = 256 / n
  for i in range(n):
    r += step
    g += step
    b += step
    r = int(r) % 256
    g = int(g) % 256
    b = int(b) % 256
  return (r,g,b)  




def index(request):
	if not request.user.is_authenticated:
		return redirect('/')
	else:

		graknData=client.execute('match $r isa productownership, (productowner: $y, companyproduct: $c); $y has name "DSV"; $c has name $n, has identifier $i; offset 0; limit 30; get $n, $i;') # dictionaries are nested structures
		projects=[]
		for x in graknData:
			project={'name':x['n']['value'],'id':x['i']['value']}
			projects.append(project)


		graknData=client.execute('match $x isa marketneed, has name $y, has identifier $z; order by $y asc; offset 0; limit 3; get $y,$z;') # dictionaries are nested structures
		vbps=[]
		for x in graknData:
			vbp={'name':x['y']['value'],'id':x['z']['value']}
			vbps.append(vbp)

		#onemonthback = str(datetime.datetime.now().date())	

		graknData=client.execute('match $r isa productownership, (productowner: $y, companyproduct: $c); $y has name "DSV"; $c has name $n, has identifier $i; offset 0; limit 30; get $n, $i;') # dictionaries are nested structures
		projects=[]
		for x in graknData:
			project={'name':x['n']['value'],'id':x['i']['value']}
			projects.append(project)	


		graknData=client.execute('match $r isa owner, (creator: $y, createdby: $c); $y has name $person; $c has name $thing, has identifier $i; offset 0; limit 10; get $person, $thing, $i;') # dictionaries are nested structures
		updates = []
		for x in graknData:
			update={'name':x['person']['value'],'thing':x['thing']['value'],'id':x['i']['value']}
			updates.append(update)	



		marketneedcount = client.execute('match $x isa marketneed; aggregate count;')
		requirementcount = client.execute('match $x isa requirement; aggregate count;')
		solutioncount = client.execute('match $x isa solutioncomponent; aggregate count;')
		products = client.execute('match $x isa product; aggregate count;')
		people = client.execute('match $x isa person; aggregate count;')
	


		context = {'projects': projects,'vbps':vbps,'title': 'Index','projectlink': 'addcompetitor', 'vbpslink':'marketanalysis', 'updates': updates, 'marketneedcount':marketneedcount, 'requirementcount': requirementcount, 'solutioncount': solutioncount, 'products': products, 'people': people}


		


		return render(request, 'interface/index.html', context)	
		

def allproducts(request):
	if not request.user.is_authenticated:
		return redirect('/')
	else:
		graknData=client.execute('match $x isa product, has name $y, has identifier $z; get $y,$z;') # dictionaries are nested structures
		
		# itterate thought results and put into dict -don't know why cna't access dict in the teplate when can on the command line
		projects=[]
		for x in graknData:
			project={'name':x['y']['value'],'id':x['z']['value']}
			projects.append(project)

		context = {'graknData': projects,'title': 'All Projects','link': 'addcompetitor','addlink':'addcompetitor'}
		return render(request, 'interface/viewall.html', context)
		# database access here	


def allcompanies(request):
	if not request.user.is_authenticated:
		return redirect('/')
	else:
		graknData=client.execute('match $x isa company, has name $y, has identifier $z; get $y,$z;') # dictionaries are nested structures
		
		# itterate thought results and put into dict -don't know why cna't access dict in the teplate when can on the command line
		projects=[]
		for x in graknData:
			project={'name':x['y']['value'],'id':x['z']['value']}
			projects.append(project)

		context = {'graknData': projects,'title': 'All Projects','link': 'addcompany','addlink':'addcompany'}
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
			

			name = graknData[0]['n']['value']
			summary = graknData[0]['s']['value']
			size = graknData[0]['m']['value']
			CAGR = graknData[0]['c']['value']
			#competitors = ['Competitor 1 | Status: Selling | Tech: CRISPR Editing | Customers: Novartis | Funding: £26m | Exit: N/A','competitor2','competitor3']
			
			competitors=client.execute('match $x isa marketneed, has identifier "'+identifier+'"; (solvedby:$b, $x); $b has name $n, has identifier $i; get $n, $i;')
			
			customers=client.execute('match $x isa marketneed, has identifier "'+identifier+'"; (customer:$b, $x); $b has name $n, has identifier $i; get $n, $i;')

			requirements=client.execute('match $x isa marketneed, has identifier "'+identifier+'"; (requiremententity:$b, $x); $b has name $n, has identifier $i, has importance $imp; get $n, $i, $imp;')


			# pull in sits withinmarkets and get all their requirements
			sitswithinmarkets = client.execute('match $x isa marketneed, has identifier "'+identifier+'"; (lowermarketneed:$x, $b); $b has identifier $i, has name $n; get $i, $n;')	

			submarkets = client.execute('match $x has identifier "'+identifier+'"; (topmarketneed: $x, lowermarketneed: $y); $y has name $n, has identifier $i; get $i, $n;')  
			
			submarketArray=[]
			if submarkets:
				for sub in submarkets:
					submarketArray.append({'name':sub['n']['value'],'id':sub['i']['value']})	# !!!!! THIS NEEDS TO BE AN ABLE TO HANDLE AN ARRAY IN THE TEMPLATE !!!!!	

			superMarketArray=[]
			if sitswithinmarkets:
				for sup in sitswithinmarkets:
					superMarketArray.append({'name':sup['n']['value'],'id':sup['i']['value']})

			customersarray=[]
			if customers:
				for cust in customers:
					customersarray.append({'name':cust['n']['value'],'id':cust['i']['value']})

			competitorsarray=[]
			if competitors:
				for comp in competitors:
					competitorsarray.append({'name':comp['n']['value'],'id':comp['i']['value']})	# !!!!! THIS NEEDS TO BE AN ABLE TO HANDLE AN ARRAY IN THE TEMPLATE !!!!!	

			# attach direct requirements		
			requirementssarray=[]
			reqNameArray=[]
			if requirements:
				for req in requirements:
					requirementssarray.append({'name':req['n']['value'],'id':req['i']['value'], 'importance':req['imp']['value']})		
					reqNameArray.append(req['n']['value'])			

			# attach requirements from related markets		
			if sitswithinmarkets:
				for i in range(0,len(sitswithinmarkets)):
					req2 = client.execute('match $x isa marketneed, has identifier "'+sitswithinmarkets[i]['i']['value']+'"; (requiremententity:$b, $x); $b has name $n, has identifier $i, has importance $imp; get $n, $i, $imp;')

					for req in req2:
						requirementssarray.append({'name':req['n']['value'],'id':req['i']['value'],'importance':req['imp']['value']})	
						reqNameArray.append(req['n']['value'])



			####### Competitor analysis table
			
			comparisonTable=[]
			colourTable=[]
			rankingdict={0:10, 1:20, 2:50, 3:200, 4:500, 5:1000}
			radarArrayAll=[]
			comparisonTableRadar=[]

	
			if requirementssarray:

				print("-------")		

				for comp in competitors:
					performanceArray=[]
					rArray=[]
					performanceArray.append({'val':comp['n']['value'],'col':'light','id':comp['i']['value']})
					score=0

					for req in requirementssarray: # something wacky with append above requires this zero
						# find if the requirement has any solutions associated specifically for this product (built the relationship but couldn't get to work in one command so using product id as a key, could be better)
						sol = client.execute('match $x isa requirement, has identifier "'+req['id']+'"; (solution:$b, $x); $b has name $n, has productid "'+comp['i']['value']+'", has identifier $i, has status $s, has confidence $co; get $n, $i, $s, $co;')
		
						if sol:
							sol=sol[0]

							# work out the score fresh like bakers bread
							score += (rankingdict[int(req['importance'])]*int(sol['s']['value'])) # int to round down
							# save said score for quick access from other pages

							performanceArray.append({'val':int(sol['s']['value']), 'col':'success'})
							rArray.append(int(sol['s']['value']))

							highlight="light"
							if int(sol['s']['value'])<2:
								highlight="danger"
							else:
								highlight="success"	

						else:
							performanceArray.append({'val':0, 'col':'danger'})
							rArray.append(0)

					score = int(score/len(requirementssarray))		
					performanceArray.append({'val': score, 'col': 'light'})
					comparisonTable.append(performanceArray)

					rgba = colours(1)
					rgba4 = rgba+(0.2,)

					radarArray = {'name': comp['n']['value'], 'solutionValues': rArray, 'rgba':str(rgba), 'rgba4':str(rgba4) }
				
					radarArrayAll.append(radarArray)


				comparisonTable.sort(key=lambda x: x[len(performanceArray)-1]['val'], reverse=True)	

		
		reqNameArray = json.dumps(reqNameArray)



		# find sub markets and top markets



		marketneeddata = {'id': identifier, 'name': name, 'summary': summary, 'size': size, 'CAGR': CAGR, 'customers': customersarray, 'competitors': competitorsarray, 'requirements': requirementssarray, 'comparisonTable': comparisonTable, 'colourTable': colourTable, 'submarketArray': submarketArray, 'superMarketArray': superMarketArray}

		context = {'title': 'Define Venture Backable Problem','link': 'addmarketneed', 'marketneeddata': marketneeddata, 'radarArrayAll': radarArrayAll, 'reqNameArray': reqNameArray}
		
		return render(request, 'interface/analysis.html', context)
		# database access here	




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

		context = {'graknData': allentities,'title': 'All Opportunities','link': 'marketanalysis', 'addlink':'addmarketneed'}
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
					client.execute('match $x isa product, has name $n, has summary $s, has identifier "'+identifier+'"; delete $n, $s;')
					# Delete specific relationships
					client.execute('match $r ($x) isa productownership; $x isa product has identifier "'+identifier+'"; delete $r;')
					
					client.execute('match $r ($x) isa producstisinmarket; $x isa product has identifier "'+identifier+'"; delete $r;')		



				else:
					# don't delete anything and create new identifier
					identifier = str(uuid.uuid4())


				name = form.cleaned_data['name'].encode('utf-8').decode('latin-1')
				summary = form.cleaned_data['summary'].encode('utf-8').decode('latin-1')

				companychoice = form.cleaned_data['companychoice']
				#technologychoice = form.cleaned_data['technologychoice']
				marketneedchoice = form.cleaned_data['marketneedchoice']
				#businessmodelchoice = form.cleaned_data['businessmodelchoice']

				#x = datetime.datetime.now()
				#print(x.strftime("%Y-%m-%d"))
				#print(strftime(x.strftime("%Y-%m-%d %H:%M")))

				client.execute('insert $x isa product, has name "' +name+'", has summary "' +summary+'", has identifier "' +identifier+'", has updated '+str(datetime.datetime.now().date())+';')

				client.execute('match $x has identifier "'+identifier+'"; $y has identifier "'+companychoice+'"; insert (productowner: $y, companyproduct: $x) isa productownership;')
				
				#client.execute('match $x has identifier "'+identifier+'"; $y has identifier "'+businessmodelchoice+'"; insert (modelused: $y, usesmodel: $x) isa productbusinessmodel;')

				client.execute('match $x isa person, has email "'+request.user.email+'"; $y isa product, has identifier "'+identifier+'"; insert (createdby: $y, creator: $x) isa owner;') # NOTE THIS RELATIONSHIP IS SPELT INCORRECLTY IN THE GRAPH

				client.execute('match $x has identifier "'+identifier+'"; $y has identifier "'+marketneedchoice+'"; insert (need: $y, solvedby: $x) isa producstisinmarket;') # NOTE THIS RELATIONSHIP IS SPELT INCORRECLTY IN THE GRAPH


				# add date

				
				#for th in technologychoice:	
				#	client.execute('match $x has identifier "'+identifier+'"; $y has identifier "'+th+'"; insert (usedinproduct: $y, usestech: $x) isa technologystack;')


				# quick way of seeing if these are working: match (productowner: $y, companyproduct: $x) isa productownership; offset 0; limit 30; get;
		else:
			identifier = request.GET.get('id')

			if identifier:
				form = 	addCompetitorForm(identifier=identifier) #THIS IS PASSING BACK TO THE FORM, BIT WEIRD

	
				# ------------- THE REQUIREMENTS MATCH UP AT THE BOTTOM --------------------
			
				marketid = client.execute('match $x isa product, has identifier "' +identifier+'"; (solvedby:$x, $b); $b has identifier $i; get $i;')
				sitswithinmarkets = client.execute('match $x isa marketneed, has identifier "' +marketid[0]['i']['value']+'"; (lowermarketneed:$x, $b); $b has identifier $i; get $i;')	

				print("market ids:", marketid[0]['i']['value'])
				print("sits in market ids:", sitswithinmarkets[0]['i']['value'])

				allmarkets=[]
				allmarkets.append(marketid[0]['i']['value'])

				for s in range(0,len(sitswithinmarkets)):
					allmarkets.append(sitswithinmarkets[s]['i']['value'])	

				
				print("all:", allmarkets)

				allrequirements=[]
				if allmarkets:
					for market in allmarkets:
						requirements=client.execute('match $x isa marketneed, has identifier "'+market+'"; (requiremententity:$b, $x); $b has name $n, has identifier $i, has category $c, has importance $p; get $n, $i, $c, $p;')
						allrequirements.append(requirements)
						


				#	if sitswithinmarkets:
				#		for i in range(0,len(sitswithinmarkets)):
				#			req2 = client.execute('match $x isa marketneed, has identifier "'+sitswithinmarkets[i]['i']['value']+'"; (requiremententity:$b, $x); $b has name $n, has identifier $i; get $n, $i;')
#
#						for req in req2:
#							requirementssarray.append({'name':req['n']['value'],'id':req['i']['value']})	
		




				requirementssarray=[]
				if allrequirements:

					for s in range(0,len(allrequirements)): # bit of a mess, ends up as nested list above, probably better way of doing this!

						for req in allrequirements[s]: # something wacky with append above requires this zero
							# find if the requirement has any solutions associated specifically for this product (built the relationship but couldn't get to work in one command so using product id as a key, could be better)
							sol = client.execute('match $x isa requirement, has identifier "'+req['i']['value']+'"; (solution:$b, $x); $b has name $n, has productid "'+identifier+'", has identifier $i, has status $s, has confidence $co; get $n, $i, $s, $co;')
							
							if sol:

								sol=sol[0]

								highlight="light"
								if int(sol['s']['value'])<2:
									highlight="danger"
								else:
									highlight="success"	
		

								requirementssarray.append({'name':req['n']['value'],'requirementid':req['i']['value'],'category':req['c']['value'], 'importance':req['p']['value'],
								'solutionname': sol['n']['value'],'solutionid': sol['i']['value'], 'status': sol['s']['value'], 'confidence': sol['co']['value'], 'productid':identifier, 'marketid':marketid, 'highlight':highlight})		
							else:
								requirementssarray.append({'name':req['n']['value'],'requirementid':req['i']['value'],'category':req['c']['value'], 'importance':req['p']['value'],
								'solutionname': 'Add new','solutionid': "", 'status': 'None', 'confidence': 'None','productid':identifier, 'marketid':marketid, 'highlight':"danger"})		
											

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
			


def addcompany(request):

	if not request.user.is_authenticated:
		return redirect('/')
	else:
		action = 'addcompany'
		pagetitle='Add Company'

		if request.method == 'POST':
			form = addCompanyForm(data=request.POST) 
			if form.is_valid():	
				messages.success(request, 'Saved')
				identifier = form.cleaned_data['mode'] # passed over only if form was in edit mode
				print("identifier:",identifier)

				if identifier: # i.e. we're in edit mode delete previous entity first
					client.execute('match $x isa company, has name $n, has summary $s, has fundingstage $f, has identifier "'+identifier+'"; delete $n, $s, $f;')
					# Delete specific relationships
					client.execute('match $r ($x) isa productownership; $x isa company has identifier "'+identifier+'"; delete $r;')		

				else:
					# don't delete anything and create new identifier
					identifier = str(uuid.uuid4())


				name = form.cleaned_data['name'].encode('utf-8').decode('latin-1')
				summary = form.cleaned_data['summary'].encode('utf-8').decode('latin-1')

				productownership = form.cleaned_data['productownership']
				marketneedchoice = form.cleaned_data['marketneedchoice']
				fundingstage = form.cleaned_data['fundingstage']

				
				client.execute('insert $x isa company, has name "' +name+'", has summary "' +summary+'", has identifier "' +identifier+'", has fundingstage "'+fundingstage+'" has updated '+str(datetime.datetime.now().date())+';')

				client.execute('match $x isa person, has email "'+request.user.email+'"; $y isa company, has identifier "'+identifier+'"; insert (createdby: $y, creator: $x) isa owner;') # NOTE THIS RELATIONSHIP IS SPELT INCORRECLTY IN THE GRAPH


				for ch in marketneedchoice:
					client.execute('match $x has identifier "'+identifier+'"; $y has identifier "'+ch+'"; insert (buyer: $y, customer: $x) isa custom;') # NOTE THIS RELATIONSHIP IS SPELT INCORRECLTY IN THE GRAPH

				for po in productownership:	
					client.execute('match $x has identifier "'+identifier+'"; $y has identifier "'+po+'"; insert (productowner: $x, companyproduct: $y) isa productownership;')


			# quick way of seeing if these are working: match (productowner: $y, companyproduct: $x) isa productownership; offset 0; limit 30; get;
		else:
			identifier = request.GET.get('id')
			if identifier:
				form = 	addCompanyForm(identifier=identifier) #THIS IS PASSING BACK TO THE FORM, BIT WEIRD
			else:
				marketid = request.GET.get('marketid')
				if marketid:
					form = 	addCompanyForm(marketid=marketid) # i.e. we've just asked for a fresh form
				else:
					form = addCompanyForm()	

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

				if identifier: # i.e. we're in edit mode delete previous entity first
					client.execute('match $x isa requirement, has name $n, has summary $s, has confidence $c, has importance $st, has category $ca, has identifier "'+identifier+'"; delete $n, $s, $c, $st, $ca;')
					# Delete specific relationships
					#client.execute('match $r ($x) isa requirementconnection; $x isa requirement has identifier "'+identifier+'"; delete $r;')		
					# DON'T KNOW WHY SHOULDN'T DELETE IN THIS CASE - IF YOU DO IT DELETES ANOTHER RELATIONSHIP???!	
				else:
					# don't delete anything and create new identifier
					identifier = str(uuid.uuid4())


				name = form.cleaned_data['name'].encode('utf-8').decode('latin-1')
				summary = html.escape(form.cleaned_data['summary'],quote=True)
				importance = form.cleaned_data['importance'].encode('utf-8').decode('latin-1')
				confidence = form.cleaned_data['confidence'].encode('utf-8').decode('latin-1')
				marketchoice = form.cleaned_data['marketchoice'].encode('utf-8').decode('latin-1')
				category = form.cleaned_data['category'].encode('utf-8').decode('latin-1')

				client.execute('insert $x isa requirement, has name "' +name+'", has summary "' +summary+'", has identifier "' +identifier+'", has importance ' +importance+', has confidence ' +confidence+', has category "' +category+'", has updated '+str(datetime.datetime.now().date())+';')

				print("id:",identifier)
				print("market choice:",marketchoice)
				client.execute('match $x has identifier "'+identifier+'"; $y has identifier "'+marketchoice+'"; insert (hasrequirement: $y, requiremententity: $x) isa requirementconnection;')
				
				client.execute('match $x isa person, has email "'+request.user.email+'"; $y isa requirement, has identifier "'+identifier+'"; insert (createdby: $y, creator: $x) isa owner;') # NOTE THIS RELATIONSHIP IS SPELT INCORRECLTY IN THE GRAPH


				# quick way of seeing if these are working: match (productowner: $y, companyproduct: $x) isa productownership; offset 0; limit 30; get;
		else:
			identifier = request.GET.get('id')
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



				if identifier: # i.e. we're in edit mode delete previous entity first
					client.execute('match $x isa solutioncomponent, has name $n, has summary $s, has confidence $c, has status $st, has identifier "'+identifier+'"; delete $n, $s, $c, $st;')
					# Delete specific relationships
					client.execute('match $r ($x) isa requirementmatch; $x isa solutioncomponent has identifier "'+identifier+'"; delete $r;')		
					# DON'T KNOW WHY THIS DELETE STATEMENT IS CAUSING ISSUES

				else:
					# don't delete anything and create new identifier
					identifier = str(uuid.uuid4())

				name = form.cleaned_data['name'].encode('utf-8').decode('latin-1')
				summary = html.escape(form.cleaned_data['summary'],quote=True)

				confidence = form.cleaned_data['confidence'].encode('utf-8').decode('latin-1')
				state = form.cleaned_data['state'].encode('utf-8').decode('latin-1')
				#category = form.cleaned_data['category'].encode('utf-8').decode('latin-1')
				requirement = form.cleaned_data['requirement'].encode('utf-8').decode('latin-1')

				if productid:

					client.execute('insert $x isa solutioncomponent, has name "'+name+'", has summary "' +summary+'", has productid "'+productid+'", has identifier "' +identifier+'", has confidence ' +confidence+', has status ' +state+', has updated '+str(datetime.datetime.now().date())+';')

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
					print("Warning - delete before rewrite (edit mode")

					# NEED TO DELETE SPECIFIC ATTRIBUTES AND RELATIONSHIPS NOT EVERYTHING ON EDIT!
					# Delete specific attributes

					client.execute('match $x isa marketneed, has name $n, has summary $s, has marketsize $m, has CAGR $c, has identifier "'+identifier+'"; delete $n, $s, $m, $c;')
					# Delete specific relationships
					client.execute('match $r ($x) isa marketneediswithinmarketneed; $x isa marketneed has identifier "'+identifier+'"; delete $r;')	
				else:
					# don't delete anything and create new identifier
					identifier = str(uuid.uuid4())


				name = form.cleaned_data['name'].encode('utf-8').decode('latin-1')
				summary = form.cleaned_data['summary'].encode('utf-8').decode('latin-1')
				#marketchoice = form.cleaned_data['marketchoice']
				marketsize = form.cleaned_data['marketsize']
				marketcagr = form.cleaned_data['marketcagr']
				sitswithinmarketchoice = form.cleaned_data['sitswithinmarketchoice']

				
				client.execute('insert $x isa marketneed, has name "' +name+'", has summary "' +summary+'", has marketsize '+marketsize+', has CAGR '+marketcagr+', has identifier "' +identifier+'", has updated '+str(datetime.datetime.now().date())+';')
				#client.execute('match $x has identifier "'+identifier+'"; $y has identifier "'+marketchoice+'"; insert (topmarket: $y, submarket: $x) isa withinmarket;')
				client.execute('match $x isa person, has email "'+request.user.email+'"; $y isa marketneed, has identifier "'+identifier+'"; insert (createdby: $y, creator: $x) isa owner;') # NOTE THIS RELATIONSHIP IS SPELT INCORRECLTY IN THE GRAPH

				for ch in sitswithinmarketchoice:
					#print("choice:",ch)
					client.execute('match $x has identifier "'+identifier+'"; $y has identifier "'+ch+'"; insert (topmarketneed: $y, lowermarketneed: $x) isa marketneediswithinmarketneed;') # NOTE THIS RELATIONSHIP IS SPELT INCORRECLTY IN THE GRAPH
				# relate to a market

		else:
			identifier = request.GET.get('id')
			if identifier:
				form = 	addMarketNeedForm(identifier=identifier) #so that the form can load the existing data
			else:
				form = 	addMarketNeedForm() # i.e. we've just asked for a fresh form
			
			
		guidance = "What is the size of this opportunity? How many people or companies are *directly* affected? What is the cost of that suffering per person or company? What is the rate of growth of those costs or the wider issue? What budget to customers have to solve this specific problem? Are they looking to urgently solve it at the moment? Could this really be venture scale (£100m+ sales per year)?"		

		return render(request, 'interface/addentity.html', {'form': form, 'action': action, 'pagetitle': pagetitle, 'guidance': guidance})





#def alltechnologies(request):
#	if not request.user.is_authenticated:
#		return redirect('/')
#	else:
##		graknData=client.execute('match $x isa technology, has name $y, has identifier $z; get $y,$z;') # dictionaries are nested structures
#		
#		# itterate thought results and put into dict -don't know why cna't access dict in the teplate when can on the command line
#		allentities=[]
#		for x in graknData:
#			singleentity={'name':x['y']['value'],'id':x['z']['value']}
#			allentities.append(singleentity)
#
##		context = {'graknData': allentities,'title': 'All Technolgies','link': 'addtechnology'}
#		return render(request, 'interface/viewall.html', context)
#		# database access here		
#

################################################# END OF VIEW ONLYs ###################################################




	# database access here

#def allcompanies(request):
#	if not request.user.is_authenticated:
#		return redirect('/')
#	else:	
#		graknData=client.execute('match $x isa company, has name $y, has identifier $z; get $y,$z;') # dictionaries are nested structures
#		
#		# itterate thought results and put into dict -don't know why cna't access dict in the teplate when can on the command line
#		companies=[]
#		for entry in graknData:
##			company={'name':entry['y']['value'],'id':entry['z']['value']}
#			companies.append(company)
#
#		context = {'graknData': companies, 'title': 'All Companies','link': 'addcompany'}
#		return render(request, 'interface/viewall.html', context)
	# database access here	


#def allrisk(request):
#	if not request.user.is_authenticated:
#		return redirect('/')
#	else:
#		graknData=client.execute('match $x isa risk, has name $y, has identifier $z; get $y,$z;') # dictionaries are nested structures
#		
#		# itterate thought results and put into dict -don't know why cna't access dict in the teplate when can on the command line
#		risks=[]
#		for entry in graknData:
#			risk={'name':entry['y']['value'],'id':entry['z']['value']}
#			risks.append(risk)
#
#		context = {'graknData': risks, 'title': 'All Risks','link': 'addrisk'}
#		return render(request, 'interface/viewall.html', context)
		# database access here	


#def allprojects(request):
#	if not request.user.is_authenticated:
#		return redirect('/')
#	else:
#		graknData=client.execute('match $x isa product, has name $y, has identifier $z; get $y,$z;') # dictionaries are nested structures
#		
#		# itterate thought results and put into dict -don't know why cna't access dict in the teplate when can on the command line
#		projects=[]
#		for x in graknData:
#			project={'name':x['y']['value'],'id':x['z']['value']}
#			projects.append(project)
#
#		context = {'graknData': projects,'title': 'All Projects','link': 'addcompetitor'}
#		return render(request, 'interface/viewall.html', context)
		# database access here	



#def allbusinessmodels(request):
#	
#	if not request.user.is_authenticated:
#		return redirect('/')
#	else:
#		graknData=client.execute('match $x isa businessmodel, has name $y, has identifier $z; get $y, $z;') # dictionaries are nested structures
#		
#		# itterate thought results and put into dict -don't know why cna't access dict in the teplate when can on the command line
#		allentities=[]
#		for x in graknData:
#			singleentity={'name':x['y']['value'],'id':x['z']['value']}
#			allentities.append(singleentity)
#
#		context = {'graknData': allentities,'title': 'All Business Models','link': 'addbusinessmodel'}
#		return render(request, 'interface/viewall.html', context)
		# database access here		





#def addproject(request):
#	
#	if not request.user.is_authenticated:
##		return redirect('/')
#	else:
#		action = 'addproject'
#		pagetitle='Add Competitor'
#
#		if request.method == 'POST':
#			form = addProjectForm(data=request.POST) 
#			if form.is_valid():	
#				messages.success(request, 'Saved')
#				identifier = form.cleaned_data['mode'] # passed over only if form was in edit mode
#				print("identifier:",identifier)
#
#				if identifier: # i.e. we're in edit mode delete previous entity first
#					client.execute('match $r ($x) has identifier"'+identifier+'"; delete $r;') # I think you need to delete all the relationships first
#					client.execute('match $y has identifier"'+identifier+'"; delete $y;') # then delete the thing, but still leaves the attributes floating - fix later
#					print("Warning - delete before rewrite (edit mode")
#
#				name = form.cleaned_data['name'].encode('utf-8').decode('latin-1')
#				summary = form.cleaned_data['summary'].encode('utf-8').decode('latin-1')
#
#				companychoice = form.cleaned_data['companychoice']
#				technologychoice = form.cleaned_data['technologychoice']
#				marketneedchoice = form.cleaned_data['marketneedchoice']
##				businessmodelchoice = form.cleaned_data['businessmodelchoice']
#
#
#
#				identifier = str(uuid.uuid4())
#				client.execute('insert $x isa product, has name "' +name+'", has summary "' +summary+'", has identifier "' +identifier+'";')
#
#				client.execute('match $x has identifier "'+identifier+'"; $y has identifier "'+companychoice+'"; insert (productowner: $y, companyproduct: $x) isa productownership;')
#				
#				client.execute('match $x has identifier "'+identifier+'"; $y has identifier "'+businessmodelchoice+'"; insert (modelused: $y, usesmodel: $x) isa productbusinessmodel;')
#
#				client.execute('match $x isa person, has email "'+request.user.email+'"; $y isa product, has identifier "'+identifier+'"; insert (createdby: $y, creator: $x) isa owner;') # NOTE THIS RELATIONSHIP IS SPELT INCORRECLTY IN THE GRAPH
##
#
#
#				for ch in marketneedchoice:
#					#print("choice:",ch)
#					client.execute('match $x has identifier "'+identifier+'"; $y has identifier "'+ch+'"; insert (need: $y, solvedby: $x) isa producstisinmarket;') # NOTE THIS RELATIONSHIP IS SPELT INCORRECLTY IN THE GRAPH
#
#				for th in technologychoice:	
#					client.execute('match $x has identifier "'+identifier+'"; $y has identifier "'+th+'"; insert (usedinproduct: $y, usestech: $x) isa technologystack;')
#
#
#				# quick way of seeing if these are working: match (productowner: $y, companyproduct: $x) isa productownership; offset 0; limit 30; get;
#		else:
#			identifier = request.GET.get('id')
#			if identifier:
##				form = 	addProjectForm(identifier=identifier) #THIS IS PASSING BACK TO THE FORM, BIT WEIRD
#			else:
#				form = 	addProjectForm() # i.e. we've just asked for a fresh form
		

		# DO THE WORK HERE TO PULL THE RELATIONS EITHER WAY WITH A LINK TO EDIT THEM - PASS BACK IN AS AN ARRAY
					
		#match (productowner: $y, companyproduct: $x) isa productownership; $x has identifier "f727c8e0-eb58-48c8-8f70-903461b84419"; offset 0; limit 30; get %y;
		#^^ get the compant that owns this prouduct
		# NOTE WILL NEED TO TURN INFERENCE ON

#		return render(request, 'interface/addentity.html', {'form': form, 'action': action, 'pagetitle': pagetitle})	







#def addrisk(request):
#	if not request.user.is_authenticated:
#		return redirect('/')
#	else:
#		action = 'addrisk'
#		if request.method == 'POST':
#			form = addRiskForm(data=request.POST) 
#			if form.is_valid():
#				messages.success(request, 'Saved')
#
#				identifier = form.cleaned_data['mode'] # passed over only if form was in edit mode
#
#
#				if identifier: # i.e. we're in edit mode delete previous entity first
#					client.execute('match $r ($x) has identifier"'+identifier+'"; delete $r;') # I think you need to delete all the relationships first
#					client.execute('match $y has identifier"'+identifier+'"; delete $y;') # then delete the thing, but still leaves the attributes floating - fix later
#					print("Warning - delete before rewrite (edit mode")
#
#
#				name = form.cleaned_data['name'].encode('utf-8').decode('latin-1')
#				summary = form.cleaned_data['summary'].encode('utf-8').decode('latin-1')
#
#				marketchoice = form.cleaned_data['marketchoice']
#				businesschoice = form.cleaned_data['businesschoice']
#				technologychoice = form.cleaned_data['technologychoice']
#				rating = form.cleaned_data['score']
#
#				identifier = str(uuid.uuid4())
#				client.execute('insert $x isa risk, has name "' +name+'", has summary "' +summary+'", has identifier "' +identifier+'", has rating '+rating+';')
##
#				client.execute('match $x isa person, has email "'+request.user.email+'"; $y isa risk, has identifier "'+identifier+'"; insert (createdby: $y, creator: $x) isa owner;') # NOTE THIS RELATIONSHIP IS SPELT INCORRECLTY IN THE GRAPH
#
#
#				if marketchoice is not "N/A":
#					print(marketchoice)
#					client.execute('match $x has identifier "'+identifier+'"; $y has identifier "'+marketchoice+'"; insert (riskaffects: $y, riskfactor: $x) isa hasrisk;')
#
#
#				if businesschoice is not "N/A":
#					print(marketchoice)
#					client.execute('match $x has identifier "'+identifier+'"; $y has identifier "'+businesschoice+'"; insert (riskaffects: $y, riskfactor: $x) isa hasrisk;')
#			
#
#				if technologychoice is not "N/A":
#					print(technologychoice)	
#					client.execute('match $x has identifier "'+identifier+'"; $y has identifier "'+technologychoice+'"; insert (riskaffects: $y, riskfactor: $x) isa hasrisk;')
#				
#
#
#		else:
##			identifier = request.GET.get('id')
#			if identifier:
#				form = 	addRiskForm(identifier=identifier) #so that the form can load the existing data
#			else:
#				form = 	addRiskForm() # i.e. we've just asked for a fresh form
#			
#			
#		return render(request, 'interface/addentity.html', {'form': form, 'action': action})




# business model
#def addbusinessmodel(request):
#	if not request.user.is_authenticated:
##		return redirect('/')
#	else:
#		action = 'addbusinessmodel'
#		if request.method == 'POST':
##			form = addBusinessModelForm(data=request.POST) 
#			if form.is_valid():
#				messages.success(request, 'Saved')
#
#				identifier = form.cleaned_data['mode'] # passed over only if form was in edit mode
#
#
#				if identifier: # i.e. we're in edit mode delete previous entity first
#					client.execute('match $r ($x) has identifier"'+identifier+'"; delete $r;') # I think you need to delete all the relationships first
#					client.execute('match $y has identifier"'+identifier+'"; delete $y;') # then delete the thing, but still leaves the attributes floating - fix later
#					print("Warning - delete before rewrite (edit mode")
#
#
#				name = form.cleaned_data['name']
#				summary = form.cleaned_data['summary']
#				top = form.cleaned_data['top']
#
##				identifier = str(uuid.uuid4())
#				client.execute('insert $x isa businessmodel, has name "' +name+'", has summary "' +summary+'", has identifier "' +identifier+'";')
#				client.execute('match $x has identifier "'+identifier+'"; $y has identifier "'+top+'"; insert (subbusinessmodel: $y, topbusinessmodel: $x) isa businessmodelgroup;')
#				client.execute('match $x isa person, has email "'+request.user.email+'"; $y isa businessmodel, has identifier "'+identifier+'"; insert (createdby: $y, creator: $x) isa owner;') # NOTE THIS RELATIONSHIP IS SPELT INCORRECLTY IN THE GRAPH
#
#
#
#		else:
##			identifier = request.GET.get('id')
#			if identifier:
#				form = 	addBusinessModelForm(identifier=identifier) #so that the form can load the existing data
#			else:
#				form = 	addBusinessModelForm() # i.e. we've just asked for a fresh form
##			
#		return render(request, 'interface/addentity.html', {'form': form, 'action': action})








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





# technology

#def addtechnology(request):
#	if not request.user.is_authenticated:
#		return redirect('/')
#	else:
#		action = 'addtechnology'
##		if request.method == 'POST':
#			form = addTechnologyForm(data=request.POST) 
#			if form.is_valid():
#				messages.success(request, 'Saved')
#
##				identifier = form.cleaned_data['mode'] # passed over only if form was in edit mode
#
#
#				if identifier: # i.e. we're in edit mode delete previous entity first
#					client.execute('match $r ($x) has identifier"'+identifier+'"; delete $r;') # I think you need to delete all the relationships first
##					client.execute('match $y has identifier"'+identifier+'"; delete $y;') # then delete the thing, but still leaves the attributes floating - fix later
#					print("Warning - delete before rewrite (edit mode")
#
#
#				name = form.cleaned_data['name'].encode('utf-8').decode('latin-1')
##				summary = form.cleaned_data['summary'].encode('utf-8').decode('latin-1')
#				technologychoice = form.cleaned_data['technologychoice']
#
#				identifier = str(uuid.uuid4())
#				client.execute('insert $x isa technology, has name "' +name+'", has summary "' +summary+'", has identifier "' +identifier+'";')
##				if technologychoice is not "N/A":
#					client.execute('match $x has identifier "'+identifier+'"; $y has identifier "'+technologychoice+'"; insert (subtechnology: $y, toptechnology: $x) isa technologygroup;')
#					client.execute('match $x isa person, has email "'+request.user.email+'"; $y isa technology, has identifier "'+identifier+'"; insert (createdby: $y, creator: $x) isa owner;') # NOTE THIS RELATIONSHIP IS SPELT INCORRECLTY IN THE GRAPH
#
#		else:
##			identifier = request.GET.get('id')
#			if identifier:
#				form = 	addTechnologyForm(identifier=identifier) #so that the form can load the existing data
##			else:
#				form = 	addTechnologyForm() # i.e. we've just asked for a fresh form
#			
#			
#		return render(request, 'interface/addentity.html', {'form': form, 'action': action})



# DELETE SPECIFIC ENTITY - SHOULD USE THIS FOR ALL DELETING 
def deleteentity(request):
	if not request.user.is_authenticated:
		return redirect('/')
	else:
		if request.method=='GET':
			identifier = request.GET.get('id')
			print("deleting only, no relationships until resolved: ", id)
			#client.execute('match $r ($x) has identifier"'+identifier+'"; delete $r;') # I think you need to delete all the relationships first
			client.execute('match $y has identifier"'+identifier+'"; delete $y;') # then delete the thing, but still leaves the attributes floating - fix later

			# need some error handling!
		return render(request, 'interface/index.html')
			

# people

# development strategy

# defensibility strategy

# Funding strategy
