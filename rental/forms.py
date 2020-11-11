from django import forms


class RentForm(forms.Form):

    def __init__(self, availableItems):
        super().__init__(),
        choices = list()
        for item in availableItems:
            choices.append((item.number.__str__(), item.number.__str__() + ". " + item.name))

        self.fields["items"] = forms.ChoiceField(choices=choices)
