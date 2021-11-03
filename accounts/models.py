from django.db import models
import datetime
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
# Create your models here.

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/beat/author/<filename>
    return 'beat/{0}/{1}'.format(instance.user, filename)


class new(models.Model):
    BOOL_CHOICES = ((True, 'Approve'), (False, 'Decline'))
    GENDER = (
    (None, 'Gender'),
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Custom', 'Custom'),
    ('Prefer Not To Say', 'Prefer Not To Say'),
    )
    user = models.OneToOneField(User ,null = True, on_delete=models.CASCADE)
    fname = models.CharField(max_length=200, null=True)
    lname = models.CharField(max_length=200, null=True)
    rnumber = models.CharField(max_length=50, null=True)
    aadharn = models.CharField(max_length=20,null=True)
    pann = models.CharField(max_length=20, null=True)
    email = models.EmailField(max_length=50, null=True)
    address = models.CharField(max_length=500, null = True)
    dob = models.DateField(("Date"), default=None, null = True)
    #dob1 = models.DateField(auto_now=False, auto_now_add=False)
    gender = models.CharField(max_length=10, null = True)
    gender1= models.CharField(max_length=50, choices=GENDER, verbose_name="gender", blank=True)
    high = models.FileField(upload_to=user_directory_path, default= None, null = True)
    senior = models.FileField(upload_to=user_directory_path, default= None, null = True)
    aadhar = models.FileField(upload_to=user_directory_path, default= None, null = True)
    pan = models.FileField(upload_to=user_directory_path, default= None, null = True)
    graduation = models.FileField(upload_to=user_directory_path, default= None, null = True)
    masters = models.FileField(upload_to=user_directory_path, default= None, null = True)
    phd = models.FileField(upload_to=user_directory_path, default= None, null = True)
    college = models.FileField(upload_to=user_directory_path, default= None, null = True)
    mobile = models.CharField(max_length=50, null = True)
    comment1 = models.CharField(max_length= 2000, null = True, blank = True)
    comment2 = models.CharField(max_length= 2000, null = True, blank = True)
    comment3 = models.CharField(max_length= 2000, null = True, blank = True)
    status1 = models.BooleanField(choices=BOOL_CHOICES, blank=True, null=True, default=None)
    status2 = models.BooleanField(choices=BOOL_CHOICES, blank=True, null=True, default=None)
    status3 = models.BooleanField(choices=BOOL_CHOICES, blank=True, null=True, default=None)


    def __str__(self):
        return '{} {} '.format(self.fname, self.lname)

class employer(models.Model):
    fname = models.CharField(max_length=200, null=True)
    lname = models.CharField(max_length=200, null=True)
    designation = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=50, null=True)
    
    def __str__(self):
        return self.designation



