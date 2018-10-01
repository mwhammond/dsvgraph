from django import forms
import grakn
client = grakn.Client(uri='http://35.197.194.67:4567', keyspace='dsvgraph')
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
import html

def getEntries(type):

	graknData=client.execute('match $x isa '+type+', has name $y, has identifier $z; order by $y asc; get;') # dictionaries are nested structures
	entries=[]
	entries.append(("N/A","N/A"))
	for entity in graknData:
		entry=(entity['z']['value'],entity['y']['value'])
		entries.append(entry)
	technologyNames=tuple(entries)

	return entries


#class addProjectForm(forms.Form):
#
#	pagetitle="Add project"
##
#	name = forms.CharField(label="Project title", max_length=100)	
#	summary = forms.CharField(widget=forms.Textarea(attrs={'width':"100%", 'cols' : "80", 'rows': "4", }))
#
#	companychoice = forms.ChoiceField(label='Company owner', choices=getEntries('company'), required=False)
##	businessmodelchoice = forms.ChoiceField(label='Business Model', choices=getEntries('businessmodel'), required=False)
#	technologychoice = forms.MultipleChoiceField(label='Add Technology', choices=getEntries('technology'), required=False)
#	marketneedchoice = forms.MultipleChoiceField(label='Market Need Set', choices=getEntries('marketneed'), required=False)
##
#	mode = forms.CharField(required=False, max_length=50, widget=forms.HiddenInput())
#
#
#
#	def __init__(self,*args,**kwargs):
##		
#		
#		if 'identifier' in kwargs:
#			identifier = kwargs.pop('identifier')
##		else: 
#			identifier=None
#
#		if 'marketid' in kwargs:
##			marketid = kwargs.pop('marketid')
#
#		print("edit mode: ", identifier)
#
##		super(addProjectForm, self).__init__(*args,**kwargs)
#		self.fields['companychoice'] = forms.ChoiceField(label='Company owner', choices=getEntries('company'), required=False)
#		self.fields['businessmodelchoice'] = forms.ChoiceField(label='Business Model', choices=getEntries('businessmodel'), required=False)
#		self.fields['technologychoice'] = forms.MultipleChoiceField(label='Add Technology', choices=getEntries('technology'), required=False)
#		self.fields['marketneedchoice'] = forms.MultipleChoiceField(label='Market Need Set', choices=getEntries('marketneed'), required=False)
#
#
##		if identifier is not None:
#			print("id exists")
#
#			savedNameSelection = graknData=client.execute('match $x isa product, has name $y, has identifier "' +identifier+'"; get;')
#			savedSummarySelection = graknData=client.execute('match $x isa product, has summary $y, has identifier "' +identifier+'"; get;')	
#			companychoiceSelection = graknData=client.execute('match $x isa product, has identifier "' +identifier+'"; (companyproduct:$x, $b); $b has identifier $d; get $d;')	
##			businessmodelchoiceSelection = graknData=client.execute('match $x isa product, has identifier "' +identifier+'"; (usesmodel:$x, $b); $b has identifier $d; get $d;')	
#			technologychoiceSelection = graknData=client.execute('match $x isa product, has identifier "' +identifier+'"; (usestech:$x, $b); $b has identifier $d; get $d;')	 
#			marketneedchoiceSelection = graknData=client.execute('match $x isa product, has identifier "' +identifier+'"; (solvedby:$x, $b); $b has identifier $d; get $d;')	
#
#			if companychoiceSelection:
#				companychoiceSelection=companychoiceSelection[0]['d']['value']
##			if businessmodelchoiceSelection:
#				businessmodelchoiceSelection=businessmodelchoiceSelection[0]['d']['value']
#			if technologychoiceSelection:
#				technologychoiceSelection=technologychoiceSelection[0]['d']['value']
#			if marketneedchoiceSelection:
#				marketneedchoiceSelection=marketneedchoiceSelection[0]['d']['value']
#
##			savedNameSelection = savedNameSelection[0]['y']['value']
#			savedSummarySelection = savedSummarySelection[0]['y']['value']
#
#			# ADD HIDDEN FIELD SO THAT THE VIEW KNOWS THAT THIS IS DELETE THEN ADD MODE
#			self.fields['mode'] = forms.CharField(required=False, max_length=50, widget=forms.HiddenInput(),initial=identifier)
##
			#super(addProjectForm, self).__init__(*args,**kwargs)
#			#self.fields['name'] = forms.ChoiceField(label="Name", choices=[(x.plug_ip, x.MY_DESCRIPTIVE_FIELD) for x in Sniffer.objects.filter(client = myClient)])
#			self.fields['name'] = forms.CharField(label="Project title", max_length=100, initial=savedNameSelection)
#			self.fields['summary'] = forms.CharField(widget=forms.Textarea(attrs={'width':"100%", 'cols' : "80", 'rows': "4"}),initial=savedSummarySelection)
#			
##			self.fields['companychoice'] = forms.ChoiceField(label='Company owner', choices=getEntries('company'), initial=companychoiceSelection, required=False)
#			self.fields['businessmodelchoice'] = forms.ChoiceField(label='Business Model', choices=getEntries('businessmodel'), initial=businessmodelchoiceSelection, required=False)
#			self.fields['technologychoice'] = forms.MultipleChoiceField(label='Technology stack', choices=getEntries('technology'), initial=technologychoiceSelection, required=False)
#			self.fields['marketneedchoice'] = forms.MultipleChoiceField(label='Market Need', choices=getEntries('marketneed'), initial=marketneedchoiceSelection, required=False)
#
#
#
#			pagetitle="Edit project"
##
#		else:
#			print('add mode')
#			self.fields['marketneedchoice'] = forms.MultipleChoiceField(label='Market Need', choices=getEntries('marketneed'), initial=marketid, required=False)
#
#			#mode = forms.CharField(required=False, max_length=50, widget=forms.HiddenInput(),initial='new')
#			#super(addProjectForm, self).__init__(*args,**kwargs)
#
#
#	# get static (rather than edit) data for form


class addProduct2Form(forms.Form):


	def __init__(self, *args, **kwargs):
		if 'extra' in kwargs:
			extra = kwargs.pop('extra')
		else:
			extra=[]	
			
		if 'identifier' in kwargs:
			identifier = kwargs.pop('identifier')
			print("popped")
		else:
			identifier=""

		if 'marketid' in kwargs:	
			marketid = kwargs.pop("marketid")
		else:
			marketid=""
		

		super(addProduct2Form, self).__init__(*args, **kwargs)




		# works out which set of options matches the requirement type
		def options(x):

			binaryStatus=[(0.0, "Unknown"), (5.0, "Yes"), (-1.0, "No")]
			marketStatus=[(0.0,"Unknown"),(-1.0,"Key reason for failure, or current serious issues"),(0.5,"No market identified"),(1.5,"Single small market -100s millions. Low growth"),(2.0,"Single small market - 100s millions. High growth"),(2.5,"Single mid-sized market low billons. Low growth"),(3.0,"Single mid-sized market - low billons. High growth"),(3.5,"Multiple mid-sized growing markets"),(4.0,"Single huge market - multi billions, low growth"),(4.5,"Single huge market -multi billions. High growth"),(5.0,"Multiple large markets. Not growing"),(5.5,"Multiple large markets. High growth")]
			defenseStatus=[(0.0,"Unknown"),(-1.0,"Key reason for failure, or current serious issues"),(0.5,"No defensibility"),(1.5,"Weak IP strategy"),(5.5,"Strong IP strategy")]
			manuStatus=[(0.0,"Unknown"),(-1.0,"Key reason for failure, or current serious issues"),(0.5,"Likely impossible"),(1,"Unsolved, theoretically possible in >5 years"),(1.5,"Unsolved, theoretically possible in >2 years"),(2.0,"Theoretically feasible in <2 years"),(2.5,"Lab scale proven"),	(3.5,"Demonstrator scale proven"),(5.5,"Proven at scale or not relavent")]
			scaleStatus=[(0.0,"Unknown"),(-1.0,"Key reason for failure, or current serious issues"),(0.5,"Expensive to produce, large upfront investment, small margin, limit on production"),(1.0,"Expensive distribution and low margin"),(2.0,"Cheap to produce, large upfront investment, no limit on production, large margin"),(3.0,"Cheap to produce, small upfront investment or distribution costs that needs to be covered, large margin"),(4.0,"Cheap to produce, small upfront investment or ongoing distribution - that will be covered by others, large margin"),(4.5,"Cost decoupled from unit price"),	(5.5,"Near zero production cost, viral economics")]
			techStatus=[(0.0,"Unknown"),(-1.0,"Key reason for failure, or current serious issues"),(0.5,"Highly sceptical of feasability"),(1.0,"Clever technical narrative with multiple back up plans"),(1.5,"Theoretically feasible in >5 years"),(2.0,"Theoretically feasible in >2 years"),(2.5,"Theoretically feasible in <2 years"),(3.0,"Lab scale proven"),(3.5,"Demonstrator scale proven"),(5.5,"Proven at scale")]
			tracStatus=[(0.0,"Unknown"),(-1.0,"Key reason for failure, or current serious issues"),(0.5,"In extended tech dev phase, no customers"),(1.0,"Evidence of strong pull from customers, clear beachhead"),(1.5,"Proven urgent need exist with LOIs"),(2.0,"First PoC commercial deals signed"),(3.0,"Major deal signed"),(4.0,"Multiple major deals signed")]
			teamStatus=[(0.0,"Unknown"),(-1.0,"Key reason for failure, or current serious issues"),(0.5,"Inexperienced, poor fit or any version of slow moving"),(1.0,"Inexperienced but fast, good fit"),(2.0,"Inexperienced, good fit, with experienced advisors"),(2.5,"Experienced but without great record"),(3.5,"Experienced proven team"),(5.5,"Serial entrepreneurs or other big names")]
			fundingStatus=[(0.0,"Unknown"),(-1.0,"Key reason for failure, or current serious issues"),(0.5,"No upstream investor pull or grants only"),(1.0,"Strong upstream investor interest"),(1.5,"Seed closed"),(2.0,"Seed HQ investors"),(2.5,"Series A closed"),(3.0,"Series A HQ investors"),(3.5,"Growth"),(4.0,"Growth HQ investors"),(4.5,"Minor exit (10s millions)"),(5.0,"Mid sized exit (100s millions)"),(5.5,"Major exit (billions)")]
			clinicalStatus=[(0.0,"Unknown"),(-1.0,"Key reason for failure, or current serious issues"),(1.0,"Pre-clinical invitro"),(2.0,"Pre-clinical invivo"),(3.0,"Phase 1"),(4.0,"Phase 2"), (5.0,"Phase 3"), (6.0,"Sold / Partnership")]
			IPOorExitStatus=[(-1.0,"Failed or likely fail"),(0.0,"Unknown"),(0.1,"10m"),(0.2,"20m"),(0.4,"30m"),(0.4,"40m"),(0.5,"50m"),(0.6,"60m"),(0.7,"70m"),(0.8,"80m"),(0.9,"90m"),(1.0,"100m"),(1.1,"110m"),(1.2,"120m"),(1.3,"130m"),(1.4,"140m"),(1.5,"150m"),(1.6,"160m"),(1.7,"170m"),(1.8,"180m"),(1.9,"190m"),(2.0,"200m"),(2.1,"210m"),(2.2,"220m"),(2.3,"230m"),(2.4,"240m"),(2.5,"250m"),(2.6,"260m"),(2.7,"270m"),(2.8,"280m"),(2.9,"290m"),(3.0,"300m"),(4.0,">300m")]

			defaultOptions=[(0.0, 'Error - options failed to load')]

			return {
			"Market size and growth potential": marketStatus,
			"Defensibility": defenseStatus,
			"Manufacturability": manuStatus,
			"Scalability and value capture": scaleStatus,
			"Technical plan feasability": techStatus,
			"Traction": tracStatus,
			"Team fit": teamStatus,
			"Funding viability": fundingStatus,
			"Clinical Stage": clinicalStatus,
			"Binary": binaryStatus,
			"Exit" : IPOorExitStatus
			}.get(x, defaultOptions)    # 9 is default if x not found


		#companystates = [(5, 'Outlier performance'), (4, 'Proven'), (3, 'Theoretically possible'), (2, 'Potentially possible in <2 years'), (1, 'Potentially possible in 2+ years'), (-1, 'Highly skeptical based on evidence'), (0, 'Unknown'), (-2, 'Not working'), (-3, 'Key reason for failure')]	
		self.fields['mode'] = forms.CharField(required=False, max_length=50, widget=forms.HiddenInput())

		self.fields['name'] = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Project name'}), label='Project name')
		self.fields['summary'] = forms.CharField(widget=SummernoteWidget(), label='Description')
		self.fields['companychoice'] = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control','placeholder':'Project name'}), choices=getEntries('company'), label='Part of company')
		self.fields['technologychoice'] = forms.MultipleChoiceField(label='Technologies', choices=getEntries('technology'),required=False)
		self.fields['marketneedchoice'] = forms.MultipleChoiceField(label='Markets', choices=getEntries('marketneed'),required=False,initial=[marketid])


		print("identifier before test:", identifier)
		if identifier != "":
			print("id exists")
			savedNameAndSummary = client.execute('match $x isa product, has name $n, has summary $s, has identifier "'+identifier+'"; get;')
			companychoiceSelection = client.execute('match $x isa product, has identifier "' +identifier+'"; (companyproduct:$x, $b); $b has identifier $d; get $d;')	
			marketneedchoiceSelection = client.execute('match $x isa product, has identifier "' +identifier+'"; (solvedby:$x, $b); $b has identifier $d; get $d;')	
			technologychoiceSelection = client.execute('match $x isa product, has identifier "' +identifier+'"; (usestech:$x, $b); $b has identifier $d; get $d;')	

			if companychoiceSelection:
				companychoiceSelection=companychoiceSelection[0]['d']['value']

			marketArray=[]	
			if marketneedchoiceSelection:
				for market in marketneedchoiceSelection:
					marketArray.append(market['d']['value'])
			
			techArray=[]
			if technologychoiceSelection:
				for tech in technologychoiceSelection:
					techArray.append(tech['d']['value'])
	

			savedNameSelection = savedNameAndSummary[0]['n']['value']
			savedSummarySelection = savedNameAndSummary[0]['s']['value']
			savedSummarySelection = html.unescape(savedSummarySelection)


			########
			#########
			###### LEFT AT TECHNOLOGY CHOICE INITIAL ANSWERS TROWING WEIRD INIT ERROR
			self.fields['mode'] = forms.CharField(required=False, max_length=50, widget=forms.HiddenInput(),initial=identifier)
			self.fields['name'] = name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Project name'}), initial=savedNameSelection, label='Project name')
			self.fields['summary'] = forms.CharField(widget=SummernoteWidget(),initial=savedSummarySelection, label='Description')
			self.fields['companychoice'] = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control'}), label='Part of company', choices=getEntries('company'), initial=companychoiceSelection, required=False)
			self.fields['technologychoice'] = forms.MultipleChoiceField(label='Technologies', choices=getEntries('technology'), initial=techArray, required=False)
			self.fields['marketneedchoice'] = forms.MultipleChoiceField(label='Markets', choices=getEntries('marketneed'),required=False, initial=marketArray)


			for req in extra:
				print(req['n']['value'])
				solstatus=client.execute('match $pr has identifier "'+req['iden']['value']+'"; $rp has identifier "'+identifier+'"; (productrequirement: $pr, requirementproduct: $rp) has statusfloat $solstatus; get;')
				if solstatus:
					savedvalue=solstatus[0]['solstatus']['value']
					
				else:
					savedvalue = 0
				# get the vale on the relationship to the current product, or 0 if none
				self.fields['id_'+req['iden']['value']] = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control'}), label=req['n']['value'], choices=options(req['cat']['value']),initial=savedvalue)

	def extra_answers(self):
		print("extra answers checking in")
		for name, value in self.cleaned_data.items():
			if name.startswith('id_'):
				yield (name, value)		
				print("*")








#class addCompetitorForm(forms.Form):
#
#	name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Project name'}), label='Project name')
##	summary = forms.CharField(widget=SummernoteWidget(), label='Description')
#	companychoice = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control','placeholder':'Project name'}), choices=getEntries('company'), label='Part of company')
#	marketneedchoice = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control'}),label='Market Need Set', choices=getEntries('marketneed'), required=False)
#
#	mode = forms.CharField(required=False, max_length=50, widget=forms.HiddenInput())
##
#
#
#	def __init__(self,*args,**kwargs):
##	
#		if 'identifier' in kwargs:
#			identifier = kwargs.pop('identifier')
#		else:
##			identifier=None	
#
#		if 'marketid' in kwargs:	
#			marketid = kwargs.pop("marketid")
#		else:
#			marketid=0
#			
##		if 'extra' in kwargs:
#			extra = kwargs.pop('extra')
#		else:
#			extra=None		
#
#		super(addCompetitorForm, self).__init__(*args,**kwargs)
#	
##
#		states = [(5, 'Outlier performance'), (4, 'Proven'), (3, 'Theoretically possible'), (2, 'Potentially possible in <2 years'), (1, 'Potentially possible in 2+ years'), (-1, 'Highly skeptical based on evidence'), (-2, 'Not working'), (-3, 'Key reason for failure')]	
#
#
#		self.fields['companychoice'] = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control'}), label='Part of company', choices=getEntries('company'), required=False)
##		self.fields['marketneedchoice'] = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control'}),label='Market Need Set', choices=getEntries('marketneed'), required=False)
#
#		if extra:
#			for req in extra:
#				self.fields['req_%s' % req['iden']['value']] = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control'}),label=req['n']['value'], choices=states, required=False)
#
#
#		if identifier is not None:
#			print("id exists")
##			savedNameAndSummary = client.execute('match $x isa product, has name $n, has summary $s, has identifier "' +identifier+'"; get;')
#			companychoiceSelection = client.execute('match $x isa product, has identifier "' +identifier+'"; (companyproduct:$x, $b); $b has identifier $d; get $d;')	
#			marketneedchoiceSelection = client.execute('match $x isa product, has identifier "' +identifier+'"; (solvedby:$x, $b); $b has identifier $d; get $d;')	
#
#			if companychoiceSelection:
#				companychoiceSelection=companychoiceSelection[0]['d']['value']
#			if marketneedchoiceSelection:
#				marketneedchoiceSelection=marketneedchoiceSelection[0]['d']['value']
#
#			savedNameSelection = savedNameAndSummary[0]['n']['value']
##			savedSummarySelection = savedNameAndSummary[0]['s']['value']
#			savedSummarySelection = html.unescape(savedSummarySelection)
#
#
#
#			# ADD HIDDEN FIELD SO THAT THE VIEW KNOWS THAT THIS IS DELETE THEN ADD MODE
#			self.fields['mode'] = forms.CharField(required=False, max_length=50, widget=forms.HiddenInput(),initial=identifier)
#			self.fields['name'] = name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Project name'}), initial=savedNameSelection, label='Project name')
#			self.fields['summary'] = forms.CharField(widget=SummernoteWidget(),initial=savedSummarySelection, label='Description')
#			self.fields['companychoice'] = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control'}), label='Part of company', choices=getEntries('company'),initial=companychoiceSelection)
##			self.fields['marketneedchoice'] = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control'}),label='Market Need', choices=getEntries('marketneed'), initial=marketneedchoiceSelection, required=False)
#
#
#	def extra_fields(self):
#		print("in function")
#		for name, value in self.cleaned_data.items():
#			print("first for")
#			print(name)
#			if name.startswith('req_'):
#				print("if name")
#				yield (self.fields[name].label, value)			
#
##
#		#	directAndIndirectReqs = []
#			# get all of the direct requirements via the product id
#		#	directAndIndirectReqs.extend(client.execute('match $i has identifier "'+identifier+'"; (solvedby:$i, $m); (requiremententity: $c, $m); $c has name $n, has identifier $iden; get;'))
#
#			#get all indirect requirements
#		#	directAndIndirectReqs.extend(client.execute('match $i has identifier "'+identifier+'"; (solvedby:$i, $m); (topmarketneed: $y, lowermarketneed: $m); (requiremententity: $b, $y); $b has name $n, has identifier $iden; get;'))



			



###############################





# NEW BROKEN VERSION
#class addCompetitorForm(forms.Form):
#
##	name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Project name'}), label='Project name')
#	summary = forms.CharField(widget=SummernoteWidget(), label='Description')
#	marketneedchoice = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control'}),label='Market Need Set', choices=getEntries('marketneed'), required=False)
#	companychoice = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control','placeholder':'Project name'}), choices=getEntries('company'), label='Part of company')
#
#	mode = forms.CharField(required=False, max_length=50, widget=forms.HiddenInput())
#
#	#mystryvalue='surprise1'
##
#
#	#def extra_answers(self):
#	#	for name, value in self.cleaned_data.items():
#	#		if name.startswith('req_'):
#	#			yield (self.fields[name].label, value)
#
#
#
#
##	def __init__(self,*args,**kwargs):
	
##
#		if 'identifier' in kwargs:
#			identifier = kwargs.pop('identifier')
#		else:
##			identifier=""
#
#		if 'marketid' in kwargs:	
#			marketid = kwargs.pop("marketid")
#			print("market id in kwargs")
#		else:
#			marketid=0	
##
#	
#
#		states = [(4, 'Killer'), (-1, 'Key cause of failure')]	
#			
#
#		super(addCompetitorForm, self).__init__(*args,**kwargs)
#
#
##		if identifier is not None:
#			print("id exists")
#
#
#			requirements=client.execute('match $x isa marketneed, has identifier "'+marketid+'"; (requiremententity:$b, $x); $b has name $n, has identifier $i, has category $c, has importance $p; get $n, $i, $c, $p;')
#
#			if requirements:
#				for req in requirements:
##					#print(req)
#					self.fields['req_%s' % i] = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control'}),label=question, choices=states, required=False)
#
#			
##			print(extra_questions) 
#
#
#			savedNameSelection = client.execute('match $x isa product, has name $y, has identifier "' +identifier+'"; get;')
#			savedSummarySelection = client.execute('match $x isa product, has summary $y, has identifier "' +identifier+'"; get;')	
##			companychoiceSelection = client.execute('match $x isa product, has identifier "' +identifier+'"; (companyproduct:$x, $b); $b has identifier $d; get $d;')	 
#			marketneedchoiceSelection = client.execute('match $x isa product, has identifier "' +identifier+'"; (solvedby:$x, $b); $b has identifier $d; get $d;')	
#
#			if companychoiceSelection:
#				companychoiceSelection=companychoiceSelection[0]['d']['value']
#			if marketneedchoiceSelection:
#				marketneedchoiceSelection=marketneedchoiceSelection[0]['d']['value']
#
##			savedNameSelection = savedNameSelection[0]['y']['value']
#			savedSummarySelection = savedSummarySelection[0]['y']['value']
#			savedSummarySelection = html.unescape(savedSummarySelection)
#
#			self.fields['mode'] = forms.CharField(required=False, max_length=50, widget=forms.HiddenInput(),initial=identifier)
#			self.fields['name'] = name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Project name'}), initial=savedNameSelection, label='Project name')
#			self.fields['summary'] = forms.CharField(widget=SummernoteWidget(),initial=savedSummarySelection, label='Description')
#			self.fields['companychoice'] = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control'}), label='Part of company', choices=getEntries('company'),initial=companychoiceSelection)
##			self.fields['marketneedchoice'] = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control'}),label='Market Need', choices=getEntries('marketneed'), initial=marketneedchoiceSelection, required=False)
#
#
#
#			pagetitle="Edit project"
#
##		else:
#			print('add mode')
#			self.fields['marketneedchoice'] = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control'}), label='Addressing Need', choices=getEntries('marketneed'), initial=marketid, required=False)
#





#############################





class addCompanyForm(forms.Form):

	# Note both customers and competitors are products in the databse, it's only thier relationship with the market need that changes

#	if 'market' in kwargs:
#			marketid = kwargs.pop('marketid')

	fundingstageoptions = [("Pre-seed",'Pre-seed'),("Seed","Seed"),("Series A","Series A"),("Growth","Growth"),("Public", "Public"),("Zombie", "Zombie"),("Dead", "Dead"),("Grant life", "Grant life")]	

	name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Company name'}),label="Company name", max_length=100)	
	summary = forms.CharField(widget=SummernoteWidget(), label='Description')

	fundingstage = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control'}),label='State:',choices=fundingstageoptions, required=False)

	marketneedchoice = forms.MultipleChoiceField(label='Market Need Set', choices=getEntries('marketneed'), required=False)
	productownership = forms.MultipleChoiceField(label='Company products', choices=getEntries('product'), required=False)
	#companychoice = forms.ChoiceField(label='Is this customer part of a larger company?', choices=getEntries('company'), required=False)
	mode = forms.CharField(required=False, max_length=50, widget=forms.HiddenInput())


	def __init__(self,*args,**kwargs):
		
		
		if 'identifier' in kwargs:
			identifier = kwargs.pop('identifier')
		else:
			identifier=None

		if 'marketid' in kwargs:	
			marketid = kwargs.pop("marketid")
		else:
			marketid=0	

		fundingstageoptions = [("Pre-seed",'Pre-seed'),("Seed","Seed"),("Series A","Series A"),("Growth","Growth"),("Public", "Public"),("Zombie", "Zombie"),("Dead", "Dead"),("Grant life", "Grant life")]	

		super(addCompanyForm, self).__init__(*args,**kwargs)
		self.fields['marketneedchoice'] = forms.MultipleChoiceField(label='Market Need Set', choices=getEntries('marketneed'), required=False)
		self.fields['productownership'] = forms.MultipleChoiceField(label='Company products', choices=getEntries('product'), required=False)
		self.fields['fundingstage'] = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control'}),label='State:',choices=fundingstageoptions, required=False)


		if identifier is not None:
			print("id exists")

			attributes =client.execute('match $x isa company, has name $n, has summary $s, has fundingstage $f, has identifier "' +identifier+'"; get $s, $n, $f;')
			productownershipSelection = client.execute('match $x isa company, has identifier "' +identifier+'"; (productowner:$x, $b); $b has identifier $d; get $d;')	
			marketneedchoiceSelection = client.execute('match $x isa company, has identifier "' +identifier+'"; (customer:$x, $b); $b has identifier $d; get $d;')	
 
			savedNameSelection = attributes[0]['n']['value']
			savedSummarySelection = attributes[0]['s']['value']
			fundingstage = attributes[0]['f']['value']
			savedSummarySelection = html.unescape(savedSummarySelection)


			marketchoices=[]
			if marketneedchoiceSelection:	
				for i in range (0,len(marketneedchoiceSelection)):
					marketchoices.append(marketneedchoiceSelection[i]['d']['value'])

			productchoices=[]
			if productownershipSelection:
				for i in range (0,len(productownershipSelection)):
					productchoices=productownershipSelection[i]['d']['value']

	

			# ADD HIDDEN FIELD SO THAT THE VIEW KNOWS THAT THIS IS DELETE THEN ADD MODE
			self.fields['mode'] = forms.CharField(required=False, max_length=50, widget=forms.HiddenInput(),initial=identifier)
			self.fields['name'] = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Project name'}),label="Company name", max_length=100, initial=savedNameSelection)
			self.fields['summary'] = forms.CharField(widget=SummernoteWidget(),initial=savedSummarySelection)
			self.fields['marketneedchoice'] = forms.MultipleChoiceField(label='Market Need', choices=getEntries('marketneed'), initial=marketchoices, required=False)
			self.fields['productownership'] = forms.MultipleChoiceField(label='Company products', choices=getEntries('product'), required=False, initial=productchoices)
			self.fields['fundingstage'] = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control'}),label='State:',choices=fundingstageoptions, required=False,initial=fundingstageoptions)


		else:
			print('add mode')
			self.fields['marketneedchoice'] = forms.MultipleChoiceField(label='Market Need', choices=getEntries('marketneed'), initial=marketid, required=False)
			self.fields['productownership'] = forms.MultipleChoiceField(label='Company products', choices=getEntries('product'), required=False)
			self.fields['fundingstage'] = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control'}),label='State:',choices=fundingstageoptions, required=False)








#class addCompanyForm(forms.Form):
#
#	pagetitle="Add Company"	
#
#	statusoptions = [(4,'Fast'),(3,'Average'),(1,'Unknown'),(0,'Dead'),(5,'Exited')]		
#	name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Company name'}),label="Company name", max_length=100)	
#	summary = forms.CharField(widget=forms.Textarea(attrs={'width':"100%", 'cols' : "80", 'rows': "4", }))
#	status = forms.ChoiceField(label='Company status', choices=statusoptions, required=False)
#
#	mode = forms.CharField(widget = forms.HiddenInput(),initial='identifer not determined')
#
#
#	def __init__(self,*args,**kwargs):
#		
#		statusoptions = [(4,'Fast'),(3,'Average'),(1,'Unknown'),(0,'Dead'),(5,'Exited')]	
#		identifier=None
#		if 'identifier' in kwargs:
#			identifier = kwargs.pop("identifier")
#		if 'marketid' in kwargs:	
#			marketid = kwargs.pop("marketid")
#		else:
#			marketid=0		
#
#		super(addCompanyForm, self).__init__(*args,**kwargs)
#
#		if identifier is not None:
#			print("identifier exists in form")
#			savedNameSelection = graknData=client.execute('match $x isa company, has name $y, has identifier "' +identifier+'"; get;')
#			savedSummarySelection = graknData=client.execute('match $x isa company, has summary $y, has identifier "' +identifier+'"; get;')
#			savedstatusSelection = graknData=client.execute('match $x isa company, has status $y, has identifier "' +identifier+'"; get;')
#
#			savedNameSelection = savedNameSelection[0]['y']['value']
#			savedSummarySelection = savedSummarySelection[0]['y']['value']
#			
#				
#
#			
#			
#			self.fields['mode'] = forms.CharField(widget = forms.HiddenInput(), max_length=100, initial=identifier, required=False)
#			self.fields['name'] = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Company name'}),label="Project title", max_length=100, initial=savedNameSelection)
#			self.fields['summary'] = forms.CharField(widget=forms.Textarea(attrs={'width':"100%", 'cols' : "80", 'rows': "4"}),initial=savedSummarySelection)
#			if savedstatusSelection:
#				self.fields['status'] = forms.ChoiceField(initial=savedstatusSelection)	
#
#			self.pagetitle="Edit Company"	
#		else:
#			print('add mode')
#			#mode = forms.CharField(required=False, max_length=50, widget=forms.HiddenInput(),initial='new')
#			#super(addCompanyForm, self).__init__(*args,**kwargs)	






class addMarketNeedForm(forms.Form):

	pagetitle="Define Venture Backable problem"

	name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Title'}),label="Market name", max_length=100)
	summary = forms.CharField(label="*Specific* pain, cost and solution requirements", widget=forms.Textarea(attrs={'width':"100%", 'cols' : "80", 'rows': "4"}))
	#marketchoice = forms.ChoiceField(label='Sits within wider market need', choices=getEntries('marketneed'), required=False)
	marketsize = forms.CharField( widget=forms.TextInput(attrs={'type':'number'}),initial=0, label= 'Specific market size in millions, number only')
	marketcagr = forms.CharField( widget=forms.TextInput(attrs={'type':'number'}),initial=0, label='CARG percent, number only dont add %')

	sitswithinmarketchoice = forms.MultipleChoiceField(label='Sits within Markets', choices=getEntries('marketneed'), required=False)


	mode = forms.CharField(required=False, max_length=50, widget=forms.HiddenInput())

	def __init__(self,*args,**kwargs):

		identifier=None
		pagetitle = "Add Market Need"
		if 'identifier' in kwargs:	
			identifier = kwargs.pop("identifier")

		super(addMarketNeedForm, self).__init__(*args,**kwargs)
		##self.fields['marketchoice'] = forms.ChoiceField(label='Sits within market', choices=getEntries('market'), required=False)

		# this is here because needs to be within super but pre-loading any ID for new forms
		self.fields['sitswithinmarketchoice'] = forms.MultipleChoiceField(label='Sits within Markets', choices=getEntries('marketneed'), required=False)


		if identifier is not None:			
			savedNameSelection = client.execute('match $x isa marketneed, has name $y, has identifier "' +identifier+'"; get;')
			savedSummarySelection = client.execute('match $x isa marketneed, has summary $y, has identifier "' +identifier+'"; get;')
			#marketchoiceSelection = client.execute('match $x isa marketneed, has identifier "' +identifier+'"; (need:$x, $b); $b has identifier $d; get $d;')	
			marketsizeSelection = client.execute('match $x isa marketneed, has marketsize $y, has identifier "' +identifier+'"; get;')
			marketcagrSelection = client.execute('match $x isa marketneed, has CAGR $y, has identifier "' +identifier+'"; get;')

			sitswithinmarkets = client.execute('match $x isa marketneed, has identifier "' +identifier+'"; (lowermarketneed:$x, $b); $b has identifier $d; get $d;')	

			savedNameSelection = savedNameSelection[0]['y']['value']
			savedSummarySelection = savedSummarySelection[0]['y']['value']

			topmarkets=[]
			if sitswithinmarkets:
				#sitswithinmarkets = sitswithinmarkets[0]['d']['value']
				
				for i in range(0,len(sitswithinmarkets)):
					topmarkets.append(sitswithinmarkets[i]['d']['value'])



			if marketsizeSelection:
				marketsizeSelection = marketsizeSelection[0]['y']['value']
			if marketcagrSelection:
				marketcagrSelection = marketcagrSelection[0]['y']['value']

			self.fields['mode'] = forms.CharField(required=False, max_length=50, widget=forms.HiddenInput(),initial=identifier)
			self.fields['name'] = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Title'}),max_length=100, initial=savedNameSelection)
			self.fields['summary'] = forms.CharField(label="*Specific* pain, cost and solution requirements", widget=forms.Textarea(attrs={'width':"100%", 'cols' : "80", 'rows': "4"}),initial=savedSummarySelection)
			#self.fields['marketchoice'] = forms.ChoiceField(label='Sits within wider market need',choices=getEntries('marketneed'), required=False,initial=marketchoiceSelection)
			self.fields['marketsize'] = forms.CharField( widget=forms.TextInput(attrs={'type':'number'}),initial=marketsizeSelection, label= 'Specific market size in millions, number only')
			self.fields['marketcagr'] = forms.CharField( widget=forms.TextInput(attrs={'type':'number'}),initial=marketcagrSelection, label='CARG percent, number only dont add %')

			self.fields['sitswithinmarketchoice'] = forms.MultipleChoiceField(label='Sits within Markets', choices=getEntries('marketneed'), required=False, initial=topmarkets)


			self.pagetitle="Edit Market Need"
		else:
			print('add mode')	
			#self.fields['sitswithinmarketchoice'] = forms.MultipleChoiceField(label='Sits within Markets', choices=getEntries('marketneed'), required=False)






class addRequirementForm(forms.Form):


	categories=[("Exit", "Exit"),("Market size and growth potential","Market size and growth potential"),("Clinical Stage", "Clinical Stage"),("Defensibility", "Defensibility"),("Manufacturability","Manufacturability"),("Scalability and value capture","Scalability and value capture"),("Technical plan feasability","Technical plan feasability"),("Traction","Traction"),("Team fit","Team fit"),("Funding viability","Funding viability"), ("Binary", "Binary")]

	pagetitle="Define key factors"

	name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Requirement name'}), label='Project name')
	summary = forms.CharField(widget=SummernoteWidget(), label='Description')
	category = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control'}), label='Category', choices=categories, required=False)

	marketchoice = forms.ChoiceField(label='Sits within wider market need', choices=getEntries('marketneed'), required=False)
	importance = forms.CharField( widget=forms.NumberInput(attrs={'type':'number', 'class':'form-control'}),initial=0, label= 'Importance: 1-5, 5 most important')
	confidence = forms.CharField( widget=forms.NumberInput(attrs={'type':'number','class':'form-control'}),initial=0, label='Confidence: 0-100%')
	marketchoice = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control'}), label='Associated with market need:', choices=getEntries('marketneed'), required=False)



	mode = forms.CharField(required=False, max_length=50, widget=forms.HiddenInput())

	def __init__(self,*args,**kwargs):

		
		if 'identifier' in kwargs:	
			identifier = kwargs.pop("identifier")
		else:
			identifier=None
			
		if 'marketid' in kwargs:	
			marketid = kwargs.pop("marketid")
		else:
			marketid=0	

		super(addRequirementForm, self).__init__(*args,**kwargs)
		##self.fields['marketchoice'] = forms.ChoiceField(label='Sits within market', choices=getEntries('market'), required=False)

		if identifier is not None:			
			print("edit mode")
			savedNameSelection = client.execute('match $x isa requirement, has name $y, has identifier "' +identifier+'"; get;')
			savedSummarySelection = client.execute('match $x isa requirement, has summary $y, has identifier "' +identifier+'"; get;')
			importanceSelection = client.execute('match $x isa requirement, has importance $y, has identifier "' +identifier+'"; get;')
			confidenceSelection	= client.execute('match $x isa requirement, has confidence $y, has identifier "' +identifier+'"; get;')
			marketchoiceSelection = client.execute('match $x isa requirement, has identifier "' +identifier+'"; (requiremententity:$x, $b); $b has identifier $d; get $d;')	
			categorySelection = client.execute('match $x isa requirement, has category $y, has identifier "' +identifier+'"; get;')


			savedNameSelection = savedNameSelection[0]['y']['value']
			savedSummarySelection = savedSummarySelection[0]['y']['value']
			savedSummarySelection = html.unescape(savedSummarySelection)


			if importanceSelection:
				importanceSelection = importanceSelection[0]['y']['value']
			if confidenceSelection:
				confidenceSelection = confidenceSelection[0]['y']['value']
			if marketchoiceSelection:
				marketchoiceSelection = marketchoiceSelection[0]['d']['value']
			if categorySelection:
				categorySelection = categorySelection[0]['y']['value']	

			categories=[("Market size and growth potential","Market size and growth potential"),("Clinical Stage", "Clinical Stage"),("Defensibility", "Defensibility"),("Manufacturability","Manufacturability"),("Scalability and value capture","Scalability and value capture"),("Technical plan feasability","Technical plan feasability"),("Traction","Traction"),("Team fit","Team fit"),("Funding viability","Funding viability")]
	

			self.fields['mode'] = forms.CharField(required=False, max_length=50, widget=forms.HiddenInput(),initial=identifier)
			
			self.fields['name'] = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Name'}), initial=savedNameSelection)
			self.fields['summary'] = forms.CharField(label="Summary",widget=SummernoteWidget(),initial=savedSummarySelection)
			self.fields['category'] = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control'}),label='Category:',choices=categories, required=False,initial=categorySelection)
			self.fields['confidence'] = forms.CharField( widget=forms.NumberInput(attrs={'type':'number', 'class':'form-control'}),initial=confidenceSelection, label= 'Confidence: 0-100%')
			self.fields['importance'] = forms.CharField( widget=forms.NumberInput(attrs={'type':'number', 'class':'form-control'}),initial=importanceSelection, label='Importance 1-5')
			self.fields['marketchoice'] = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control'}),label='Accociated with market need:',choices=getEntries('marketneed'), required=False,initial=marketchoiceSelection)


			self.pagetitle="Edit Requirement"
		else:
			print('add mode')
			print(marketid)
			self.fields['marketchoice'] = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control'}),label='Accociated with market need:',choices=getEntries('marketneed'), required=False,initial=marketid)	




class addSolutionForm(forms.Form):


	#categories=[('Breakthrough Advantage','Breakthrough Advantage'), ('Defensibility', 'Defensibility'), ('Scalability', 'Scalability'), ('SCritical performance threshold viability - PoC', 'Critical performance threshold viability - PoC'), ('Critical performance threshold viability - Partnership','Critical performance threshold viability - Partnership'), ('Critical performance threshold viability - Scale', 'Critical performance threshold viability - Scale'), ('Traction','Traction'),('Team fit','Team fit'),('Funding viability - PoC', 'Funding viability - PoC'),('Funding viability - Seed', 'Funding viability - Seed'), ('Funding viability - Scale', 'Funding viability - Scale')]
	status=[(-5,'Key reason for failure'),(-4,'In place - not working'),(-3,'Not addressed or likely not viable'), (-2,'20+ years away'), (-1,'10+ years away'), (0,'5+ years away'), (1,'Near term draft viability'), (2,'Near term - multi DD viability'), (3,'Early evidence'), (4,'Proven'), (5,'Key reason for success')]

	pagetitle="Add solution"
	requirement = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control'}), label='Addresses Requirement', choices=getEntries('requirement'), required=False)

	name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Title'}), label='Title')
	#category = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control'}), label='Category', choices=categories, required=False)
	state = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control'}),label='Status', choices=status, required=False)
	confidence = forms.CharField( widget=forms.NumberInput(attrs={'type':'number','class':'form-control'}), initial=0, label='Confidence: 0-100%')
	summary = forms.CharField(widget=SummernoteWidget(), label='Description')



	mode = forms.CharField(required=False, max_length=50, widget=forms.HiddenInput())
	reqid = forms.CharField(required=False, max_length=50, widget=forms.HiddenInput())
	productid = forms.CharField(required=False, max_length=50, widget=forms.HiddenInput())

	def __init__(self,*args,**kwargs):

		
		pagetitle = "Add Solution"
		if 'solutionid' in kwargs:	
			solutionid = kwargs.pop("solutionid")
		else:
			solutionid = ""				
		if 'reqid' in kwargs:	
			reqid = kwargs.pop("reqid")
		else:
			reqid = ""
		if 'productid' in kwargs:
			productid = kwargs.pop("productid")
		else:
			productid = ""	

		super(addSolutionForm, self).__init__(*args,**kwargs)
		##self.fields['marketchoice'] = forms.ChoiceField(label='Sits within market', choices=getEntries('market'), required=False)

		if solutionid is not "":	# NOTE SET AS EMPTY STRING IN COMPETITOR PAGE		
			print("edit mode")
			savedNameSelection = client.execute('match $x isa solutioncomponent, has name $y, has identifier "' +solutionid+'"; get;')
			savedSummarySelection = client.execute('match $x isa solutioncomponent, has summary $y, has identifier "' +solutionid+'"; get;')
			stateSelection = client.execute('match $x isa solutioncomponent, has status $y, has identifier "' +solutionid+'"; get;')
		#	categorySelection = client.execute('match $x isa solutioncomponent, has category $y, has identifier "' +solutionid+'"; get;')
			confidenceSelection	= client.execute('match $x isa solutioncomponent, has confidence $y, has identifier "' +solutionid+'"; get;')
			requirementSelection = client.execute('match $x isa solutioncomponent, has identifier "' +solutionid+'"; (solution:$x, $b); $b has identifier $d; get $d;')	
		

			savedNameSelection = savedNameSelection[0]['y']['value']
			savedSummarySelection = savedSummarySelection[0]['y']['value']
			savedSummarySelection = html.unescape(savedSummarySelection)


			if confidenceSelection:
				confidenceSelection = confidenceSelection[0]['y']['value']

			if stateSelection:
				stateSelection = stateSelection[0]['y']['value']


			if requirementSelection:
				requirementSelection = requirementSelection[0]['d']['value']	

						
		#	categories=[('Breakthrough Advantage','Breakthrough Advantage'), ('Defensibility', 'Defensibility'), ('Scalability', 'Scalability'), ('SCritical performance threshold viability - PoC', 'Critical performance threshold viability - PoC'), ('Critical performance threshold viability - Partnership','Critical performance threshold viability - Partnership'), ('Critical performance threshold viability - Scale', 'Critical performance threshold viability - Scale'), ('Traction','Traction'),('Team fit','Team fit'),('Funding viability - PoC', 'Funding viability - PoC'),('Funding viability - Seed', 'Funding viability - Seed'), ('Funding viability - Scale', 'Funding viability - Scale')]
			status=[(-2,'Key reason for failure'),(-1,'In place - not working'),(0,'Not addressed or likely not viable'), (1,'Draft viability'), (2,'Multi DD viability'), (3,'Early evidence'), (4,'Proven'), (5,'Key reason for success')]


			self.fields['mode'] = forms.CharField(required=False, max_length=50, widget=forms.HiddenInput(),initial=solutionid)
			self.fields['reqid'] = forms.CharField(required=False, max_length=50, widget=forms.HiddenInput(),initial=reqid)
			self.fields['productid'] = forms.CharField(required=False, max_length=50, widget=forms.HiddenInput(),initial=productid)



			self.fields['requirement'] = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control'}),label='Addresses requirement:',choices=getEntries('requirement'), required=False,initial=requirementSelection)
	
			self.fields['name'] = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Title'}), initial=savedNameSelection, label='Title')
			self.fields['summary'] = forms.CharField(label="Summary", widget=SummernoteWidget(),initial=savedSummarySelection)
			self.fields['confidence'] = forms.CharField(widget=forms.NumberInput(attrs={'type':'number', 'class':'form-control'}),initial=confidenceSelection, label= 'Confidence: 0-100%')
			self.fields['state'] = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control'}),label='State:',choices=status, required=False,initial=stateSelection)
		#	self.fields['category'] = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control'}),label='Category:',choices=categories, required=False,initial=categorySelection)


			self.pagetitle="Edit Solution"
		else:
			print('add mode')
			#print(requirementid)
			self.fields['requirement'] = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control'}),label='Accociated with requirement:',choices=getEntries('requirement'), required=False,initial=reqid)	
			self.fields['reqid'] = forms.CharField(required=False, max_length=50, widget=forms.HiddenInput(),initial=reqid)
			self.fields['productid'] = forms.CharField(required=False, max_length=50, widget=forms.HiddenInput(),initial=productid)






class addTechnologyForm(forms.Form):

	pagetitle="Add Technology"

	name = forms.CharField(label="Technology name", max_length=100)	
	summary = forms.CharField(widget=forms.Textarea(attrs={'width':"100%", 'cols' : "80", 'rows': "4", }))
	technologychoice = forms.ChoiceField(label='part of technology group:', choices=getEntries('technology'), required=False)
	mode = forms.CharField(required=False, max_length=50, widget=forms.HiddenInput())


	def __init__(self,*args,**kwargs):

		identifier=None
		if 'identifier' in kwargs:
			identifier = kwargs.pop("identifier")

		super(addTechnologyForm, self).__init__(*args,**kwargs)	
	
		if identifier is not None:
			print("identifier exists")

			print("Edit mode")
			nameAndSummary = client.execute('match $x isa technology, has name $n, has summary $s, has identifier "' +identifier+'"; get;')
			technologychoiceSelection = client.execute('match $x isa technology, has identifier "' +identifier+'"; (toptechnology:$x, $b); $b has identifier $d; get $d;')	
		 	
			if technologychoiceSelection:
				technologychoiceSelection=technologychoiceSelection[0]['d']['value']

			# NEEDS TO GRAB RELATIONSHIP ON MARKET WHICH NEED SITS IN
			savedNameSelection = nameAndSummary[0]['n']['value']
			savedSummarySelection = nameAndSummary[0]['s']['value']
			self.fields['mode'] = forms.CharField(required=False, max_length=50, widget=forms.HiddenInput(),initial=identifier)
			self.fields['name'] = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Title'}), initial=savedNameSelection, label='Title')
			self.fields['summary'] = forms.CharField(label="Summary", widget=SummernoteWidget(),initial=savedSummarySelection)
			self.fields['technologychoice'] = forms.MultipleChoiceField(widget=forms.SelectMultiple(attrs={'class':'form-control'}),initial=technologychoiceSelection,label='Part of technology group:', choices=getEntries('technology'), required=False)
			

			pagetitle="Add Technology"
		else:
			print('add mode')
			






#class addRiskForm(forms.Form):
#
#	pagetitle="Add Risk / Impact factor"
##
#
#	def __init__(self,*args,**kwargs):
#
#		identifier=None
#		ratings = [(5.0,5.0),(4.0,4.0),(3.0,3.0),(2.0,2.0),(1.0,1.0),(-1.0,-1.0),(-2.0,-2.0),(-3.0,-3.0),(-4.0,-4.0),(-5.0,-5.0)]	
##
#		savedNameSelection = savedNameSelection[0]['y']['value']
#		savedSummarySelection = savedSummarySelection[0]['y']['value']
#		self.fields['mode'] = forms.CharField(required=False, max_length=50, widget=forms.HiddenInput(),initial=identifier)
#		self.fields['name'] = forms.CharField(label="Project title", max_length=100, initial=savedNameSelection)
#		self.fields['summary'] = forms.CharField(widget=forms.Textarea(attrs={'width':"100%", 'cols' : "80", 'rows': "4"}),initial=savedSummarySelection)
##		self.fields['marketchoice'] = forms.ChoiceField(label='Effects a market need:', choices=getEntries('marketneed'), required=False,initial=marketchoiceSelection)
#		self.fields['businesschoice'] = forms.ChoiceField(label='Effects a businessmodel:', choices=getEntries('businessmodel'), required=False, initial=businessmodelchoiceSelection)
#		self.fields['technologychoice'] = forms.ChoiceField(label='Effects a technology:', choices=getEntries('technology'), required=False, initial=technologychoiceSelection)
#		self.fields['score'] = forms.ChoiceField(label='rating, higher good impact, lower worse risk', choices=ratings, required=True,initial=savedRiskRating)
#
#
#
#		pagetitle="Edit risk"
##
#		if 'identifier' in kwargs:	
#			identifier = kwargs.pop("identifier")
#
#		super(addRiskForm, self).__init__(*args,**kwargs)
#	#	self.fields['marketchoice'] = forms.ChoiceField(label='Effects a market:', choices=getEntries('marketneed'), required=False)
#	#	self.fields['businesschoice'] = forms.ChoiceField(label='Effects a businessmodel:', choices=getEntries('businessmodel'), required=False)
##	#	self.fields['technologychoice'] = forms.ChoiceField(label='Effects a technology:', choices=getEntries('technology'), required=False)
#	
#		if identifier is not None:
#
#			print("Edit mode")
#			savedNameSelection =client.execute('match $x isa risk, has name $y, has identifier "' +identifier+'"; get;')
#			savedSummarySelection = client.execute('match $x isa risk, has summary $y, has identifier "' +identifier+'"; get;')
#			savedRiskRating = client.execute('match $x isa risk, has rating $y, has identifier "' +identifier+'"; get;')
#
#			marketchoiceSelection = client.execute('match $x isa risk, has identifier "' +identifier+'"; (riskfactor:$x, $b); $b isa marketneed; $b has identifier $d; get $d;')		
#			businessmodelchoiceSelection = client.execute('match $x isa risk, has identifier "' +identifier+'"; (riskfactor:$x, $b); isa businessmodel; $b has identifier $d; get $d;')	
##			technologychoiceSelection = client.execute('match $x isa risk, has identifier "' +identifier+'"; (riskfactor:$x, $b); isa technology; $b has identifier $d; get $d;')	
#
#			if marketchoiceSelection:
#				marketchoiceSelection = marketchoiceSelection[0]['d']['value']	
##				print(marketchoiceSelection)
#
#			if businessmodelchoiceSelection:
#				print(businessmodelchoiceSelection)
#				businessmodelchoiceSelection = businessmodelchoiceSelection[0]['d']['value']
#				
#
#			if technologychoiceSelection:
#				technologychoiceSelection = technologychoiceSelection[0]['d']['value']	
#				print(technologychoiceSelection)
#
#			if savedRiskRating:
#				savedRiskRating=savedRiskRating[0]['y']['value']
#				print(savedRiskRating)	
#
#
#
##		else:
#			print('add mode')
#
#
#	ratings = [(5.0,5.0),(4.0,4.0),(3.0,3.0),(2.0,2.0),(1.0,1.0),(-1.0,-1.0),(-2.0,-2.0),(-3.0,-3.0),(-4.0,-4.0),(-5.0,-5.0)]		
#	name = forms.CharField(label="Name", max_length=100)	
#	summary = forms.CharField(widget=forms.Textarea(attrs={'width':"100%", 'cols' : "80", 'rows': "4", }))
#	score = forms.ChoiceField(label='rating, higher good impact, lower worse risk', choices=ratings, required=True)
#	marketchoice = forms.ChoiceField(label='Effects a market need:', choices=getEntries('marketneed'), required=False)
#	businesschoice = forms.ChoiceField(label='Effects a businessmodel:', choices=getEntries('businessmodel'), required=False)
#	technologychoice = forms.ChoiceField(label='Effects a technology:', choices=getEntries('technology'), required=False)
#	mode = forms.CharField(required=False, max_length=50, widget=forms.HiddenInput())







#class addBusinessModelForm(forms.Form):
#
#	pagetitle="Add Business Model"
##
#
#	name = forms.CharField(label="Business Model name", max_length=100)	
#	summary = forms.CharField(widget=forms.Textarea(attrs={'width':"100%", 'cols' : "80", 'rows': "4", }))
#	top = forms.ChoiceField(label='Sits within model group', choices=getEntries('businessmodel'), required=False)
#	mode = forms.CharField(required=False, max_length=50, widget=forms.HiddenInput())
#
#
##	def __init__(self,*args,**kwargs):
#
#		identifier=None
#		if 'identifier' in kwargs:
#			identifier = kwargs.pop("identifier")
#		super(addBusinessModelForm, self).__init__(*args,**kwargs)	
#		
#		if identifier is not None:
#
#			print("Edit mode")
#			savedNameSelection = client.execute('match $x isa businessmodel, has name $y, has identifier "' +identifier+'"; get;')
#			savedSummarySelection = client.execute('match $x isa businessmodel, has summary $y, has identifier "' +identifier+'"; get;')
#			businessmodelchoiceSelection = client.execute('match $x isa businessmodel, has identifier "' +identifier+'"; (topbusinessmodel:$x, $b); $b has identifier $d; get $d;')	
#
#			savedNameSelection = savedNameSelection[0]['y']['value']
#			savedSummarySelection = savedSummarySelection[0]['y']['value']
#			if businessmodelchoiceSelection:
#				businessmodelchoiceSelection = businessmodelchoiceSelection[0]['d']['value']
#
#			self.fields['mode'] = forms.CharField(required=False, max_length=50, widget=forms.HiddenInput(),initial=identifier)
#			self.fields['name'] = forms.CharField(label="Project title", max_length=100, initial=savedNameSelection)
#			self.fields['summary'] = forms.CharField(widget=forms.Textarea(attrs={'width':"100%", 'cols' : "80", 'rows': "4"}),initial=savedSummarySelection)
#			self.fields['top'] = forms.ChoiceField(label='Sits within model group', choices=getEntries('businessmodel'), initial=businessmodelchoiceSelection, required=False)
#	
#
#			# UPDATE TOP BUSINESS MODEL FIELD
#			pagetitle="Edit Business model"
#		else:
#			print('add mode')
			#mode = forms.CharField(required=False, max_length=50, widget=forms.HiddenInput(),initial='new')
			



#class addMarketForm(forms.Form):

#	def __init__(self,*args,**kwargs):

#		identifier=None
#		if 'identifier' in kwargs:
#			identifier = kwargs.pop("identifier")
#		super(addMarketForm, self).__init__(*args,**kwargs)	



#		pagetitle="Add Market"

#		if identifier is not None:
#			print("identifier exists")
#
#			print("Edit mode")
#			savedNameSelection = graknData=client.execute('match $x isa market, has name $y, has identifier "' +identifier+'"; get;')
#			savedSummarySelection = graknData=client.execute('match $x isa market, has summary $y, has identifier "' +identifier+'"; get;')
#			marketchoiceSelection = client.execute('match $x isa market, has identifier "' +identifier+'"; (topmarket:$x, $b); $b has identifier $d; get $d;')	
#			
#			if marketchoiceSelection:
#				marketchoiceSelection=marketchoiceSelection[0]['d']['value']	
#
##			savedNameSelection = savedNameSelection[0]['y']['value']
#			savedSummarySelection = savedSummarySelection[0]['y']['value']
#
#
#			self.fields['mode'] = forms.CharField(required=False, max_length=50, widget=forms.HiddenInput(),initial=identifier)
#			self.fields['name'] = forms.CharField(label="Project title", max_length=100, initial=savedNameSelection)
##			self.fields['summary'] = forms.CharField(widget=forms.Textarea(attrs={'width':"100%", 'cols' : "80", 'rows': "4"}),initial=savedSummarySelection)
#			self.fields['top'] = forms.ChoiceField(label='Sits within market', choices=getEntries('market'), required=False, initial=marketchoiceSelection)
#
#
#			pagetitle="Edit Market"
#		else:
##			print('add mode')
#			#mode = forms.CharField(required=False, max_length=50, widget=forms.HiddenInput(),initial='new')
#			
#
##
#	name = forms.CharField(label="Market name", max_length=100)	
#	summary = forms.CharField(widget=forms.Textarea(attrs={'width':"100%", 'cols' : "80", 'rows': "4", }))
#	top = forms.ChoiceField(label='Sits within market', choices=getEntries('market'), required=False)
#	mode = forms.CharField(required=False, max_length=50, widget=forms.HiddenInput())

