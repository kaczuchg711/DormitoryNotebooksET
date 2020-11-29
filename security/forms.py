from django import forms

class LoginForm(forms.Form):
    def __init__(self, dormsTupleTuples):
        super().__init__()
        choices = ((x, x.__str__()) for x in dormsTupleTuples)

        self.fields["dorms"] = forms.ChoiceField(choices=choices)
        self.fields["email"] = forms.CharField()
        self.fields["password"] = forms.CharField(widget=forms.PasswordInput)
