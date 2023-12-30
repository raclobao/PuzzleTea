from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.forms.widgets import PasswordInput, TextInput, NumberInput

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput)
    password = forms.CharField(widget=PasswordInput)  

class ShoppingForm(forms.Form):
    quantity = forms.IntegerField(min_value= 1, widget=NumberInput(attrs={'style':'width:40px;'}))

class AddressForm(forms.Form):
    address = forms.CharField(widget=TextInput)
