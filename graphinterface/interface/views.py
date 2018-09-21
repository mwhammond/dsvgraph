from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render

from .forms import addCompanyForm
from .forms import addMarketNeedForm
from .forms import addCompanyForm
from .forms import addRequirementForm
from .forms import addSolutionForm
from .forms import addTechnologyForm

from .forms import addProduct2Form


from django.contrib import messages

from django.shortcuts import redirect, render, render_to_response

import grakn
import uuid
import datetime
import json
import html

import pandas as pd
import matplotlib
matplotlib.use('agg') # for google cloud headless environment
import matplotlib.pyplot as plt
import pylab

import random as rand # note after as pylab has it's own random function!

import seaborn as sns

import io
from io import *

# installed as Pillow
import PIL
from PIL import Image

import numpy as np
import base64

from collections import Counter



#import plotly

client = grakn.Client(uri='http://35.197.194.67:4567', keyspace='dsvgraph')

# Create your views here.

# used for finding disctinct colours for graphs
def colours(n):
  ret = []
  r = int(rand.random() * 256)
  g = int(rand.random() * 256)
  b = int(rand.random() * 256)
  step = 256 / n
  for i in range(n):
    r += step
    g += step
    b += step
    r = int(r) % 256
    g = int(g) % 256
    b = int(b) % 256
  return (r,g,b)  


# THIS IS A SEPARATE FUNCTION BECAUSE MATPLOTLIB TK BACKGROUND BLOCKS SO OTHERWISE REQUIRES MULTIHTREADING - IT'S PART OF MARKETANALYSIS VIEW CALLED FROM THE TEMPLATE AS AN IMAGE LINK
def graph(request):

	identifier = request.GET.get('id')

	print("identifier recieved: ", identifier)
	sns.set()

# Load the example iris dataset
	#planets = sns.load_dataset("planets")

	#cmap = sns.cubehelix_palette(rot=-.2, as_cmap=True)
	#ax = sns.scatterplot(x="distance", y="orbital_period",
	#                     hue="year", size="mass",
	#                     palette=cmap, sizes=(10, 200),
	#                     data=planets)
	
	reqandsol = client.execute('match $marketidentifier has identifier "'+identifier+'"; (solvedby:$m, $marketidentifier); $m has name $productname; (productrequirement: $pr, requirementproduct: $m), has statusfloat $statusfloat; $pr has name $reqname, has importance $reqimp; get $productname, $reqname, $statusfloat, $reqimp;')
			
	# put into a Pandas dataframe
	reandsolflt=[]
	for i in range(0,len(reqandsol)):
		flt = ([reqandsol[i]['productname']['value'], reqandsol[i]['reqname']['value'], reqandsol[i]['statusfloat']['value'], reqandsol[i]['reqimp']['value']])
		reandsolflt.append(flt)
			

	reqandsoldf = pd.DataFrame(reandsolflt, columns = ["Product","Requirement","Status","Importance"])


	reqandsoldf[['Status','Importance']] = reqandsoldf[['Status','Importance']].apply(pd.to_numeric)
	#reqandsoldf.replace(0,np.nan, inplace=True) < LEFT AT TRYING TO CONVERT ZEROS TO NAN

	reqandsolpivot = reqandsoldf.pivot(index='Product', columns='Requirement', values='Status')


	# Simple data to display in various forms
	x = np.linspace(0, 2 * np.pi, 400)
	y = np.sin(x ** 2)

	plt.close('all')


	marketStatus=[(0.0,"Unknown"),(-1.0,"Key reason for failure, or current serious issues"),(0.5,"No market identified"),(1.5,"Single small market -100s millions. Low growth"),(2.0,"Single small market - 100s millions. High growth"),(2.5,"Single mid-sized market low billons. Low growth"),(3.0,"Single mid-sized market - low billons. High growth"),(3.5,"Multiple mid-sized growing markets"),(4.0,"Single huge market - multi billions, low growth"),(4.5,"Single huge market -multi billions. High growth"),(5.0,"Multiple large markets. Not growing"),(5.5,"Multiple large markets. High growth")]
	defenseStatus=[(0.0,"Unknown"),(-1.0,"Key reason for failure, or current serious issues"),(0.5,"No defensibility"),(1.5,"Weak IP strategy"),(5.5,"Strong IP strategy")]
	manuStatus=[(0.0,"Unknown"),(-1.0,"Key reason for failure, or current serious issues"),(0.5,"Likely impossible"),(1,"Unsolved, theoretically possible in >5 years"),(1.5,"Unsolved, theoretically possible in >2 years"),(2.0,"Theoretically feasible in <2 years"),(2.5,"Lab scale proven"),	(3.5,"Demonstrator scale proven"),(5.5,"Proven at scale or not relavent")]
	scaleStatus=[(0.0,"Unknown"),(-1.0,"Key reason for failure, or current serious issues"),(0.5,"Expensive to produce, large upfront investment, small margin, limit on production"),(1.0,"Expensive distribution and low margin"),(2.0,"Cheap to produce, large upfront investment, no limit on production, large margin"),(3.0,"Cheap to produce, small upfront investment or distribution costs that needs to be covered, large margin"),(4.0,"Cheap to produce, small upfront investment or ongoing distribution - that will be covered by others, large margin"),(4.5,"Cost decoupled from unit price"),	(5.5,"Near zero production cost, viral economics")]
	techStatus=[(0.0,"Unknown"),(-1.0,"Key reason for failure, or current serious issues"),(0.5,"Highly sceptical of feasability"),(1.0,"Clever technical narrative with multiple back up plans"),(1.5,"Theoretically feasible in >5 years"),(2.0,"Theoretically feasible in >2 years"),(2.5,"Theoretically feasible in <2 years"),(3.0,"Lab scale proven"),(3.5,"Demonstrator scale proven"),(5.5,"Proven at scale")]
	tracStatus=[(0.0,"Unknown"),(-1.0,"Key reason for failure, or current serious issues"),(0.5,"In extended tech dev phase, no customers"),(1.0,"Evidence of strong pull from customers, clear beachhead"),(1.5,"Proven urgent need exist with LOIs"),(2.0,"First PoC commercial deals signed"),(3.0,"Major deal signed"),(4.0,"Multiple major deals signed")]
	teamStatus=[(0.0,"Unknown"),(-1.0,"Key reason for failure, or current serious issues"),(0.5,"Inexperienced, poor fit or any version of slow moving"),(1.0,"Inexperienced but fast, good fit"),(2.0,"Inexperienced, good fit, with experienced advisors"),(2.5,"Experienced but without great record"),(3.5,"Experienced proven team"),(5.5,"Serial entrepreneurs or other big names")]
	fundingStatus=[(0.0,"Unknown"),(-1.0,"Key reason for failure, or current serious issues"),(0.5,"No upstream investor pull or grants only"),(1.0,"Strong upstream investor interest"),(1.5,"Seed closed"),(2.0,"Seed HQ investors"),(2.5,"Series A closed"),(3.0,"Series A HQ investors"),(3.5,"Growth"),(4.0,"Growth HQ investors"),(4.5,"Minor exit (10s millions)"),(5.0,"Mid sized exit (100s millions)"),(5.5,"Major exit (billions)")]
	clinicalStatus=[(0.0,"Unknown"),(-1.0,"Key reason for failure, or current serious issues"),(1.0,"Pre-clinical invitro"),(2.0,"Pre-clinical invivo"),(3.0,"Phase 1"),(4.0,"Phase 2"), (5.0,"Phase 3"), (6.0,"Sold / Partnership")]
	defaultOptions=[(0.0, 'Error - options failed to load')]


	marketStatus=["Key reason for failure, or current serious issues", "Unknown","No market identified","Single small market -100s millions. Low growth","Single small market - 100s millions. High growth","Single mid-sized market low billons. Low growth","Single mid-sized market - low billons. High growth","Multiple mid-sized growing markets","Single huge market - multi billions, low growth","Single huge market -multi billions. High growth","Multiple large markets. Not growing","Multiple large markets. High growth"]


	print(list(reqandsolpivot)) # gets column names

	# Two subplots, unpack the axes array immediately
	f, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(9, 3))
	#fig, axes = plt.subplots(nrows=2, ncols=2)
	#reqandsolpivot.plot(subplots=True, layout=(1,5), sharey=True, figsize=(9, 4))

	#allbutfunding = reqandsolpivot.drop('Funding status', axis=1)
	#for i in range(0,len(allbutfunding))
	##	print(reqandsolpivot[])

	# for each column that's not funding create a subplot

	reqandsolpivot.plot(ax=ax1,kind='scatter', x='Breadth potential of platform', y='Funding status', label='Breadth of platform', c='red')
	
	reqandsolpivot.plot(ax=ax2,kind='scatter', x='Scalability of technology (Autologous vs. Allogeneic)', y='Funding status', label='Scalability of manufacture', c='blue')
	ax1.set_xlabel('')
	ax2.set_xlabel('')
	#ax1.plot(x, y)
	ax1.set_title('Breadth vs. Funding')

	ax1.set_yticklabels(fundingStatus, rotation=90)
 	#ax1.set_xticklabels(df.C, )
	ax1.legend().set_visible(False)
	ax2.legend().set_visible(False)
	ax2.set_title('Scalability vs. funding')

	
	#reqandsolpivot.plot(ax=ax3,x=["Breadth potential of platform", "Scalability of technology (Autologous vs. Allogeneic)"], y="Funding status", kind="scatter")
	#ax2.scatter(x, y)
	#ax2.set_title('Vs. deals')
	#ax3.scatter(x, y)
	#ax3.set_title('Vs. clinical milestones')
		#sns.set()
	#sns.set(style="ticks", color_codes=True)
	#sns.pairplot(reqandsolpivot)



		#g = sns.pairplot(reqandsolpivot, kind="reg")
	#g = g.map_diag(plt.hist)
	#g = g.map_offdiag(plt.scatter)
	#g = g.map(plt.scatter)
	


	buffer = io.BytesIO()
	canvas = pylab.get_current_fig_manager().canvas
	canvas.draw()
	graphIMG = PIL.Image.frombytes('RGB', canvas.get_width_height(), canvas.tostring_rgb())
	graphIMG.save(buffer, "PNG")
	pylab.close()

	return HttpResponse (buffer.getvalue(), content_type="Image/png")


def index(request):
	if not request.user.is_authenticated:
		return redirect('/')
	else:


		# GET MOST ACTIVE PROJECTS ---------------------
		graknData=client.execute('match $x isa marketneed has name $xn has identifier $xi; (solvedby:$b, $x); $b has name $bn; get $xn, $xi, $bn;')
		vbps=[]
		vbpsIDs={}
		for x in graknData:
			vbp=(x['xn']['value'])
			vbpsIDs[x['xn']['value']] = x['xi']['value']
			vbps.append(vbp)

		print(vbps)	
		c = Counter(vbps).most_common(10)

		popularProjects=[]
		
		for item in c:

			entry = {'name':item[0], 'number': item[1], 'identifier':vbpsIDs[item[0]]}
			popularProjects.append(entry)
		
		print("popularProjects:")
		print(popularProjects)

		
		# GET MOST ACTIVE USERS -------------------------


		graknData=client.execute('match $x isa product has name $n; (createdby:$x, $b); $b has name $bn; get $bn, $n;')
		graknData.extend(client.execute('match $x isa marketneed has name $n; (createdby:$x, $b); $b has name $bn; get $bn, $n;'))
		graknData.extend(client.execute('match $x isa technology has name $n; (createdby:$x, $b); $b has name $bn; get $bn, $n;'))


		names=[]
		for x in graknData:
			name=(x['bn']['value'])
			names.append(name)

		c = Counter(names).most_common(10)	

		namesList=[]		
		for item in c:

			entry = {'name':item[0], 'number': item[1]}
			namesList.append(entry)	

		
			

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
		solutioncount = client.execute('match $x isa solutionaxis; aggregate count;')
		products = client.execute('match $x isa product; aggregate count;')
		people = client.execute('match $x isa person; aggregate count;')
	


		context = {'projects': projects, 'namesList':namesList,'popularProjects':popularProjects, 'vbps':vbps,'title': 'Index','projectlink': 'addcompetitor', 'vbpslink':'marketanalysis', 'updates': updates, 'marketneedcount':marketneedcount, 'requirementcount': requirementcount, 'solutioncount': solutioncount, 'products': products, 'people': people}


		


		return render(request, 'interface/index.html', context)	
		

def allproducts(request):
	if not request.user.is_authenticated:
		return redirect('/')
	else:
		graknData=client.execute('match $x isa product, has name $y, has identifier $z; order by $y asc; get $y, $z;') # dictionaries are nested structures
		
		# itterate thought results and put into dict -don't know why cna't access dict in the teplate when can on the command line
		projects=[]
		for x in graknData:
			project={'name':x['y']['value'],'id':x['z']['value']}
			projects.append(project)

		context = {'graknData': projects,'title': 'All Companies','link': 'addProduct','addlink':'addProduct'}
		return render(request, 'interface/viewall.html', context)
		# database access here	


def allcompanies(request):
	if not request.user.is_authenticated:
		return redirect('/')
	else:
		graknData=client.execute('match $x isa company, has name $y, has identifier $z; order by $y asc; get $y,$z;') # dictionaries are nested structures
		
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
			name="N/A"
			summary="N/A"
			size=0
			CAGR=0
			if graknData:
				name = graknData[0]['n']['value']
				summary = graknData[0]['s']['value']
				size = graknData[0]['m']['value']
				CAGR = graknData[0]['c']['value']
			#competitors = ['Competitor 1 | Status: Selling | Tech: CRISPR Editing | Customers: Novartis | Funding: £26m | Exit: N/A','competitor2','competitor3']
			
			competitors=client.execute('match $x isa marketneed, has identifier "'+identifier+'"; (solvedby:$b, $x); $b has name $n, has identifier $i; get $n, $i;')

			# NEED O EXTEND FOR EACH SUB AREA - BEWARE DIFFERENT REQUIREMENTS ******************* OR COMPARE ON ONE PAGE?
			
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

	
			# find all companies attatched to a market need, find all their requirements (importance, confidence), find all their solutionaxis (statusfloat)


			reqandsol = client.execute('match $marketidentifier has identifier "'+identifier+'"; (solvedby:$m, $marketidentifier); $m has name $productname; (productrequirement: $pr, requirementproduct: $m), has statusfloat $statusfloat; $pr has name $reqname, has importance $reqimp; get $productname, $reqname, $statusfloat, $reqimp;')
			
			# put into a Pandas dataframe
			reandsolflt=[]
			for i in range(0,len(reqandsol)):
				flt = ([reqandsol[i]['productname']['value'], reqandsol[i]['reqname']['value'], reqandsol[i]['statusfloat']['value'], reqandsol[i]['reqimp']['value']])
				reandsolflt.append(flt)
		
			reqandsoldf = pd.DataFrame(reandsolflt, columns = ["Product","Requirement","Status","Importance"])

			reqandsolpivot = reqandsoldf.pivot(index='Product', columns='Requirement', values='Status').head()
	
			reqandsoldf.set_index(['Requirement'], inplace=True)

			reqandsoldf.sort_index(inplace=True)

			reqandsolhtml = reqandsolpivot.to_html(classes="table")




			# for each company
			# get it's requirements and matching solutions - in one go, no solutuons doesn't matter
			# solstatus=client.execute('match $pr has identifier "'+req['iden']['value']+'"; $rp has identifier "'+identifier+'"; (productrequirement: $pr, requirementproduct: $rp) has statusfloat $solstatus; get;')
			#directAndIndirectReqs.extend(client.execute('match $i has identifier "'+identifier+'"; (solvedby:$m, $i); (requiremententity: $c, $m); $c has name $n, has identifier $iden, has importance $p, has category $cat; (productrequirement: $pr, requirementproduct: $c) has statusfloat $solstatus; get;'))
			
			# directAndIndirectReqs.extend(client.execute('match $i has identifier "'+identifier+'"; (solvedby:$i, $m); (topmarketneed: $y, lowermarketneed: $m); (requiremententity: $c, $y); $c has name $n, has identifier $iden, has importance $p, has category $cat; (productrequirement: $pr, requirementproduct: $c) has statusfloat $solstatus; get;'))
			# Add product name to this!
			# extend them into an array

			#


			if requirementssarray:

				print("-------")		

				for comp in competitors:
					performanceArray=[]
					rArray=[]
					performanceArray.append({'val':comp['n']['value'],'col':'light','id':comp['i']['value']})
					score=0

					for req in requirementssarray: # something wacky with append above requires this zero
						# find if the requirement has any solutions associated specifically for this product (built the relationship but couldn't get to work in one command so using product id as a key, could be better)
						#sol = client.execute('match $x isa requirement, has identifier "'+req['id']+'"; (solution:$b, $x); $b has name $n, has productid "'+comp['i']['value']+'", has identifier $i, has status $s, has confidence $co; get $n, $i, $s, $co;')

						#sol = client.execute('match $x isa requirement, has identifier "'+req['id']+'"; (solution:$b, $x); $b has name $n, has productid "'+comp['i']['value']+'", has identifier $i, has status $s, has confidence $co; get $n, $i, $s, $co;')
						

			
						sol = client.execute('match $x has identifier "'+req['id']+'"; $y has identifier "'+comp['i']['value']+'"; (productrequirement: $x, requirementproduct: $y) isa solutionaxis, has statusfloat $s; get;')
						
						if sol:
							sol=sol[0]

							# work out the score fresh like bakers bread
							score += (rankingdict[float(req['importance'])]*float(sol['s']['value'])) # int to round down
							# save said score for quick access from other pages

							performanceArray.append({'val':float(sol['s']['value']), 'col':'success'})
							rArray.append(float(sol['s']['value']))

							highlight="light"
							if float(sol['s']['value'])<2:
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

		context = {'title': 'Define Venture Backable Problem','link': 'addmarketneed', 'marketneeddata': marketneeddata, 'radarArrayAll': radarArrayAll, 'reqNameArray': reqNameArray, 'reqandsolhtml': reqandsolhtml}
		
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


def get_questions(identifier):
	directAndIndirectReqs=[]
	if identifier != None:
		# get all of the direct requirements via the product id
		directAndIndirectReqs.extend(client.execute('match $i has identifier "'+identifier+'"; (solvedby:$i, $m); (requiremententity: $c, $m); $c has name $n, has identifier $iden, has importance $p, has category $cat; get;'))
	
		#get all indirect requirements
		#print("direct length:",len(directAndIndirectReqs))
		directAndIndirectReqs.extend(client.execute('match $i has identifier "'+identifier+'"; (solvedby:$i, $m); (topmarketneed: $y, lowermarketneed: $m); (requiremententity: $c, $y); $c has name $n, has identifier $iden, has importance $p, has category $cat; get;'))
	

		#  (productrequirement: $c, requirementproduct: $i) isa solutionaxis, has status $solstatus;
		# reqStatusArray = []
		# for req in the directAndIndirectReqs
		# 	solstatus=client.execute('(productrequirement: '+req[0]['c']+', requirementproduct: '+req[0]['i']+') isa solutionaxis, has status $solstatus')
		#	reqStatusArray.extend(solstatus[0]['solstatus'][value])
	return directAndIndirectReqs


def addProduct(request):
	
	if not request.user.is_authenticated:
		return redirect('/')
	else:
		identifier = ""
		marketid = ""
		if request.method == 'POST':
			identifier = request.POST.get('mode') # Needs the ID to load questions even on POST
		if request.method == 'GET':
			identifier = request.GET.get('id')
		marketid = request.GET.get('marketid')
		action = 'addProduct'
		pagetitle='Add Product'
		addlink = 'addProduct'	
		extra_questions=[]
		extra_questions = get_questions(identifier)

		if request.method == 'POST':	
			form = addProduct2Form(request.POST, extra=extra_questions, identifier=identifier, marketid=marketid)
		

			if form.is_valid():
				identifier = form.cleaned_data['mode'] # passed over only if form was in edit mode
				name = form.cleaned_data['name']
				summary = form.cleaned_data['summary']
				summary = html.escape(form.cleaned_data['summary'],quote=True)
				companychoice = form.cleaned_data['companychoice']
				marketneedchoice = form.cleaned_data['marketneedchoice']
				technologychoice = form.cleaned_data['technologychoice']

				if identifier != "": # i.e. we're in edit mode delete previous entity first
					print("updating")
					client.execute('match $x isa product, has name $n, has summary $s, has identifier "'+identifier+'"; delete $n, $s;')
					client.execute('match $x has identifier "'+identifier+'"; insert $x has name "' +name+'", has summary "' +summary+'", has updated '+str(datetime.datetime.now().date())+';')
					
					client.execute('match $r ($x) isa productownership; $x isa product, has identifier "'+identifier+'"; delete $r;')
					client.execute('match $r ($x) isa producstisinmarket; $x isa product, has identifier "'+identifier+'"; delete $r;')

					client.execute('match $r ($x) isa solutionaxis; $x isa product, has identifier "'+identifier+'"; delete $r;')
					client.execute('match $r ($x) isa technologystack; $x isa product, has identifier "'+identifier+'"; delete $r;')
					#solutionaxis connects the product and requirement, data is storated on the relationship



				else:
					# don't delete anything and create new identifier
					identifier = str(uuid.uuid4())
					client.execute('insert $x isa product, has name "' +name+'", has summary "' +summary+'", has identifier "' +identifier+'", has updated '+str(datetime.datetime.now().date())+';')

				client.execute('match $x has identifier "'+identifier+'"; $y has identifier "'+companychoice+'"; insert (productowner: $y, companyproduct: $x) isa productownership;')
				client.execute('match $x isa person, has email "'+request.user.email+'"; $y isa product, has identifier "'+identifier+'"; insert (createdby: $y, creator: $x) isa owner;') # NOTE THIS RELATIONSHIP IS SPELT INCORRECLTY IN THE GRAPH
				
				for tech in technologychoice:
					client.execute('match $x has identifier "'+identifier+'"; $y has identifier "'+tech+'"; insert (usestech: $x, usedinproduct: $y) isa technologystack;') # NOTE THIS RELATIONSHIP IS SPELT INCORRECLTY IN THE GRAPH

				for mar in marketneedchoice:
					client.execute('match $x has identifier "'+identifier+'"; $y has identifier "'+mar+'"; insert (need: $y, solvedby: $x) isa producstisinmarket;') # NOTE THIS RELATIONSHIP IS SPELT INCORRECLTY IN THE GRAPH

				for (question, answer) in form.extra_answers():
					client.execute('match $x has identifier "'+identifier+'"; $y has identifier "'+question[3:]+'"; insert (productrequirement: $y, requirementproduct: $x) isa solutionaxis, has identifier "sol_'+question[3:]+'", has statusfloat '+answer+';')
					print(".")


				messages.success(request, 'Saved')
				returnstring = "/explore/addcompetitor?id="+identifier
				return redirect(returnstring) # this is a hack to get it to reload - use AJAX in the future

		else:
			print("no updating, no editing")
			if identifier:
				extra_questions = get_questions(identifier)
				print("identifier found, extra sent")

				form = addProduct2Form(extra=extra_questions, identifier=identifier, marketid=marketid)
			else:
				print("no identifier")
				form = addProduct2Form(marketid=marketid)
	
	

		return render(request, "interface/addCompetitor.html", {'form': form, 'action': action, 'addlink': addlink})	





def addcompetitor(request):

	if not request.user.is_authenticated:
		return redirect('/')
	else:
		identifier=None
		identifier = request.GET.get('id')
		action = 'addcompetitor'
		pagetitle='Add Competitor'

		requirementssarray=[]
		marketid = request.GET.get('marketid')


		directAndIndirectReqs = []
		extra=[]
		if identifier:
			print("extra is completed")
			# get all of the direct requirements via the product id
			directAndIndirectReqs.extend(client.execute('match $i has identifier "'+identifier+'"; (solvedby:$i, $m); (requiremententity: $c, $m); $c has name $n, has identifier $iden, has importance $p, has category $cat; get;'))

			#get all indirect requirements
			directAndIndirectReqs.extend(client.execute('match $i has identifier "'+identifier+'"; (solvedby:$i, $m); (topmarketneed: $y, lowermarketneed: $m); (requiremententity: $b, $y); $b has name $n, has identifier $iden, has importance $p, has category $cat; get;'))
			
		if request.method == 'POST':	

			form = addCompetitorForm(extra=directAndIndirectReqs, identifier=identifier, marketid=marketid, data=request.POST) 

			print(request.POST)	
			if form.is_valid():	



				for (question, answer) in form.extra_fields():
					print(question)
					print(answer)

				print("^^^^")	
				print(form.cleaned_data)
					
				identifier = form.cleaned_data['mode'] # passed over only if form was in edit mode
				name = form.cleaned_data['name'].encode('utf-8').decode('latin-1')
				summary = form.cleaned_data['summary'].encode('utf-8').decode('latin-1')
				summary = html.escape(form.cleaned_data['summary'],quote=True)
				companychoice = form.cleaned_data['companychoice']
				marketneedchoice = form.cleaned_data['marketneedchoice']

				if identifier: # i.e. we're in edit mode delete previous entity first
					client.execute('match $x isa product, has name $n, has summary $s, has identifier "'+identifier+'"; delete $n, $s;')
					client.execute('match $x has identifier "'+identifier+'"; insert $x has name "' +name+'", has summary "' +summary+'", has updated '+str(datetime.datetime.now().date())+';')
					
					client.execute('match $r ($x) isa productownership; $x isa product has identifier "'+identifier+'"; delete $r;')
					client.execute('match $r ($x) isa producstisinmarket; $x isa product has identifier "'+identifier+'"; delete $r;')		
				else:
					# don't delete anything and create new identifier
					identifier = str(uuid.uuid4())
					client.execute('insert $x isa product, has name "' +name+'", has summary "' +summary+'", has identifier "' +identifier+'", has updated '+str(datetime.datetime.now().date())+';')

				client.execute('match $x has identifier "'+identifier+'"; $y has identifier "'+companychoice+'"; insert (productowner: $y, companyproduct: $x) isa productownership;')
				client.execute('match $x isa person, has email "'+request.user.email+'"; $y isa product, has identifier "'+identifier+'"; insert (createdby: $y, creator: $x) isa owner;') # NOTE THIS RELATIONSHIP IS SPELT INCORRECLTY IN THE GRAPH
				client.execute('match $x has identifier "'+identifier+'"; $y has identifier "'+marketneedchoice+'"; insert (need: $y, solvedby: $x) isa producstisinmarket;') # NOTE THIS RELATIONSHIP IS SPELT INCORRECLTY IN THE GRAPH
				messages.success(request, 'Saved')

		else: #method get
			form = addCompetitorForm(extra=extra, identifier=identifier, marketid=marketid) 		

			marketid = client.execute('match $x isa product, has identifier "' +identifier+'"; (solvedby:$x, $b); $b has identifier $i; get $i;')
			sitswithinmarkets = client.execute('match $x isa marketneed, has identifier "' +marketid[0]['i']['value']+'"; (lowermarketneed:$x, $b); $b has identifier $i; get $i;')	

			allmarkets=[]
			if marketid:
				allmarkets.append(marketid[0]['i']['value'])

			if sitswithinmarkets:	
				for s in range(0,len(sitswithinmarkets)):
					allmarkets.append(sitswithinmarkets[s]['i']['value'])	

		
			allrequirements=[]
			if allmarkets:
				for market in allmarkets:
					requirements=client.execute('match $x isa marketneed, has identifier "'+market+'"; (requiremententity:$b, $x); $b has name $n, has identifier $i, has category $c, has importance $p; get $n, $i, $c, $p;')
					allrequirements.append(requirements)
					


			#	if sitswithinmarkets:
			#		for i in range(0,len(sitswithinmarkets)):
			#			req2 = client.execute('match $x isa marketneed, has identifier "'+sitswithinmarkets[i]['i']['value']+'"; (requiremententity:$b, $x); $b has name $n, has identifier $i; get $n, $i;')

			#		for req in req2:
			#			requirementssarray.append({'name':req['n']['value'],'id':req['i']['value']})	
	



			requirementssarray = []	
			if directAndIndirectReqs:

				for req in directAndIndirectReqs: # something wacky with append above requires this zero
					# find if the requirement has any solutions associated specifically for this product (built the relationship but couldn't get to work in one command so using product id as a key, could be better)
					sol = client.execute('match $x isa requirement, has identifier "'+req['iden']['value']+'"; (solution:$b, $x); $b has name $n, has productid "'+identifier+'", has identifier $i, has status $s, has confidence $co; get $n, $i, $s, $co;')
					
					if sol:

						sol=sol[0]

						highlight="light"
						if int(sol['s']['value'])<2:
							highlight="danger"
						else:
							highlight="success"	


						requirementssarray.append({'name':req['n']['value'],'requirementid':req['iden']['value'],'category':req['cat']['value'], 'importance':req['p']['value'],
						'solutionname': sol['n']['value'],'solutionid': sol['i']['value'], 'status': sol['s']['value'], 'confidence': sol['co']['value'], 'productid':identifier, 'marketid':marketid, 'highlight':highlight})		
					else:
						requirementssarray.append({'name':req['n']['value'],'requirementid':req['iden']['value'],'category':req['cat']['value'], 'importance':req['p']['value'],
						'solutionname': 'Add new','solutionid': "", 'status': 'None', 'confidence': 'None','productid':identifier, 'marketid':marketid, 'highlight':"danger"})		
									

			pagetitle='Edit Product'		
	


	return render(request, 'interface/addCompetitor.html', {'form': form, 'action': action, 'pagetitle': pagetitle, 'requirements': requirementssarray, 'marketid': marketid})	




			


def addcompany(request):

	if not request.user.is_authenticated:
		return redirect('/')
	else:
		action = 'addcompany'
		pagetitle='Add Company'
		identifier=None
		identifier = request.GET.get('id')


		if request.method == 'POST':
			form = addCompanyForm(data=request.POST) 
			if form.is_valid():	
				
				identifier = form.cleaned_data['mode'] # passed over only if form was in edit mode

				name = form.cleaned_data['name']
				summary = form.cleaned_data['summary']
				summary = html.escape(form.cleaned_data['summary'],quote=True)

				productownership = form.cleaned_data['productownership']
				marketneedchoice = form.cleaned_data['marketneedchoice']
				fundingstage = form.cleaned_data['fundingstage']


				if identifier: # i.e. we're in edit mode delete previous entity first
					client.execute('match $x isa company, has identifier "'+identifier+'", has name $n, has summary $s, has fundingstage $f; delete $n, $s, $f;')
					client.execute('match $x has identifier "'+identifier+'"; insert $x has name "' +name+'", has summary "' +summary+'", has fundingstage "'+fundingstage+'", has updated '+str(datetime.datetime.now().date())+';')

					# Delete specific relationships
					client.execute('match $r ($x) isa custom; $x isa company has identifier "'+identifier+'"; delete $r;')
					client.execute('match $r ($x) isa productownership; $x isa company has identifier "'+identifier+'"; delete $r;')		

				else:
					# don't delete anything and create new identifier
					identifier = str(uuid.uuid4())
					client.execute('insert $x isa company, has name "'+name+'", has summary "'+summary+'", has fundingstage "'+fundingstage+'", has identifier "'+identifier+'", has updated '+str(datetime.datetime.now().date())+';')


				
				client.execute('match $x isa person, has email "'+request.user.email+'"; $y isa company, has identifier "'+identifier+'"; insert (createdby: $y, creator: $x) isa owner;') # NOTE THIS RELATIONSHIP IS SPELT INCORRECLTY IN THE GRAPH


				for ch in marketneedchoice:
					client.execute('match $x has identifier "'+identifier+'"; $y has identifier "'+ch+'"; insert (buyer: $y, customer: $x) isa custom;') # NOTE THIS RELATIONSHIP IS SPELT INCORRECLTY IN THE GRAPH

				for po in productownership:	
					client.execute('match $x has identifier "'+identifier+'"; $y has identifier "'+po+'"; insert (productowner: $x, companyproduct: $y) isa productownership;')

				messages.success(request, 'Saved')	

			# quick way of seeing if these are working: match (productowner: $y, companyproduct: $x) isa productownership; offset 0; limit 30; get;
		else:
			if identifier:
				form = 	addCompanyForm(identifier=identifier) #THIS IS PASSING BACK TO THE FORM, BIT WEIRD
			else:
				marketid = request.GET.get('marketid')
				if marketid:
					form = 	addCompanyForm(marketid=marketid) # i.e. we've just asked for a fresh form
				else:
					form = addCompanyForm(identifier=identifier)	

		return render(request, 'interface/addentity.html', {'form': form, 'action': action, 'pagetitle': pagetitle})	







def addrequirement(request):
	
	if not request.user.is_authenticated:
		return redirect('/')
	else:
		action = 'addrequirement'
		pagetitle='Add Requirement'
		indentifier=None
		identifier = request.GET.get('id')


		if request.method == 'POST':
			form = addRequirementForm(data=request.POST) 
			if form.is_valid():	
				
				name = form.cleaned_data['name'].encode('utf-8').decode('latin-1')
				summary = html.escape(form.cleaned_data['summary'],quote=True)
				importance = form.cleaned_data['importance'].encode('utf-8').decode('latin-1')
				confidence = form.cleaned_data['confidence'].encode('utf-8').decode('latin-1')
				marketchoice = form.cleaned_data['marketchoice'].encode('utf-8').decode('latin-1')
				category = form.cleaned_data['category'].encode('utf-8').decode('latin-1')

				identifier = form.cleaned_data['mode'] # passed over only if form was in edit mode

				if identifier: # i.e. we're in edit mode delete previous entity first
					client.execute('match $x isa requirement, has identifier "'+identifier+'", has name $n, has summary $s, has confidence $c, has importance $st, has category $ca; delete $n, $s;')
					#### ***** DON'T DELETE SHARED ATTRIBUTSE BUT SHOULD DELETE RELATIONSHIP TOO THEM, CURRENTLY KEEPING HISTORY ******

					client.execute('match $x isa requirement, has identifier "'+identifier+'"; insert $x has name "'+name+'", has summary "'+summary+'", has importance '+importance+', has confidence '+confidence+', has category "'+category+'", has updated '+str(datetime.datetime.now().date())+';')
					print("added new info")

					# Delete specific relationships
					client.execute('match $r ($x) isa requirementconnection; $x isa requirement has identifier "'+identifier+'"; delete $r;')
					print("deleted relationships")
					

					# DON'T KNOW WHY SHOULDN'T DELETE IN THIS CASE - IF YOU DO IT DELETES ANOTHER RELATIONSHIP???!	
				else:
					# don't delete anything and create new identifier
					identifier = str(uuid.uuid4())
					print("else branch")

					client.execute('insert $x isa requirement, has name "'+name+'", has summary "'+summary+'", has identifier "'+identifier+'", has importance '+importance+', has confidence '+confidence+', has category "'+category+'", has updated '+str(datetime.datetime.now().date())+';')
					print("added new info on new requirement")

				client.execute('match $x has identifier "'+identifier+'"; $y has identifier "'+marketchoice+'"; insert (hasrequirement: $y, requiremententity: $x) isa requirementconnection;')
				print("inserted relationships")	

				client.execute('match $x isa person, has email "'+request.user.email+'"; $y isa requirement, has identifier "'+identifier+'"; insert (createdby: $y, creator: $x) isa owner;') # NOTE THIS RELATIONSHIP IS SPELT INCORRECLTY IN THE GRAPH

				messages.success(request, 'Saved')

				return redirect("/explore/marketanalysis?id="+marketchoice) # this is a hack to get it to reload - use AJAX in the future

				# quick way of seeing if these are working: match (productowner: $y, companyproduct: $x) isa productownership; offset 0; limit 30; get;
		else:
			if identifier:
				form = 	addRequirementForm(identifier=identifier) #THIS IS PASSING BACK TO THE FORM, BIT WEIRD
				print("1")
			else:
				marketid = request.GET.get('marketid')
				if marketid:
					form = 	addRequirementForm(marketid=marketid, identifier=identifier) # i.e. we've just asked for a fresh form
					print("2")
				else:
					form = 	addRequirementForm(identifier=identifier)
					print("3")
		

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


				name = form.cleaned_data['name'].encode('utf-8').decode('latin-1')
				summary = html.escape(form.cleaned_data['summary'],quote=True)

				confidence = form.cleaned_data['confidence'].encode('utf-8').decode('latin-1')
				state = form.cleaned_data['state'].encode('utf-8').decode('latin-1')
				#category = form.cleaned_data['category'].encode('utf-8').decode('latin-1')
				requirement = form.cleaned_data['requirement'].encode('utf-8').decode('latin-1')



				if identifier: # i.e. we're in edit mode delete previous entity first
					client.execute('match $x isa solutioncomponent, has identifier "'+identifier+'", has name $n, has summary $s, has confidence $c, has status $st; delete $n, $s, $c, $st;')
					client.execute('insert $x isa solutioncomponent, has identifier "' +identifier+'"; insert $x has name "'+name+'", has summary "' +summary+'", has productid "'+productid+'", has confidence ' +confidence+', has status ' +state+', has updated '+str(datetime.datetime.now().date())+';')

					client.execute('match $r ($x) isa requirementmatch; $x isa solutioncomponent has identifier "'+identifier+'"; delete $r;')		
					# DON'T KNOW WHY THIS DELETE STATEMENT IS CAUSING ISSUES

				else:
					# don't delete anything and create new identifier
					identifier = str(uuid.uuid4())

					client.execute('insert $x isa solutioncomponent, has name "'+name+'", has summary "' +summary+'", has productid "'+productid+'", has identifier "' +identifier+'", has confidence ' +confidence+', has status ' +state+', has updated '+str(datetime.datetime.now().date())+';')

				client.execute('match $x has identifier "'+identifier+'"; $y has identifier "'+requirement+'"; insert (requiressolution: $y, solution: $x) isa requirementmatch;')

				#client.execute('match $x has identifier "'+identifier+'"; $y has identifier "'+productid+'"; insert (productincludessolution: $y, solution: $x) isa relatedtoproduct;')

				client.execute('match $x isa person, has email "'+request.user.email+'"; $y isa solutioncomponent, has identifier "'+identifier+'"; insert (createdby: $y, creator: $x) isa owner;') # NOTE THIS RELATIONSHIP IS SPELT INCORRECLTY IN THE GRAPH


		else:

			reqid = None
			productid = None
			solutionid = None
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
		pagetitle = "Define Opportunity area"
		identifier=None
		identifier = request.GET.get('id')
		if request.method == 'POST':
			form = addMarketNeedForm(data=request.POST) 
			if form.is_valid():


				name = form.cleaned_data['name'].encode('utf-8').decode('latin-1')
				summary = form.cleaned_data['summary'].encode('utf-8').decode('latin-1')
				#marketchoice = form.cleaned_data['marketchoice']
				marketsize = form.cleaned_data['marketsize']
				marketcagr = form.cleaned_data['marketcagr']
				sitswithinmarketchoice = form.cleaned_data['sitswithinmarketchoice']

				

				identifier = form.cleaned_data['mode'] # passed over only if form was in edit mode

				if identifier: # i.e. we're in edit mode delete previous entity first

					client.execute('match $x isa marketneed, has identifier "'+identifier+'", has name $n, has summary $s; delete $n, $s;')
					client.execute('match $x has identifier "'+identifier+'"; insert $x has name "' +name+'", has summary "' +summary+'", has marketsize '+marketsize+', has CAGR '+marketcagr+', has updated '+str(datetime.datetime.now().date())+';')
					print("saving in marketneed")	
					# Delete specific relationships
					client.execute('match $r ($x) isa marketneediswithinmarketneed; $x isa marketneed has identifier "'+identifier+'"; delete $r;')	
				else:
					# don't delete anything and create new identifier
					identifier = str(uuid.uuid4())
					client.execute('insert $x isa marketneed, has name "' +name+'", has summary "' +summary+'", has marketsize '+marketsize+', has CAGR '+marketcagr+', has identifier "' +identifier+'", has updated '+str(datetime.datetime.now().date())+';')
				

				client.execute('match $x isa person, has email "'+request.user.email+'"; $y isa marketneed, has identifier "'+identifier+'"; insert (createdby: $y, creator: $x) isa owner;') # NOTE THIS RELATIONSHIP IS SPELT INCORRECLTY IN THE GRAPH

				for ch in sitswithinmarketchoice:
					#print("choice:",ch)
					client.execute('match $x has identifier "'+identifier+'"; $y has identifier "'+ch+'"; insert (topmarketneed: $y, lowermarketneed: $x) isa marketneediswithinmarketneed;') # NOTE THIS RELATIONSHIP IS SPELT INCORRECLTY IN THE GRAPH
		
			messages.success(request, 'Saved')
			return redirect("/explore/allmarketneeds")
					
				# relate to a market

		else:
			
			form = 	addMarketNeedForm(identifier=identifier) # identifier goes back with blank form so that can make subsequent edits
			
			
			guidance = "What is the size of this opportunity? How many people or companies are *directly* affected? What is the cost of that suffering per person or company? What is the rate of growth of those costs or the wider issue? What budget to customers have to solve this specific problem? Are they looking to urgently solve it at the moment? Could this really be venture scale (£100m+ sales per year)?"		

			return render(request, 'interface/addentity.html', {'form': form, 'action': action, 'pagetitle': pagetitle, 'guidance': guidance})





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

		context = {'graknData': allentities,'title': 'All Technolgies','link': 'addtechnology', 'addlink': 'addtechnology'}
		return render(request, 'interface/viewall.html', context)
		# database access here		
#

################################################# END OF VIEW ONLYs ###################################################


def addtechnology(request):
	if not request.user.is_authenticated:
		return redirect('/')
	else:
		action = 'addtechnology'
		if request.method == 'POST':
			form = addTechnologyForm(data=request.POST) 
			if form.is_valid():
				

				identifier = form.cleaned_data['mode'] # passed over only if form was in edit mode

				name = form.cleaned_data['name'].encode('utf-8').decode('latin-1')
				summary = form.cleaned_data['summary'].encode('utf-8').decode('latin-1')
				technologychoice = form.cleaned_data['technologychoice']

				if identifier: # i.e. we're in edit mode delete previous entity first
					
					client.execute('match $x isa technology, has identifier "'+identifier+'", has name $n, has summary $s; delete $n, $s;')
					client.execute('match $x isa technology, has identifier "'+identifier+'"; insert $x has name "'+name+'", has summary "'+summary+'", has updated '+str(datetime.datetime.now().date())+';')
					
					client.execute('match $r ($x) isa technologygroup; $x isa technology has identifier "'+identifier+'"; delete $r;')	

				else:	

					identifier = str(uuid.uuid4())
					client.execute('insert $x isa technology, has name "' +name+'", has summary "' +summary+'", has identifier "' +identifier+'";')
				
				if technologychoice is not "N/A":
					client.execute('match $x has identifier "'+identifier+'"; $y has identifier "'+technologychoice+'"; insert (subtechnology: $y, toptechnology: $x) isa technologygroup;')
				
				client.execute('match $x isa person, has email "'+request.user.email+'"; $y isa technology, has identifier "'+identifier+'"; insert (createdby: $y, creator: $x) isa owner;') # NOTE THIS RELATIONSHIP IS SPELT INCORRECLTY IN THE GRAPH


				messages.success(request, 'Saved')	
		else:
			identifier = request.GET.get('id')
			if identifier:
				form = 	addTechnologyForm(identifier=identifier) #so that the form can load the existing data
			else:
				form = 	addTechnologyForm() # i.e. we've just asked for a fresh form
			
			
		return render(request, 'interface/addentity.html', {'form': form, 'action': action})




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
		return redirect('index')
			

# people

# development strategy

# defensibility strategy

# Funding strategy
