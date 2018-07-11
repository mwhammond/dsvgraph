from django import forms

class addCompanyForm(forms.Form):
	projectName = forms.CharField(label="Project title", max_length=100)	
	summary = forms.CharField(widget=forms.Textarea(attrs={'width':"100%", 'cols' : "80", 'rows': "4", }))



	businessModels = (
    ('Licence at TRL3', 'Licence at TRL3'),
    ('Licence at TRL6', 'Licence at TRL6'),
)

	companyNames = (
    ('DSV', 'DSV'),
    ('Cortexica', 'Cortexica'),
)

	markets = (
    ('Alzhiemers', 'Alzhiemers'),
    ('Energy Storage', 'Energy storage'),
)

	needset = (
    ('Alzhiemers', 'New models in Alzhiemers'),
    ('Energy Storage', 'Automotive energy'),
)


	withinCompany = forms.ChoiceField(label='Company owner', choices=companyNames)
	protocompany = forms.BooleanField(label='Protocompany', required=False)


	topmarket = forms.ChoiceField(label='Specific market', choices=markets)
	marketNeedSet = forms.ChoiceField(label='Market Need Set', choices=needset)

