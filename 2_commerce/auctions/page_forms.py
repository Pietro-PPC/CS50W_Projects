from django import forms

class NewListingForm(forms.Form):
    title = forms.CharField(label=False, widget=forms.TextInput(
        attrs={'placeholder': 'Title',
            'class': 'form-control'
        })
    )
    description = forms.CharField(label=False, widget=forms.Textarea(
        attrs={'class': 'form-control'}
    ))
    minimum_bid = forms.FloatField(label=False, widget=forms.NumberInput(
        attrs={'class': 'form-control', 'step':"0.01"}
    ))
    category = forms.CharField(label=False, required=False, widget=forms.TextInput(
        attrs={'class': 'form-control'}
    ))
    url = forms.URLField(label=False, required=False, widget=forms.TextInput(
        attrs={'class': 'form-control'}
    ))