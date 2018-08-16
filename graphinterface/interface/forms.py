from django import forms
import grakn
client = grakn.Client(uri='http://35.197.194.67:4567', keyspace='dsvgraph')


def getEntries(type):

	graknData=client.execute('match $x isa '+type+', has name $y, has identifier $z; get $y,$z;') # dictionaries are nested structures
	entries=[]
	entries.append(("N/A","N/A"))
	for entity in graknData:
		entry=(entity['z']['value'],entity['y']['value'])
		entries.append(entry)
	technologyNames=tuple(entries)

	return entries


class addProjectForm(forms.Form):

	pagetitle="Add project"

	name = forms.CharField(label="Project title", max_length=100)	
	summary = forms.CharField(widget=forms.Textarea(attrs={'width':"100%", 'cols' : "80", 'rows': "4", }))

	companychoice = forms.ChoiceField(label='Company owner', choices=getEntries('company'), required=False)
	businessmodelchoice = forms.ChoiceField(label='Business Model', choices=getEntries('businessmodel'), required=False)
	technologychoice = forms.MultipleChoiceField(label='Add Technology', choices=getEntries('technology'), required=False)
	marketneedchoice = forms.MultipleChoiceField(label='Market Need Set', choices=getEntries('marketneed'), required=False)

	mode = forms.CharField(required=False, max_length=50, widget=forms.HiddenInput())



	def __init__(self,*args,**kwargs):
		
		
		if 'identifier' in kwargs:
			identifier = kwargs.pop('identifier')
		else: 
			identifier=None

		if 'marketid' in kwargs:
			marketid = kwargs.pop('marketid')

		print("edit mode: ", identifier)

		super(addProjectForm, self).__init__(*args,**kwargs)
		self.fields['companychoice'] = forms.ChoiceField(label='Company owner', choices=getEntries('company'), required=False)
		self.fields['businessmodelchoice'] = forms.ChoiceField(label='Business Model', choices=getEntries('businessmodel'), required=False)
		self.fields['technologychoice'] = forms.MultipleChoiceField(label='Add Technology', choices=getEntries('technology'), required=False)
		self.fields['marketneedchoice'] = forms.MultipleChoiceField(label='Market Need Set', choices=getEntries('marketneed'), required=False)


		if identifier is not None:
			print("id exists")

			savedNameSelection = graknData=client.execute('match $x isa product, has name $y, has identifier "' +identifier+'"; get;')
			savedSummarySelection = graknData=client.execute('match $x isa product, has summary $y, has identifier "' +identifier+'"; get;')	
			companychoiceSelection = graknData=client.execute('match $x isa product, has identifier "' +identifier+'"; (companyproduct:$x, $b); $b has identifier $d; get $d;')	
			businessmodelchoiceSelection = graknData=client.execute('match $x isa product, has identifier "' +identifier+'"; (usesmodel:$x, $b); $b has identifier $d; get $d;')	
			technologychoiceSelection = graknData=client.execute('match $x isa product, has identifier "' +identifier+'"; (usestech:$x, $b); $b has identifier $d; get $d;')	 
			marketneedchoiceSelection = graknData=client.execute('match $x isa product, has identifier "' +identifier+'"; (solvedby:$x, $b); $b has identifier $d; get $d;')	

			if companychoiceSelection:
				companychoiceSelection=companychoiceSelection[0]['d']['value']
			if businessmodelchoiceSelection:
				businessmodelchoiceSelection=businessmodelchoiceSelection[0]['d']['value']
			if technologychoiceSelection:
				technologychoiceSelection=technologychoiceSelection[0]['d']['value']
			if marketneedchoiceSelection:
				marketneedchoiceSelection=marketneedchoiceSelection[0]['d']['value']

			savedNameSelection = savedNameSelection[0]['y']['value']
			savedSummarySelection = savedSummarySelection[0]['y']['value']

			# ADD HIDDEN FIELD SO THAT THE VIEW KNOWS THAT THIS IS DELETE THEN ADD MODE
			self.fields['mode'] = forms.CharField(required=False, max_length=50, widget=forms.HiddenInput(),initial=identifier)

			#super(addProjectForm, self).__init__(*args,**kwargs)
			#self.fields['name'] = forms.ChoiceField(label="Name", choices=[(x.plug_ip, x.MY_DESCRIPTIVE_FIELD) for x in Sniffer.objects.filter(client = myClient)])
			self.fields['name'] = forms.CharField(label="Project title", max_length=100, initial=savedNameSelection)
			self.fields['summary'] = forms.CharField(widget=forms.Textarea(attrs={'width':"100%", 'cols' : "80", 'rows': "4"}),initial=savedSummarySelection)
			
			self.fields['companychoice'] = forms.ChoiceField(label='Company owner', choices=getEntries('company'), initial=companychoiceSelection, required=False)
			self.fields['businessmodelchoice'] = forms.ChoiceField(label='Business Model', choices=getEntries('businessmodel'), initial=businessmodelchoiceSelection, required=False)
			self.fields['technologychoice'] = forms.MultipleChoiceField(label='Technology stack', choices=getEntries('technology'), initial=technologychoiceSelection, required=False)
			self.fields['marketneedchoice'] = forms.MultipleChoiceField(label='Market Need', choices=getEntries('marketneed'), initial=marketneedchoiceSelection, required=False)



			pagetitle="Edit project"

		else:
			print('add mode')
			self.fields['marketneedchoice'] = forms.MultipleChoiceField(label='Market Need', choices=getEntries('marketneed'), initial=marketid, required=False)

			#mode = forms.CharField(required=False, max_length=50, widget=forms.HiddenInput(),initial='new')
			#super(addProjectForm, self).__init__(*args,**kwargs)


	# get static (rather than edit) data for form





class addCompetitorForm(forms.Form):

	name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Project name'}), label='Project name')
	summary = forms.CharField(widget=forms.Textarea(attrs={'width':"100%", 'cols' : "80", 'rows': "4",'class':'form-control','placeholder':'Description'}), label='Description')
	companychoice = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control','placeholder':'Project name'}), choices=getEntries('company'), label='Part of company')

			


	#businessmodelchoice = forms.ChoiceField(label='Business Model', choices=getEntries('businessmodel'), required=False)
	#technologychoice = forms.MultipleChoiceField(label='Add Technology', choices=getEntries('technology'), required=False)
	marketneedchoice = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control'}),label='Market Need Set', choices=getEntries('marketneed'), required=False)

	mode = forms.CharField(required=False, max_length=50, widget=forms.HiddenInput())

	#mystryvalue='surprise1'

	def __init__(self,*args,**kwargs):
	

		if 'identifier' in kwargs:
			identifier = kwargs.pop('identifier')
		else:
			identifier=None	

		if 'marketid' in kwargs:	
			marketid = kwargs.pop("marketid")
		else:
			marketid=0	

		self.mystryvalue='surprise2'			

		super(addCompetitorForm, self).__init__(*args,**kwargs)
		#self.fields['companychoice'] = forms.ChoiceField(label='Company owner', choices=getEntries('company'), required=False)
	#	self.fields['businessmodelchoice'] = forms.ChoiceField(label='Business Model', choices=getEntries('businessmodel'), required=False)
	#	self.fields['technologychoice'] = forms.MultipleChoiceField(label='Add Technology', choices=getEntries('technology'), required=False)
		self.fields['marketneedchoice'] = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control'}),label='Market Need Set', choices=getEntries('marketneed'), required=False)

		

		if identifier is not None:
			print("id exists")

			savedNameSelection = client.execute('match $x isa product, has name $y, has identifier "' +identifier+'"; get;')
			savedSummarySelection = client.execute('match $x isa product, has summary $y, has identifier "' +identifier+'"; get;')	
			companychoiceSelection = client.execute('match $x isa product, has identifier "' +identifier+'"; (companyproduct:$x, $b); $b has identifier $d; get $d;')	
	#		businessmodelchoiceSelection = client.execute('match $x isa product, has identifier "' +identifier+'"; (usesmodel:$x, $b); $b has identifier $d; get $d;')	
	#		technologychoiceSelection = client.execute('match $x isa product, has identifier "' +identifier+'"; (usestech:$x, $b); $b has identifier $d; get $d;')	 
			marketneedchoiceSelection = client.execute('match $x isa product, has identifier "' +identifier+'"; (solvedby:$x, $b); $b has identifier $d; get $d;')	


			# QUESTION IS WHAT DO I ADD THIS TOO???	

			if companychoiceSelection:
				companychoiceSelection=companychoiceSelection[0]['d']['value']
	#		if businessmodelchoiceSelection:
	#			businessmodelchoiceSelection=businessmodelchoiceSelection[0]['d']['value']
	#		if technologychoiceSelection:
	#			technologychoiceSelection=technologychoiceSelection[0]['d']['value']
			if marketneedchoiceSelection:
				marketneedchoiceSelection=marketneedchoiceSelection[0]['d']['value']

			savedNameSelection = savedNameSelection[0]['y']['value']
			savedSummarySelection = savedSummarySelection[0]['y']['value']

			# ADD HIDDEN FIELD SO THAT THE VIEW KNOWS THAT THIS IS DELETE THEN ADD MODE
			self.fields['mode'] = forms.CharField(required=False, max_length=50, widget=forms.HiddenInput(),initial=identifier)

			self.fields['name'] = name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Project name'}), initial=savedNameSelection, label='Project name')
			self.fields['summary'] = forms.CharField(widget=forms.Textarea(attrs={'width':"100%", 'cols' : "80", 'rows': "4",'class':'form-control','placeholder':'Description'}),initial=savedSummarySelection, label='Description')
			self.fields['companychoice'] = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control'}), label='Part of company', choices=getEntries('company'),initial=companychoiceSelection)



	#		self.fields['businessmodelchoice'] = forms.ChoiceField(label='Business Model', choices=getEntries('businessmodel'), initial=businessmodelchoiceSelection, required=False)
	#		self.fields['technologychoice'] = forms.MultipleChoiceField(label='Technology stack', choices=getEntries('technology'), initial=technologychoiceSelection, required=False)
			self.fields['marketneedchoice'] = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control'}),label='Market Need', choices=getEntries('marketneed'), initial=marketneedchoiceSelection, required=False)



			pagetitle="Edit project"

		else:
			print('add mode')
			self.fields['marketneedchoice'] = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control'}), label='Addressing Need', choices=getEntries('marketneed'), initial=marketid, required=False)






class addCustomerForm(forms.Form):

	# Note both customers and competitors are products in the databse, it's only thier relationship with the market need that changes

#	if 'market' in kwargs:
#			marketid = kwargs.pop('marketid')

	riskratings = [(5.0,'Extreme'),(4.0,'High'),(3.0,'Medium'),(2.0,'Low')]	

	name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Company name'}),label="Company name", max_length=100)	
	summary = forms.CharField(widget=forms.Textarea(attrs={'width':"100%", 'cols' : "80", 'rows': "4", }))

	companychoice = forms.ChoiceField(label='Is this customer part of a larger company?', choices=getEntries('company'), required=False)
	#businessmodelchoice = forms.ChoiceField(label='Business Model of how they tend to purchase (if known)', choices=getEntries('businessmodel'), required=False)
	marketneedchoice = forms.MultipleChoiceField(label='Market Need Set', choices=getEntries('marketneed'), required=False)
	mode = forms.CharField(required=False, max_length=50, widget=forms.HiddenInput())


	financialimpact = forms.CharField(widget=forms.TextInput(attrs={'type':'number'}), label="Quantified financial impact (numer in thousands)", max_length=100)	
	userbudget = forms.CharField(widget=forms.TextInput(attrs={'type':'number'}), label="Aprox budget for the company to solve (number in thousands)", max_length=100)	
	riskadversion = forms.ChoiceField(label='Risk adversion of customer', choices=riskratings, required=False)




			# Quantified financial impact per company (number)
			# Direct end user budget to solve (number)
			# Risk adversion (very high-high-med-low)


	def __init__(self,*args,**kwargs):
		
		
		if 'identifier' in kwargs:
			identifier = kwargs.pop('identifier')
		else:
			identifier=None

		if 'marketid' in kwargs:	
			marketid = kwargs.pop("marketid")
		else:
			marketid=0	

		riskratings = [(5.0,'Extreme'),(4.0,'High'),(3.0,'Medium'),(2.0,'Low')]	

		super(addCustomerForm, self).__init__(*args,**kwargs)
		self.fields['companychoice'] = forms.ChoiceField(label='Is this customer part of a larger company?', choices=getEntries('company'), required=False)
		#self.fields['businessmodelchoice'] = forms.ChoiceField(label='Business Model of how they tend to purchase (if known)', choices=getEntries('businessmodel'), required=False)
		self.fields['marketneedchoice'] = forms.MultipleChoiceField(label='Market Need Set', choices=getEntries('marketneed'), required=False)

		self.fields['financialimpact'] = forms.CharField(label="Quantified financial impact (numer in thousands)", max_length=100)	
		self.fields['userbudget'] = forms.CharField(label="Aprox budget for the company to solve (number in thousands)", max_length=100)	
		self.fields['riskadversion'] = forms.ChoiceField(label='Risk adversion of customer', choices=riskratings, required=False)



		if identifier is not None:
			print("id exists")

			savedNameSelection =client.execute('match $x isa product, has name $y, has identifier "' +identifier+'"; get;')
			savedSummarySelection =client.execute('match $x isa product, has summary $y, has identifier "' +identifier+'"; get;')	
			companychoiceSelection =client.execute('match $x isa product, has identifier "' +identifier+'"; (companyproduct:$x, $b); $b has identifier $d; get $d;')	
			#businessmodelchoiceSelection =client.execute('match $x isa product, has identifier "' +identifier+'"; (usesmodel:$x, $b); $b has identifier $d; get $d;')	
			marketneedchoiceSelection = client.execute('match $x isa product, has identifier "' +identifier+'"; (customer:$x, $b); $b has identifier $d; get $d;')	

			attributes = client.execute('match $x isa product, has finimpact $f, has userbudget $u, has riskscore $r, has identifier "' +identifier+'"; get;')



			if companychoiceSelection:
				companychoiceSelection=companychoiceSelection[0]['d']['value']
			#if businessmodelchoiceSelection:
			#	businessmodelchoiceSelection=businessmodelchoiceSelection[0]['d']['value']
			if marketneedchoiceSelection:
				marketneedchoiceSelection=marketneedchoiceSelection[0]['d']['value']

			if attributes:
				print(attributes)
				financialimpactSelection = attributes[0]['f']['value']
				userbudgetSelection = attributes[0]['u']['value']
				riskadversionSelection = attributes[0]['r']['value']
	

			savedNameSelection = savedNameSelection[0]['y']['value']
			savedSummarySelection = savedSummarySelection[0]['y']['value']

			# ADD HIDDEN FIELD SO THAT THE VIEW KNOWS THAT THIS IS DELETE THEN ADD MODE
			self.fields['mode'] = forms.CharField(required=False, max_length=50, widget=forms.HiddenInput(),initial=identifier)

			#super(addProjectForm, self).__init__(*args,**kwargs)
			#self.fields['name'] = forms.ChoiceField(label="Name", choices=[(x.plug_ip, x.MY_DESCRIPTIVE_FIELD) for x in Sniffer.objects.filter(client = myClient)])
			self.fields['name'] = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Project name'}),label="Company name", max_length=100, initial=savedNameSelection)
			self.fields['summary'] = forms.CharField(widget=forms.Textarea(attrs={'width':"100%", 'cols' : "80", 'rows': "4"}),initial=savedSummarySelection)
			
			self.fields['companychoice'] = forms.ChoiceField(label='Is this customer part of a larger company?', choices=getEntries('company'), initial=companychoiceSelection, required=False)
			#self.fields['businessmodelchoice'] = forms.ChoiceField(label='Business Model of how they tend to purchase (if known)', choices=getEntries('businessmodel'), initial=businessmodelchoiceSelection, required=False)
			self.fields['marketneedchoice'] = forms.MultipleChoiceField(label='Market Need', choices=getEntries('marketneed'), initial=marketneedchoiceSelection, required=False)

			self.fields['financialimpact'] = forms.CharField(label="Quantified financial impact (numer in thousands)", initial=financialimpactSelection, max_length=100)	
			self.fields['userbudget'] = forms.CharField(label="Aprox budget for the company to solve (number in thousands)", initial=userbudgetSelection, max_length=100)	
			self.fields['riskadversion'] = forms.ChoiceField(label='Risk adversion of customer', choices=riskratings, initial=riskadversionSelection, required=False)




		else:
			print('add mode')
			self.fields['marketneedchoice'] = forms.MultipleChoiceField(label='Market Need', choices=getEntries('marketneed'), initial=marketid, required=False)








class addCompanyForm(forms.Form):

	pagetitle="Add Company"	

	statusoptions = [(4,'Fast'),(3,'Average'),(1,'Unknown'),(0,'Dead'),(5,'Exited')]		
	name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Company name'}),label="Company name", max_length=100)	
	summary = forms.CharField(widget=forms.Textarea(attrs={'width':"100%", 'cols' : "80", 'rows': "4", }))
	status = forms.ChoiceField(label='Company status', choices=statusoptions, required=False)

	mode = forms.CharField(widget = forms.HiddenInput(),initial='identifer not determined')


	def __init__(self,*args,**kwargs):
		
		statusoptions = [(4,'Fast'),(3,'Average'),(1,'Unknown'),(0,'Dead'),(5,'Exited')]	
		identifier=None
		if 'identifier' in kwargs:
			identifier = kwargs.pop("identifier")
		if 'marketid' in kwargs:	
			marketid = kwargs.pop("marketid")
		else:
			marketid=0		

		super(addCompanyForm, self).__init__(*args,**kwargs)

		if identifier is not None:
			print("identifier exists in form")
			savedNameSelection = graknData=client.execute('match $x isa company, has name $y, has identifier "' +identifier+'"; get;')
			savedSummarySelection = graknData=client.execute('match $x isa company, has summary $y, has identifier "' +identifier+'"; get;')
			savedstatusSelection = graknData=client.execute('match $x isa company, has status $y, has identifier "' +identifier+'"; get;')

			savedNameSelection = savedNameSelection[0]['y']['value']
			savedSummarySelection = savedSummarySelection[0]['y']['value']
			
				

			
			
			self.fields['mode'] = forms.CharField(widget = forms.HiddenInput(), max_length=100, initial=identifier, required=False)
			self.fields['name'] = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Company name'}),label="Project title", max_length=100, initial=savedNameSelection)
			self.fields['summary'] = forms.CharField(widget=forms.Textarea(attrs={'width':"100%", 'cols' : "80", 'rows': "4"}),initial=savedSummarySelection)
			if savedstatusSelection:
				self.fields['status'] = forms.ChoiceField(initial=savedstatusSelection)	

			self.pagetitle="Edit Company"	
		else:
			print('add mode')
			#mode = forms.CharField(required=False, max_length=50, widget=forms.HiddenInput(),initial='new')
			#super(addCompanyForm, self).__init__(*args,**kwargs)	






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






class addRequirementForm(forms.Form):



	categories=[('Technical','Technical'), ('Team', 'Team'), ('Seed financing', 'Seed financing'), ('Growth financing','Growth financing')]

	pagetitle="Define Venture Backable problem"

	name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Requirement name'}), label='Project name')
	summary = forms.CharField(widget=forms.Textarea(attrs={'width':"100%", 'cols' : "80", 'rows': "4",'class':'form-control','placeholder':'Description'}), label='Description')
	category = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control'}), label='Category', choices=categories, required=False)

	marketchoice = forms.ChoiceField(label='Sits within wider market need', choices=getEntries('marketneed'), required=False)
	importance = forms.CharField( widget=forms.NumberInput(attrs={'type':'number', 'class':'form-control'}),initial=0, label= 'Importance: 1-5, 5 most important')
	confidence = forms.CharField( widget=forms.NumberInput(attrs={'type':'number','class':'form-control'}),initial=0, label='Confidence: 0-100%')
	marketchoice = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control'}), label='Associated with market need:', choices=getEntries('marketneed'), required=False)



	mode = forms.CharField(required=False, max_length=50, widget=forms.HiddenInput())

	def __init__(self,*args,**kwargs):

		
		pagetitle = "Add Requirement"
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

			if importanceSelection:
				importanceSelection = importanceSelection[0]['y']['value']
			if confidenceSelection:
				confidenceSelection = confidenceSelection[0]['y']['value']
			if marketchoiceSelection:
				marketchoiceSelection = marketchoiceSelection[0]['d']['value']
			if categorySelection:
				categorySelection = categorySelection[0]['y']['value']	

			categories=[('Technical','Technical'), ('Team', 'Team'), ('Seed financing', 'Seed financing'), ('Growth financing','Growth financing')]
	

			self.fields['mode'] = forms.CharField(required=False, max_length=50, widget=forms.HiddenInput(),initial=identifier)
			
			self.fields['name'] = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Requirement name'}), initial=savedNameSelection)
			self.fields['summary'] = forms.CharField(label="Summary", widget=forms.Textarea(attrs={'width':"100%", 'cols' : "80", 'rows': "4",'class':'form-control','placeholder':'Description'}),initial=savedSummarySelection)
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


	categories=[('Technical','Technical'), ('Team', 'Team'), ('Seed financing', 'Seed financing'), ('Growth financing','Growth financing')]
	status=[(0,'Not addressed or not viable'), (1,'Draft viability'), (2,'Multi DD viability'), (3,'Early evidence'), (4,'Proven'), (5,'Out performed')]

	pagetitle="Add solution"
	requirement = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control'}), label='Addresses Requirement', choices=getEntries('requirement'), required=False)

	name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Title'}), label='Title')
	category = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control'}), label='Category', choices=categories, required=False)
	state = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control'}),label='Status', choices=status, required=False)
	confidence = forms.CharField( widget=forms.NumberInput(attrs={'type':'number','class':'form-control'}), initial=0, label='Confidence: 0-100%')
	summary = forms.CharField(widget=forms.Textarea(attrs={'width':"100%", 'cols' : "80", 'rows': "4",'class':'form-control','placeholder':'Description'}), label='Description')


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
			categorySelection = client.execute('match $x isa solutioncomponent, has category $y, has identifier "' +solutionid+'"; get;')
			confidenceSelection	= client.execute('match $x isa solutioncomponent, has confidence $y, has identifier "' +solutionid+'"; get;')
			requirementSelection = client.execute('match $x isa solutioncomponent, has identifier "' +solutionid+'"; (solution:$x, $b); $b has identifier $d; get $d;')	
		

			savedNameSelection = savedNameSelection[0]['y']['value']
			savedSummarySelection = savedSummarySelection[0]['y']['value']

			if confidenceSelection:
				confidenceSelection = confidenceSelection[0]['y']['value']

			if stateSelection:
				stateSelection = stateSelection[0]['y']['value']

			if categorySelection:
				categorySelection = categorySelection[0]['y']['value']

			if requirementSelection:
				requirementSelection = requirementSelection[0]['d']['value']	

						
			categories=[('Technical','Technical'), ('Team', 'Team'), ('Seed financing', 'Seed financing'), ('Growth financing','Growth financing')]
			status=[(0,'Not addressed or not viable'), (1,'Draft plan'), (2,'Multi DD plan'), (3,'Early evidence'), (4,'Proven'), (5,'Out performed')]
	

			self.fields['mode'] = forms.CharField(required=False, max_length=50, widget=forms.HiddenInput(),initial=solutionid)
			self.fields['reqid'] = forms.CharField(required=False, max_length=50, widget=forms.HiddenInput(),initial=reqid)
			self.fields['productid'] = forms.CharField(required=False, max_length=50, widget=forms.HiddenInput(),initial=productid)



			self.fields['requirement'] = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control'}),label='Addresses requirement:',choices=getEntries('requirement'), required=False,initial=requirementSelection)
	
			self.fields['name'] = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Title'}), initial=savedNameSelection, label='Title')
			self.fields['summary'] = forms.CharField(label="Summary", widget=forms.Textarea(attrs={'width':"100%", 'cols' : "80", 'rows': "4",'class':'form-control','placeholder':'Description'}),initial=savedSummarySelection)
			self.fields['confidence'] = forms.CharField(widget=forms.NumberInput(attrs={'type':'number', 'class':'form-control'}),initial=confidenceSelection, label= 'Confidence: 0-100%')
			self.fields['state'] = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control'}),label='State:',choices=status, required=False,initial=stateSelection)
			self.fields['category'] = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control'}),label='Category:',choices=categories, required=False,initial=categorySelection)


			self.pagetitle="Edit Solution"
		else:
			print('add mode')
			#print(requirementid)
			self.fields['requirement'] = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control'}),label='Accociated with requirement:',choices=getEntries('requirement'), required=False,initial=reqid)	
			self.fields['reqid'] = forms.CharField(required=False, max_length=50, widget=forms.HiddenInput(),initial=reqid)
			self.fields['productid'] = forms.CharField(required=False, max_length=50, widget=forms.HiddenInput(),initial=productid)










class addRiskForm(forms.Form):

	pagetitle="Add Risk / Impact factor"


	def __init__(self,*args,**kwargs):

		identifier=None
		ratings = [(5.0,5.0),(4.0,4.0),(3.0,3.0),(2.0,2.0),(1.0,1.0),(-1.0,-1.0),(-2.0,-2.0),(-3.0,-3.0),(-4.0,-4.0),(-5.0,-5.0)]	

		savedNameSelection = savedNameSelection[0]['y']['value']
		savedSummarySelection = savedSummarySelection[0]['y']['value']
		self.fields['mode'] = forms.CharField(required=False, max_length=50, widget=forms.HiddenInput(),initial=identifier)
		self.fields['name'] = forms.CharField(label="Project title", max_length=100, initial=savedNameSelection)
		self.fields['summary'] = forms.CharField(widget=forms.Textarea(attrs={'width':"100%", 'cols' : "80", 'rows': "4"}),initial=savedSummarySelection)
		self.fields['marketchoice'] = forms.ChoiceField(label='Effects a market need:', choices=getEntries('marketneed'), required=False,initial=marketchoiceSelection)
		self.fields['businesschoice'] = forms.ChoiceField(label='Effects a businessmodel:', choices=getEntries('businessmodel'), required=False, initial=businessmodelchoiceSelection)
		self.fields['technologychoice'] = forms.ChoiceField(label='Effects a technology:', choices=getEntries('technology'), required=False, initial=technologychoiceSelection)
		self.fields['score'] = forms.ChoiceField(label='rating, higher good impact, lower worse risk', choices=ratings, required=True,initial=savedRiskRating)



		pagetitle="Edit risk"

		if 'identifier' in kwargs:	
			identifier = kwargs.pop("identifier")

		super(addRiskForm, self).__init__(*args,**kwargs)
	#	self.fields['marketchoice'] = forms.ChoiceField(label='Effects a market:', choices=getEntries('marketneed'), required=False)
	#	self.fields['businesschoice'] = forms.ChoiceField(label='Effects a businessmodel:', choices=getEntries('businessmodel'), required=False)
	#	self.fields['technologychoice'] = forms.ChoiceField(label='Effects a technology:', choices=getEntries('technology'), required=False)
	
		if identifier is not None:

			print("Edit mode")
			savedNameSelection =client.execute('match $x isa risk, has name $y, has identifier "' +identifier+'"; get;')
			savedSummarySelection = client.execute('match $x isa risk, has summary $y, has identifier "' +identifier+'"; get;')
			savedRiskRating = client.execute('match $x isa risk, has rating $y, has identifier "' +identifier+'"; get;')

			marketchoiceSelection = client.execute('match $x isa risk, has identifier "' +identifier+'"; (riskfactor:$x, $b); $b isa marketneed; $b has identifier $d; get $d;')		
			businessmodelchoiceSelection = client.execute('match $x isa risk, has identifier "' +identifier+'"; (riskfactor:$x, $b); isa businessmodel; $b has identifier $d; get $d;')	
			technologychoiceSelection = client.execute('match $x isa risk, has identifier "' +identifier+'"; (riskfactor:$x, $b); isa technology; $b has identifier $d; get $d;')	

			if marketchoiceSelection:
				marketchoiceSelection = marketchoiceSelection[0]['d']['value']	
				print(marketchoiceSelection)

			if businessmodelchoiceSelection:
				print(businessmodelchoiceSelection)
				businessmodelchoiceSelection = businessmodelchoiceSelection[0]['d']['value']
				

			if technologychoiceSelection:
				technologychoiceSelection = technologychoiceSelection[0]['d']['value']	
				print(technologychoiceSelection)

			if savedRiskRating:
				savedRiskRating=savedRiskRating[0]['y']['value']
				print(savedRiskRating)	



		else:
			print('add mode')


	ratings = [(5.0,5.0),(4.0,4.0),(3.0,3.0),(2.0,2.0),(1.0,1.0),(-1.0,-1.0),(-2.0,-2.0),(-3.0,-3.0),(-4.0,-4.0),(-5.0,-5.0)]		
	name = forms.CharField(label="Name", max_length=100)	
	summary = forms.CharField(widget=forms.Textarea(attrs={'width':"100%", 'cols' : "80", 'rows': "4", }))
	score = forms.ChoiceField(label='rating, higher good impact, lower worse risk', choices=ratings, required=True)
	marketchoice = forms.ChoiceField(label='Effects a market need:', choices=getEntries('marketneed'), required=False)
	businesschoice = forms.ChoiceField(label='Effects a businessmodel:', choices=getEntries('businessmodel'), required=False)
	technologychoice = forms.ChoiceField(label='Effects a technology:', choices=getEntries('technology'), required=False)
	mode = forms.CharField(required=False, max_length=50, widget=forms.HiddenInput())







class addBusinessModelForm(forms.Form):

	pagetitle="Add Business Model"


	name = forms.CharField(label="Business Model name", max_length=100)	
	summary = forms.CharField(widget=forms.Textarea(attrs={'width':"100%", 'cols' : "80", 'rows': "4", }))
	top = forms.ChoiceField(label='Sits within model group', choices=getEntries('businessmodel'), required=False)
	mode = forms.CharField(required=False, max_length=50, widget=forms.HiddenInput())


	def __init__(self,*args,**kwargs):

		identifier=None
		if 'identifier' in kwargs:
			identifier = kwargs.pop("identifier")
		super(addBusinessModelForm, self).__init__(*args,**kwargs)	
		
		if identifier is not None:

			print("Edit mode")
			savedNameSelection = client.execute('match $x isa businessmodel, has name $y, has identifier "' +identifier+'"; get;')
			savedSummarySelection = client.execute('match $x isa businessmodel, has summary $y, has identifier "' +identifier+'"; get;')
			businessmodelchoiceSelection = client.execute('match $x isa businessmodel, has identifier "' +identifier+'"; (topbusinessmodel:$x, $b); $b has identifier $d; get $d;')	

			savedNameSelection = savedNameSelection[0]['y']['value']
			savedSummarySelection = savedSummarySelection[0]['y']['value']
			if businessmodelchoiceSelection:
				businessmodelchoiceSelection = businessmodelchoiceSelection[0]['d']['value']

			self.fields['mode'] = forms.CharField(required=False, max_length=50, widget=forms.HiddenInput(),initial=identifier)
			self.fields['name'] = forms.CharField(label="Project title", max_length=100, initial=savedNameSelection)
			self.fields['summary'] = forms.CharField(widget=forms.Textarea(attrs={'width':"100%", 'cols' : "80", 'rows': "4"}),initial=savedSummarySelection)
			self.fields['top'] = forms.ChoiceField(label='Sits within model group', choices=getEntries('businessmodel'), initial=businessmodelchoiceSelection, required=False)
	

			# UPDATE TOP BUSINESS MODEL FIELD
			pagetitle="Edit Business model"
		else:
			print('add mode')
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



class addTechnologyForm(forms.Form):

	pagetitle="Add Technology"

	def __init__(self,*args,**kwargs):

		identifier=None
		if 'identifier' in kwargs:
			identifier = kwargs.pop("identifier")
		super(addTechnologyForm, self).__init__(*args,**kwargs)	
	
		if identifier is not None:
			print("identifier exists")

			print("Edit mode")
			savedNameSelection = graknData=client.execute('match $x isa technology, has name $y, has identifier "' +identifier+'"; get;')
			savedSummarySelection = graknData=client.execute('match $x isa technology, has summary $y, has identifier "' +identifier+'"; get;')
			technologychoiceSelection = client.execute('match $x isa technology, has identifier "' +identifier+'"; (toptechnology:$x, $b); $b has identifier $d; get $d;')	
		 	
			print('output',technologychoiceSelection)

			if technologychoiceSelection:
				technologychoiceSelection=technologychoiceSelection[0]['d']['value']

			# NEEDS TO GRAB RELATIONSHIP ON MARKET WHICH NEED SITS IN
			savedNameSelection = savedNameSelection[0]['y']['value']
			savedSummarySelection = savedSummarySelection[0]['y']['value']
			self.fields['mode'] = forms.CharField(required=False, max_length=50, widget=forms.HiddenInput(),initial=identifier)
			self.fields['name'] = forms.CharField(label="Project title", max_length=100, initial=savedNameSelection)
			self.fields['summary'] = forms.CharField(widget=forms.Textarea(attrs={'width':"100%", 'cols' : "80", 'rows': "4"}),initial=savedSummarySelection)
			self.fields['technologychoice'] = forms.ChoiceField(label='part of technology group:', choices=getEntries('technology'), required=False, initial=technologychoiceSelection)
			

			pagetitle="Edit Market Need"
		else:
			print('add mode')
			


	name = forms.CharField(label="Technology name", max_length=100)	
	summary = forms.CharField(widget=forms.Textarea(attrs={'width':"100%", 'cols' : "80", 'rows': "4", }))
	technologychoice = forms.ChoiceField(label='part of technology group:', choices=getEntries('technology'), required=False)
	mode = forms.CharField(required=False, max_length=50, widget=forms.HiddenInput())