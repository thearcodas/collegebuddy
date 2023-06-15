from django import forms

class MaterialForm(forms.Form):
    title= forms.CharField()
    fileupload = forms.FileField(
        label='Select a file'
    )
    desc=forms.CharField(widget= forms.Textarea)