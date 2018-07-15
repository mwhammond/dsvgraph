from django import forms
import grakn
client = grakn.Client(uri='http://35.197.194.67:4567', keyspace='dsvgraph')



class addProjectForm(forms.Form):

	pagetitle="Add project"

	businessModels = (
    ('Licence at TRL3', 'Licence at TRL3'),
    ('Licence at TRL6', 'Licence at TRL6'),
)


	graknData=client.execute('match $x isa company, has name $y; offset 0; limit 30; get $y;') # dictionaries are nested structures
	companies=[]
	for x in graknData:
		company={x['y']['value'],x['y']['id']}
		companies.append(company)
	companyNames=tuple(companies)


	graknData=client.execute('match $x isa market, has name $y; offset 0; limit 30; get $y;') # dictionaries are nested structures
	markets=[]
	for x in graknData:
		market={x['y']['value'],x['y']['id']}
		markets.append(market)
	marketNames=tuple(markets)

	graknData=client.execute('match $x isa technology, has name $y; offset 0; limit 30; get $y;') # dictionaries are nested structures
	technologies=[]
	for x in graknData:
		technology={x['y']['value'],x['y']['id']}
		technologies.append(technology)
	technologyNames=tuple(technologies)				


	needset = (
    ('not yet connected', 'not yet connected'),
    ('not yet connected', 'not yet connected'),
)

	name = forms.CharField(label="Project title", max_length=100)	
	summary = forms.CharField(widget=forms.Textarea(attrs={'width':"100%", 'cols' : "80", 'rows': "4", }))
	companychoice = forms.ChoiceField(label='Company owner', choices=companyNames, required=False)
	technologychoice = forms.ChoiceField(label='Add Technology', choices=technologyNames, required=False)
	marketchoice = forms.ChoiceField(label='Specific market', choices=marketNames, required=False)

	marketNeedSet = forms.ChoiceField(label='Market Need Set', choices=needset, required=False)






class addCompanyForm(forms.Form):

	pagetitle="Add Company"

	graknData=client.execute('match $x isa market, has name $y; offset 0; limit 30; get $y;') # dictionaries are nested structures
	markets=[]
	for x in graknData:
		market={x['y']['value'],x['y']['id']}
		markets.append(market)
	marketNames=tuple(markets)

	name = forms.CharField(label="Company name", max_length=100)	
	summary = forms.CharField(widget=forms.Textarea(attrs={'width':"100%", 'cols' : "80", 'rows': "4", }))
	#protocompany = forms.BooleanField(label='Protocompany', required=False)
	marketchoice = forms.ChoiceField(label='Sits within market', choices=marketNames, required=False)



class addBusinessModelForm(forms.Form):

	pagetitle="Add Business Model"

	graknData=client.execute('match $x isa businessmodel, has name $y; offset 0; limit 30; get $y;') # dictionaries are nested structures
	things=[]
	for x in graknData:
		thing={x['y']['value'],x['y']['id']}
		things.append(thing)
	businessModelNames=tuple(things)

	name = forms.CharField(label="Business Model name", max_length=100)	
	summary = forms.CharField(widget=forms.Textarea(attrs={'width':"100%", 'cols' : "80", 'rows': "4", }))
	top = forms.ChoiceField(label='Sits within model group', choices=businessModelNames, required=False)




class addMarketForm(forms.Form):

	pagetitle="Add Market"

	graknData=client.execute('match $x isa market, has name $y; offset 0; limit 30; get $y;') # dictionaries are nested structures
	things=[]
	for x in graknData:
		thing={x['y']['value'],x['y']['id']}
		things.append(thing)
	marketNames=tuple(things)

	name = forms.CharField(label="Market name", max_length=100)	
	summary = forms.CharField(widget=forms.Textarea(attrs={'width':"100%", 'cols' : "80", 'rows': "4", }))
	top = forms.ChoiceField(label='Sits within market', choices=marketNames, required=False)




class addTechnologyForm(forms.Form):

	pagetitle="Add Technology"

	graknData=client.execute('match $x isa technology, has name $y; offset 0; limit 30; get $y;') # dictionaries are nested structures
	things=[]
	for x in graknData:
		thing={x['y']['value'],x['y']['id']}
		things.append(thing)
	technologyNames=tuple(things)

	name = forms.CharField(label="Technology name", max_length=100)	
	summary = forms.CharField(widget=forms.Textarea(attrs={'width':"100%", 'cols' : "80", 'rows': "4", }))
	top = forms.ChoiceField(label='part of technology group:', choices=technologyNames, required=False)