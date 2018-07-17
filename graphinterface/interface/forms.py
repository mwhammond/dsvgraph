from django import forms
import grakn
client = grakn.Client(uri='http://35.197.194.67:4567', keyspace='dsvgraph')



class addProjectForm(forms.Form):

	identifier =''

	def __init__(self,*args,**kwargs):
		
		if 'identifier' in kwargs:
			identifier = kwargs.pop("identifier")
			print("edit mode")
			if identifier is not None:
				print("identifier exists")

				print("Edit mode")
				savedNameSelection = graknData=client.execute('match $x isa product, has name $y, has identifier "' +identifier+'"; get;')
				savedSummarySelection = graknData=client.execute('match $x isa product, has summary $y, has identifier "' +identifier+'"; get;')	
				companychoiceSelection = 'nothing' # need to set them all first
				businessmodelchoiceSelection = 'nothing'
				technologychoiceSelection = 'nothing'
				marketchoiceSelection = 'nothing'
				marketNeedSetSelection ='nothing'


				savedNameSelection = savedNameSelection[0]['y']['value']
				savedSummarySelection = savedSummarySelection[0]['y']['value']

				# ADD HIDDEN FIELD SO THAT THE VIEW KNOWS THAT THIS IS DELETE THEN ADD MODE
				#mode = forms.CharField(required=False, max_length=50, widget=forms.HiddenInput(),initial='edit')

				super(addProjectForm, self).__init__(*args,**kwargs)
				#self.fields['name'] = forms.ChoiceField(label="Name", choices=[(x.plug_ip, x.MY_DESCRIPTIVE_FIELD) for x in Sniffer.objects.filter(client = myClient)])
				self.fields['name'] = forms.CharField(label="Project title", max_length=100, initial=savedNameSelection)
				self.fields['summary'] = forms.CharField(widget=forms.Textarea(attrs={'width':"100%", 'cols' : "80", 'rows': "4"}),initial=savedSummarySelection)

		else:
			print('add mode')
			#mode = forms.CharField(required=False, max_length=50, widget=forms.HiddenInput(),initial='new')
			super(addProjectForm, self).__init__(*args,**kwargs)



	pagetitle="Add project"

	# get data for form

	#print(identifier)

	graknData=client.execute('match $x isa businessmodel, has name $y, has identifier $z; get;') # dictionaries are nested structures
	businesmodels=[]
	entity={}
	for entity in graknData:
		businesmodel=(entity['z']['value'],entity['y']['value'])
		businesmodels.append(businesmodel)
	businesmodels=tuple(businesmodels)

	
	graknData=client.execute('match $x isa company, has name $y, has identifier $z; get;') # dictionaries are nested structures
	companies=[]
	entity={}
	for entity in graknData:
		company=(entity['z']['value'],entity['y']['value'])
		companies.append(company)
	companyNames=tuple(companies)

	

	graknData=client.execute('match $x isa market, has name $y, has identifier $z; get;') # dictionaries are nested structures
	markets=[]
	entity={}
	for entity in graknData:
		market=(entity['z']['value'],entity['y']['value'])
		markets.append(market)	
	marketNames=tuple(markets)


	graknData=client.execute('match $x isa technology, has name $y, has identifier $z; get;') # dictionaries are nested structures
	technologies=[]
	entity={}
	for entity in graknData:
		technology=(entity['z']['value'],entity['y']['value'])
		technologies.append(technology)
	technologyNames=tuple(technologies)		

	
	graknData=client.execute('match $x isa marketneed, has name $y, has identifier $z; get;') # dictionaries are nested structures
	marketneeds=[]
	entity={}
	for entity in graknData:
		marketneed=(entity['z']['value'],entity['y']['value'])
		marketneeds.append(marketneed)
	marketneedsNames=tuple(marketneeds)	


	name = forms.CharField(label="Project title", max_length=100)	
	summary = forms.CharField(widget=forms.Textarea(attrs={'width':"100%", 'cols' : "80", 'rows': "4", }))

	companychoice = forms.ChoiceField(label='Company owner', choices=companyNames, required=False)
	businessmodelchoice = forms.ChoiceField(label='Business Model', choices=businesmodels, required=False)
	technologychoice = forms.ChoiceField(label='Add Technology', choices=technologyNames, required=False)
	marketchoice = forms.ChoiceField(label='Specific market', choices=marketNames, required=False)
	marketNeedSet = forms.ChoiceField(label='Market Need Set', choices=marketneedsNames, required=False)






class addCompanyForm(forms.Form):

	pagetitle="Add Company"

	graknData=client.execute('match $x isa market, has name $y, has identifier $z; get $y,$z;') # dictionaries are nested structures
	markets=[]
	for entity in graknData:
		market=(entity['z']['value'],entity['y']['value'])
		markets.append(market)
	marketNames=tuple(markets)

	name = forms.CharField(label="Company name", max_length=100)	
	summary = forms.CharField(widget=forms.Textarea(attrs={'width':"100%", 'cols' : "80", 'rows': "4", }))
	#protocompany = forms.BooleanField(label='Protocompany', required=False)
	marketchoice = forms.ChoiceField(label='Sits within market', choices=marketNames, required=False)





class addMarketNeedForm(forms.Form):

	pagetitle="Add Market Need"

	graknData=client.execute('match $x isa market, has name $y, has identifier $z; get $y,$z;') # dictionaries are nested structures
	markets=[]
	for entity in graknData:
		market=(entity['z']['value'],entity['y']['value'])
		markets.append(market)
	marketNames=tuple(markets)

	name = forms.CharField(label="Name", max_length=100)	
	summary = forms.CharField(widget=forms.Textarea(attrs={'width':"100%", 'cols' : "80", 'rows': "4", }))
	#protocompany = forms.BooleanField(label='Protocompany', required=False)
	marketchoice = forms.ChoiceField(label='Sits within market', choices=marketNames, required=False)



class addRiskForm(forms.Form):

	pagetitle="Add Risk / Impact factor"

	graknData=client.execute('match $x isa businessmodel, has name $y, has identifier $z; get;') # dictionaries are nested structures

	businesmodels=[]
	businesmodels.append(("N/A","N/A"))
	entity={}
	for entity in graknData:
		businesmodel=(entity['z']['value'],entity['y']['value'])
		businesmodels.append(businesmodel)
	businesmodels=tuple(businesmodels)
	

	graknData=client.execute('match $x isa market, has name $y, has identifier $z; get;') # dictionaries are nested structures
	markets=[]
	markets.append(("N/A","N/A"))
	entity={}
	for entity in graknData:
		market=(entity['z']['value'],entity['y']['value'])
		markets.append(market)	
	marketNames=tuple(markets)


	graknData=client.execute('match $x isa technology, has name $y, has identifier $z; get;') # dictionaries are nested structures
	technologies=[]
	technologies.append(("N/A","N/A"))
	entity={}
	for entity in graknData:
		technology=(entity['z']['value'],entity['y']['value'])
		technologies.append(technology)
	technologyNames=tuple(technologies)		

	


	name = forms.CharField(label="Name", max_length=100)	
	summary = forms.CharField(widget=forms.Textarea(attrs={'width':"100%", 'cols' : "80", 'rows': "4", }))
	#protocompany = forms.BooleanField(label='Protocompany', required=False)
	marketchoice = forms.ChoiceField(label='Effects a market:', choices=marketNames, required=False)
	businesschoice = forms.ChoiceField(label='Effects a businessmodel:', choices=businesmodels, required=False)
	technologychoice = forms.ChoiceField(label='Effects a technology:', choices=technologyNames, required=False)





class addBusinessModelForm(forms.Form):

	pagetitle="Add Business Model"

	graknData=client.execute('match $x isa businessmodel, has name $y, has identifier $z; get $y,$z;') # dictionaries are nested structures
	things=[]
	for entity in graknData:
		thing=(entity['z']['value'],entity['y']['value'])
		things.append(thing)
	businessModelNames=tuple(things)

	name = forms.CharField(label="Business Model name", max_length=100)	
	summary = forms.CharField(widget=forms.Textarea(attrs={'width':"100%", 'cols' : "80", 'rows': "4", }))
	top = forms.ChoiceField(label='Sits within model group', choices=businessModelNames, required=False)




class addMarketForm(forms.Form):

	pagetitle="Add Market"

	graknData=client.execute('match $x isa market, has name $y, has identifier $z; get $y,$z;') # dictionaries are nested structures
	things=[]
	for entity in graknData:
		thing=(entity['z']['value'],entity['y']['value'])
		things.append(thing)
	marketNames=tuple(things)

	name = forms.CharField(label="Market name", max_length=100)	
	summary = forms.CharField(widget=forms.Textarea(attrs={'width':"100%", 'cols' : "80", 'rows': "4", }))
	top = forms.ChoiceField(label='Sits within market', choices=marketNames, required=False)




class addTechnologyForm(forms.Form):

	pagetitle="Add Technology"

	graknData=client.execute('match $x isa technology, has name $y, has identifier $z; get $y,$z;') # dictionaries are nested structures
	things=[]
	for entity in graknData:
		thing=(entity['z']['value'],entity['y']['value'])
		things.append(thing)
	technologyNames=tuple(things)

	name = forms.CharField(label="Technology name", max_length=100)	
	summary = forms.CharField(widget=forms.Textarea(attrs={'width':"100%", 'cols' : "80", 'rows': "4", }))
	top = forms.ChoiceField(label='part of technology group:', choices=technologyNames, required=False)