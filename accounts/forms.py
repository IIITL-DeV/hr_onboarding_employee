from django.forms import ModelForm
from .models import new
from django.forms import Textarea, TextInput
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username','first_name','last_name', 'email', 'password1', 'password2',]

class newForm(ModelForm):
    class Meta:
        model = new
        fields = ["fname", "address","lname", "email", "dob", "gender", "aadharn", "rnumber", "pann", "dlink", "mobile", "submitted"]
    
        widgets = {
            "fname": TextInput(attrs={"placeholder": "First name",}),
            "mname": TextInput(attrs={"placeholder": "Middle name",}),
            "lname": TextInput(attrs={"placeholder": "Last name",}),
            "dob": TextInput(attrs={"placeholder": "mm/dd/yyyy",}),
        }
class approval(ModelForm):
    class Meta:
        model = new
        fields = ["approved1", "declined1", "comment1"] 
        widgets = {
            "comment": TextInput(attrs={"placeholder": "comment",}),
        }  



    