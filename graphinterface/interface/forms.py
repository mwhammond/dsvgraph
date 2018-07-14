from django import forms


class addProjectForm(forms.Form):

	pagetitle="Add project"

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

	projectName = forms.CharField(label="Project title", max_length=100)	
	summary = forms.CharField(widget=forms.Textarea(attrs={'width':"100%", 'cols' : "80", 'rows': "4", }))
	withinCompany = forms.ChoiceField(label='Company owner', choices=companyNames)
	topmarket = forms.ChoiceField(label='Specific market', choices=markets)
	marketNeedSet = forms.ChoiceField(label='Market Need Set', choices=needset)


class addCompanyForm(forms.Form):

	pagetitle="Add Company"

	businessModels = (
    ('Licence at TRL3', 'Licence at TRL3'),
    ('Licence at TRL6', 'Licence at TRL6'),
)

	markets = (
    ('Alzhiemers', 'Alzhiemers'),
    ('Energy Storage', 'Energy storage'),
)

	needset = (
    ('Alzhiemers', 'New models in Alzhiemers'),
    ('Energy Storage', 'Automotive energy'),
)

	companyName = forms.CharField(label="Company name", max_length=100)	
	summary = forms.CharField(widget=forms.Textarea(attrs={'width':"100%", 'cols' : "80", 'rows': "4", }))
	protocompany = forms.BooleanField(label='Protocompany', required=False)
	topmarket = forms.ChoiceField(label='Specific market', choices=markets)

