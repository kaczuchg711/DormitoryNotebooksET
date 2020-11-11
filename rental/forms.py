from django import forms


class RentForm(forms.Form):

    def __init__(self, availableItems):
        super().__init__(),
        option_name = list()
        for item in availableItems:
            option_name.append(item.number.__str__() + " " + item.name)
        choices = [
            ('FR', 'Freshman'),
            ('SO', 'Sophomore'),
            ('JR', 'Junior'),
            ('SR', 'Senior'),
            ('GR', 'Graduate'),
        ]
        # choices = ((x, x.__str__()) for x in ItemsTupleTuples)

        self.fields["items"] = forms.ChoiceField(choices=choices)

# class LoginForm(forms.Form):
#
#     def __init__(self, dormsTupleTuples):
#         super().__init__()
#
#         choices = ((x, x.__str__()) for x in dormsTupleTuples)
#
#         self.fields["dorms"] = forms.ChoiceField(choices=choices)
#         self.fields["email"] = forms.CharField()
#         self.fields["password"] = forms.CharField(widget=forms.PasswordInput)
