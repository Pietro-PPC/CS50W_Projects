from django import forms

class NewListingForm(forms.Form):
    title = forms.CharField(label=False, widget=forms.TextInput(
        attrs={'placeholder': 'Title',
        })
    )
    description = forms.CharField(widget=forms.Textarea)
    starting_bid = forms.FloatField()
    category = forms.CharField(required=False)
    url = forms.URLField(required=False, label="Image URL")