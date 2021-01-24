from django import forms


class BreakdownForm(forms.Form):
    description = forms.CharField(widget=forms.TextInput(attrs={'style': 'width:40%', "placeholder": "Opis awarii"}))


class RemoveBreakdownForm(forms.Form):
    id = forms.IntegerField()
    button_flag = 1
    def __init__(self, id):
        super().__init__()
        self.fields["id"] = forms.IntegerField(initial=id)
        self.fields["id"].widget = forms.HiddenInput()