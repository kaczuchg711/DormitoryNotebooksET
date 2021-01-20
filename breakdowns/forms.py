from django import forms


class BreakdownForm(forms.Form):
    description = forms.CharField(widget=forms.TextInput(attrs={'style': 'width:40%', "placeholder": "Opis awarii"}))
