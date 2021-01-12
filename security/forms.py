from django import forms

from global_fun import print_with_enters


class LoginForm(forms.Form):
    def __init__(self, dormsTupleTuples):
        super().__init__()
        choices = ((x, x.__str__()) for x in dormsTupleTuples)

        self.fields["dorms"] = forms.ChoiceField(choices=choices)
        self.fields["email"] = forms.CharField()
        self.fields["password"] = forms.CharField(widget=forms.PasswordInput)


from django import forms
from django.contrib.auth.forms import UserCreationForm
from users.models import CustomUser


class registrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    room = forms.CharField(max_length=10, required=True)
    dorm = forms.ChoiceField()

    def __init__(self,dormsTupleTuples, *args, **kwargs):
        super().__init__(*args, **kwargs)
        choices = ((x, x.__str__()) for x in dormsTupleTuples)
        print_with_enters(choices)
        self.fields["dorm"] = forms.ChoiceField(choices=choices)

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', "dorm", 'room', 'password1', 'password2')
