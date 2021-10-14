from django.forms import ModelForm
from .models import new
from django.forms import Textarea, TextInput
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.forms.widgets import FileInput

class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username','first_name','last_name', 'email', 'password1', 'password2',]

class DateInput(forms.DateInput):
    input_type = 'date'
    
class newForm(ModelForm):
    class Meta:
        model = new
        fields = ["fname", "address","lname", "email", "dob", "gender", "aadharn", "rnumber", "pann","high","senior", "aadhar","pan","graduation","masters","phd" ,"college","mobile"]
    
        widgets = {
            "fname": TextInput(attrs={"placeholder": "First name",}),
            "lname": TextInput(attrs={"placeholder": "Last name",}),
            #"dob": TextInput(attrs={"placeholder": "mm/dd/yyyy",}),
            'dob': DateInput(),
        }

TRUE_FALSE_CHOICES = (
    (True, 'Aprrove'),
    (False, 'Decline')
)
class approval(ModelForm):
    class Meta:
        model = new
        fields = ["status1","comment1"] 
        widgets = {
            "status1": forms.Select(choices=TRUE_FALSE_CHOICES),
            #'status1': forms.RadioSelect,
            "comment1": TextInput(attrs={"placeholder": "comment",}),
        } 
class approval2(ModelForm):
    class Meta:
        model = new
        fields = ["status2","comment2"] 
        widgets = {
            "status2": forms.Select(choices=TRUE_FALSE_CHOICES),
            #'status1': forms.RadioSelect,
            "comment3": TextInput(attrs={"placeholder": "comment",}),
        } 
class approval3(ModelForm):
    class Meta:
        model = new
        fields = ["status3","comment3"] 
        widgets = {
            "status3": forms.Select(choices=TRUE_FALSE_CHOICES),
            #'status1': forms.RadioSelect,
            "comment3": TextInput(attrs={"placeholder": "comment",}),
        }  

class update1(ModelForm):
    class Meta:
        model = new
        fields = ["fname", "address","lname", "email", "gender", "dob","aadharn", "rnumber", "pann","high","senior", "aadhar","pan","graduation","masters","phd" ,"college","mobile"]
        
    



    