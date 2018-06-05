from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Item


class SignUpForm(UserCreationForm):
    phone = forms.CharField(max_length=10, help_text='Required. Inform a valid 10 digit phone number.')
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'phone', 'password1', 'password2')

class ItemForm(forms.ModelForm):
    """Image upload form."""
    street = forms.CharField(max_length=32, required=False) 
    street_no = forms.CharField(max_length=16, required=False) 
    city = forms.CharField(max_length=16, required=True) 
    state = forms.CharField(max_length=16, required=True) 
    location_desc = forms.CharField(max_length=256,required=False)
    picture = forms.ImageField(required=False)
    class Meta:
       model = Item 
       fields = ('cat', 'subCat', 'date', 'street', 'street_no', 'city', 'state', 'location_desc','color', 'title', 'description', 'picture',)

