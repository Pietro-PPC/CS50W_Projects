from django import forms

class NewListingForm(forms.Form):
    title = forms.CharField(label=False, widget=forms.TextInput(
        attrs={'placeholder': 'Title',
            'class': 'form-control new-listing'
        })
    )
    description = forms.CharField(label=False, widget=forms.Textarea(
        attrs={'class': 'form-control new-listing',
            'placeholder': 'Item description '}
    ))
    minimum_bid = forms.FloatField(label=False, widget=forms.NumberInput(
        attrs={'class': 'form-control new-listing',
            'placeholder': 'Starting Price (US$)'}
    ))
    category = forms.CharField(label=False, required=False, widget=forms.TextInput(
        attrs={'class': 'form-control new-listing',
            'placeholder': 'Category (optional)'}

    ))
    url = forms.URLField(label=False, required=False, widget=forms.TextInput(
        attrs={'class': 'form-control new-listing',
            'placeholder': 'Image URL (optional)'}
    ))