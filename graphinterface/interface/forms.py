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

	def __init__(self,*args,**kwargs):
		
		print(kwargs)
		identifier = kwargs.pop("identifier")
		print("edit mode: ", identifier)

		super(addProjectForm, self).__init__(*args,**kwargs)
		self.fields['companychoice'] = forms.ChoiceField(label='Company owner', choices=getEntries('company'), required=False)
		self.fields['businessmodelchoice'] = forms.ChoiceField(label='Business Model', choices=getEntries('businessmodel'), required=False)
		self.fields['technologychoice'] = forms.ChoiceField(label='Add Technology', choices=getEntries('technology'), required=False)
		self.fields['marketneedchoice'] = forms.ChoiceField(label='Market Need Set', choices=getEntries('marketneed'), required=False)


		if identifier is not None:
			print("id exists")

			savedNameSelection = graknData=client.execute('match $x isa product, has name $y, has identifier "' +identifier+'"; get;')
			savedSummarySelection = graknData=client.execute('match $x isa product, has summary $y, has identifier "' +identifier+'"; get;')	
			companychoiceSelection = 'nothing' # GET THE ID OF THE COMPANY IT RELATES TO, IF ANY
			businessmodelchoiceSelection = 'nothing' # GET THE ID OF THE BUSINESS MODEL SHARING THE RELATIONSHIP, IF ANY
			technologychoiceSelection = 'nothing'
			marketneedchoiceSelection ='nothing'


			savedNameSelection = savedNameSelection[0]['y']['value']
			savedSummarySelection = savedSummarySelection[0]['y']['value']

			# ADD HIDDEN FIELD SO THAT THE VIEW KNOWS THAT THIS IS DELETE THEN ADD MODE
			mode = forms.CharField(required=False, max_length=50, widget=forms.HiddenInput(),initial=identifier)

			super(addProjectForm, self).__init__(*args,**kwargs)
			#self.fields['name'] = forms.ChoiceField(label="Name", choices=[(x.plug_ip, x.MY_DESCRIPTIVE_FIELD) for x in Sniffer.objects.filter(client = myClient)])
			self.fields['name'] = forms.CharField(label="Project title", max_length=100, initial=savedNameSelection)
			self.fields['summary'] = forms.CharField(widget=forms.Textarea(attrs={'width':"100%", 'cols' : "80", 'rows': "4"}),initial=savedSummarySelection)
			pagetitle="Edit project"

		else:
			print('add mode')
			#mode = forms.CharField(required=False, max_length=50, widget=forms.HiddenInput(),initial='new')
			#super(addProjectForm, self).__init__(*args,**kwargs)


	# get static (rather than edit) data for form


	name = forms.CharField(label="Project title", max_length=100)	
	summary = forms.CharField(widget=forms.Textarea(attrs={'width':"100%", 'cols' : "80", 'rows': "4", }))

	companychoice = forms.ChoiceField(label='Company owner', choices=[], required=False)
	businessmodelchoice = forms.ChoiceField(label='Business Model', choices=[], required=False)
	technologychoice = forms.ChoiceField(label='Add Technology', choices=[], required=False)
	marketneedchoice = forms.ChoiceField(label='Market Need Set', choices=[], required=False)
	mode = forms.CharField(required=False, max_length=50, widget=forms.HiddenInput())






class addCompanyForm(forms.Form):

	pagetitle="Add Company"	

	def __init__(self,*args,**kwargs):
		
		if 'identifier' in kwargs:
			identifier = kwargs.pop("identifier")
			print("edit mode")
			if identifier is not None:
				print("identifier exists in form")
				savedNameSelection = graknData=client.execute('match $x isa company, has name $y, has identifier "' +identifier+'"; get;')
				savedSummarySelection = graknData=client.execute('match $x isa company, has summary $y, has identifier "' +identifier+'"; get;')	
				savedNameSelection = savedNameSelection[0]['y']['value']
				savedSummarySelection = savedSummarySelection[0]['y']['value']
				
				super(addCompanyForm, self).__init__(*args,**kwargs)
				self.fields['mode'] = forms.CharField(widget = forms.HiddenInput(), max_length=100, initial=identifier, required=False)
				self.fields['name'] = forms.CharField(label="Project title", max_length=100, initial=savedNameSelection)
				self.fields['summary'] = forms.CharField(widget=forms.Textarea(attrs={'width':"100%", 'cols' : "80", 'rows': "4"}),initial=savedSummarySelection)
				pagetitle="Edit Company"	
		else:
			print('add mode')
			#mode = forms.CharField(required=False, max_length=50, widget=forms.HiddenInput(),initial='new')
			super(addCompanyForm, self).__init__(*args,**kwargs)	

	
	name = forms.CharField(label="Company name", max_length=100)	
	summary = forms.CharField(widget=forms.Textarea(attrs={'width':"100%", 'cols' : "80", 'rows': "4", }))
	mode = forms.CharField(widget = forms.HiddenInput(),initial='identifer not determined')




class addMarketNeedForm(forms.Form):

	pagetitle="Add Market Need"


	def __init__(self,*args,**kwargs):

		identifier=None
		if 'identifier' in kwargs:	
			identifier = kwargs.pop("identifier")

		super(addMarketNeedForm, self).__init__(*args,**kwargs)
		self.fields['marketchoice'] = forms.ChoiceField(label='Sits within market', choices=getEntries('market'), required=False)

		if identifier is not None:			
			print("edit mode")
			savedNameSelection = graknData=client.execute('match $x isa marketneed, has name $y, has identifier "' +identifier+'"; get;')
			savedSummarySelection = graknData=client.execute('match $x isa marketneed, has summary $y, has identifier "' +identifier+'"; get;')
			# NEEDS TO GRAB RELATIONSHIP ON MARKET WHICH NEED SITS IN
			savedNameSelection = savedNameSelection[0]['y']['value']
			savedSummarySelection = savedSummarySelection[0]['y']['value']
			mode = forms.CharField(required=False, max_length=50, widget=forms.HiddenInput(),initial=identifier)
			super(addMarketNeedForm, self).__init__(*args,**kwargs)
			self.fields['name'] = forms.CharField(label="Project title", max_length=100, initial=savedNameSelection)
			self.fields['summary'] = forms.CharField(widget=forms.Textarea(attrs={'width':"100%", 'cols' : "80", 'rows': "4"}),initial=savedSummarySelection)
			pagetitle="Edit Market Need"
		else:
			print('add mode')
			#mode = forms.CharField(required=False, max_length=50, widget=forms.HiddenInput(),initial='new')
			#super(addMarketNeedForm, self).__init__(*args,**kwargs)	


	name = forms.CharField(label="Project title", max_length=100)
	summary = forms.CharField(widget=forms.Textarea(attrs={'width':"100%", 'cols' : "80", 'rows': "4"}))
	marketchoice = forms.ChoiceField(label='Sits within market', choices=[], required=False)

					
	mode = forms.CharField(required=False, max_length=50, widget=forms.HiddenInput())


class addRiskForm(forms.Form):

	pagetitle="Add Risk / Impact factor"

	def __init__(self,*args,**kwargs):

		identifier=None
		if 'identifier' in kwargs:	
			identifier = kwargs.pop("identifier")

		super(addRiskForm, self).__init__(*args,**kwargs)
		self.fields['marketchoice'] = forms.ChoiceField(label='Effects a market:', choices=getEntries('market'), required=False)
		self.fields['businesschoice'] = forms.ChoiceField(label='Effects a businessmodel:', choices=getEntries('businessmodel'), required=False)
		self.fields['technologychoice'] = forms.ChoiceField(label='Effects a technology:', choices=getEntries('technology'), required=False)
	
		if identifier is not None:

			print("Edit mode")
			savedNameSelection = graknData=client.execute('match $x isa risk, has name $y, has identifier "' +identifier+'"; get;')
			savedSummarySelection = graknData=client.execute('match $x isa risk, has summary $y, has identifier "' +identifier+'"; get;')
			# NEEDS TO GRAB RELATIONSHIP ON MARKET WHICH NEED SITS IN
			savedNameSelection = savedNameSelection[0]['y']['value']
			savedSummarySelection = savedSummarySelection[0]['y']['value']
			mode = forms.CharField(required=False, max_length=50, widget=forms.HiddenInput(),initial=identifier)
			super(addRiskForm, self).__init__(*args,**kwargs)
			self.fields['name'] = forms.CharField(label="Project title", max_length=100, initial=savedNameSelection)
			self.fields['summary'] = forms.CharField(widget=forms.Textarea(attrs={'width':"100%", 'cols' : "80", 'rows': "4"}),initial=savedSummarySelection)
			# UPDATE TOP BUSINESS MODEL FIELD !!!!!!!!!!!!!!!!!!!!!!!!!!!1
			#!!!!!!!!!!!!!!!!!!!!!!!!!!!
			pagetitle="Edit risk"
		else:
			print('add mode')
			#mode = forms.CharField(required=False, max_length=50, widget=forms.HiddenInput(),initial='new')
				


	ratings = [(5.0,5.0),(4.0,4.0),(3.0,3.0),(2.0,2.0),(1.0,1.0),(-1.0,-1.0),(-2.0,-2.0),(-3.0,-3.0),(-4.0,-4.0),(-5.0,-5.0)]	

	name = forms.CharField(label="Name", max_length=100)	
	summary = forms.CharField(widget=forms.Textarea(attrs={'width':"100%", 'cols' : "80", 'rows': "4", }))
	score = forms.ChoiceField(label='rating, higher good impact, lower worse risk', choices=ratings, required=True)
	marketchoice = forms.ChoiceField(label='Effects a market:', choices=[], required=False)
	businesschoice = forms.ChoiceField(label='Effects a businessmodel:', choices=[], required=False)
	technologychoice = forms.ChoiceField(label='Effects a technology:', choices=[], required=False)
	mode = forms.CharField(required=False, max_length=50, widget=forms.HiddenInput())




class addBusinessModelForm(forms.Form):

	pagetitle="Add Business Model"

	def __init__(self,*args,**kwargs):

		identifier=None
		if 'identifier' in kwargs:
			identifier = kwargs.pop("identifier")
		super(addBusinessModelForm, self).__init__(*args,**kwargs)	
		self.fields['top'] = forms.ChoiceField(label='Sits within model group', choices=getEntries('businessmodel'), required=False)
		
		if identifier is not None:

			print("Edit mode")
			savedNameSelection = graknData=client.execute('match $x isa businessmodel, has name $y, has identifier "' +identifier+'"; get;')
			savedSummarySelection = graknData=client.execute('match $x isa businessmodel, has summary $y, has identifier "' +identifier+'"; get;')
			# NEEDS TO GRAB RELATIONSHIP ON MARKET WHICH NEED SITS IN
			savedNameSelection = savedNameSelection[0]['y']['value']
			savedSummarySelection = savedSummarySelection[0]['y']['value']
			mode = forms.CharField(required=False, max_length=50, widget=forms.HiddenInput(),initial=identifier)
			super(addBusinessModelForm, self).__init__(*args,**kwargs)
			self.fields['name'] = forms.CharField(label="Project title", max_length=100, initial=savedNameSelection)
			self.fields['summary'] = forms.CharField(widget=forms.Textarea(attrs={'width':"100%", 'cols' : "80", 'rows': "4"}),initial=savedSummarySelection)
			# UPDATE TOP BUSINESS MODEL FIELD
			pagetitle="Edit Business model"
		else:
			print('add mode')
			#mode = forms.CharField(required=False, max_length=50, widget=forms.HiddenInput(),initial='new')
			


	name = forms.CharField(label="Business Model name", max_length=100)	
	summary = forms.CharField(widget=forms.Textarea(attrs={'width':"100%", 'cols' : "80", 'rows': "4", }))
	top = forms.ChoiceField(label='Sits within model group', choices=[], required=False)
	mode = forms.CharField(required=False, max_length=50, widget=forms.HiddenInput())


class addMarketForm(forms.Form):

	def __init__(self,*args,**kwargs):

		identifier=None
		if 'identifier' in kwargs:
			identifier = kwargs.pop("identifier")
		super(addMarketForm, self).__init__(*args,**kwargs)	
		self.fields['top'] = forms.ChoiceField(label='Sits within market', choices=getEntries('market'), required=False)

		pagetitle="Add Market"

		if identifier is not None:
			print("identifier exists")

			print("Edit mode")
			savedNameSelection = graknData=client.execute('match $x isa market, has name $y, has identifier "' +identifier+'"; get;')
			savedSummarySelection = graknData=client.execute('match $x isa market, has summary $y, has identifier "' +identifier+'"; get;')
			# NEEDS TO GRAB RELATIONSHIP ON MARKET WHICH NEED SITS IN
			savedNameSelection = savedNameSelection[0]['y']['value']
			savedSummarySelection = savedSummarySelection[0]['y']['value']
			mode = forms.CharField(required=False, max_length=50, widget=forms.HiddenInput(),initial=identifier)
			super(addMarketForm, self).__init__(*args,**kwargs)
			self.fields['name'] = forms.CharField(label="Project title", max_length=100, initial=savedNameSelection)
			self.fields['summary'] = forms.CharField(widget=forms.Textarea(attrs={'width':"100%", 'cols' : "80", 'rows': "4"}),initial=savedSummarySelection)
			pagetitle="Edit Market"
		else:
			print('add mode')
			#mode = forms.CharField(required=False, max_length=50, widget=forms.HiddenInput(),initial='new')
			


	name = forms.CharField(label="Market name", max_length=100)	
	summary = forms.CharField(widget=forms.Textarea(attrs={'width':"100%", 'cols' : "80", 'rows': "4", }))
	top = forms.ChoiceField(label='Sits within market', choices=[], required=False)
	mode = forms.CharField(required=False, max_length=50, widget=forms.HiddenInput())



class addTechnologyForm(forms.Form):

	pagetitle="Add Technology"

	def __init__(self,*args,**kwargs):

		identifier=None
		if 'identifier' in kwargs:
			identifier = kwargs.pop("identifier")
		super(addTechnologyForm, self).__init__(*args,**kwargs)	
		self.fields['technologychoice'] = forms.ChoiceField(label='part of technology group:', choices=getEntries('technology'), required=False)
	
		if identifier is not None:
			print("identifier exists")

			print("Edit mode")
			savedNameSelection = graknData=client.execute('match $x isa technology, has name $y, has identifier "' +identifier+'"; get;')
			savedSummarySelection = graknData=client.execute('match $x isa technology, has summary $y, has identifier "' +identifier+'"; get;')
			# NEEDS TO GRAB RELATIONSHIP ON MARKET WHICH NEED SITS IN
			savedNameSelection = savedNameSelection[0]['y']['value']
			savedSummarySelection = savedSummarySelection[0]['y']['value']
			mode = forms.CharField(required=False, max_length=50, widget=forms.HiddenInput(),initial=identifier)
			super(addTechnologyForm, self).__init__(*args,**kwargs)
			self.fields['name'] = forms.CharField(label="Project title", max_length=100, initial=savedNameSelection)
			self.fields['summary'] = forms.CharField(widget=forms.Textarea(attrs={'width':"100%", 'cols' : "80", 'rows': "4"}),initial=savedSummarySelection)
			pagetitle="Edit Market Need"
		else:
			print('add mode')
			#mode = forms.CharField(required=False, max_length=50, widget=forms.HiddenInput(),initial='new')
			


	name = forms.CharField(label="Technology name", max_length=100)	
	summary = forms.CharField(widget=forms.Textarea(attrs={'width':"100%", 'cols' : "80", 'rows': "4", }))
	technologychoice = forms.ChoiceField(label='part of technology group:', choices=[], required=False)
	mode = forms.CharField(required=False, max_length=50, widget=forms.HiddenInput())