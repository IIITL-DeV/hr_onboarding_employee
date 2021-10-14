from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import new
from django.urls import reverse
from .forms import newForm, approval, CreateUserForm, approval2, approval3, update1
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, FormMixin, UpdateView
from django.urls import reverse_lazy
from django.forms import Textarea
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.models import Group
from .decorators import unauthenticated_user, allowed_users
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.core.mail import send_mail
from django.contrib import messages
from django.template.loader import get_template
import accounts

# Create your views here.
@unauthenticated_user
def home(request):
    return render(request, 'accounts/home.html')

@login_required(login_url='login')
def form_submitted(request):
    return render(request, 'accounts/form_submitted.html')


@unauthenticated_user
def registerPage(request):

    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            group = Group.objects.get(name = 'employee')
            user.groups.add(group)
            messages.success(request, 'Account was created for '+ username)
            return redirect('login')

    context = {'form':form}
    return render(request, 'accounts/register.html', context)

@unauthenticated_user
def loginPage(request):
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_id = request.user.id
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if request.user.groups.filter(name = 'employee').exists():
                if new.objects.filter(user=request.user).exists():
                    return redirect('form_submitted')
                else:
                    return redirect('upload')
            else:
                return HttpResponse('Sorry')

        else:
            messages.info(request, 'Username OR password is incorrect')
    context = {}
    return render(request, 'accounts/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')
"""
class upload(CreateView):
    model = new
    context_object_name = 'upload'
    form_class = newForm
    success_url = reverse_lazy('home')

"""
#@allowed_users(allowed_roles=['employee'])
def upload(request):
    model = new
    form = newForm()
    if request.method == 'POST':
            if new.objects.filter(user=request.user).exists():
                return HttpResponse('form was already submitted')  
            form = newForm(request.POST, request.FILES)
            form.instance.user = request.user
            if form.is_valid():
                body = {
                    'Name': form.cleaned_data['fname'] +' ' +form.cleaned_data['lname'],                
                    'E-mail': form.cleaned_data['email'],
                    'Phone number': form.cleaned_data['mobile'],
                    'Registration Number': form.cleaned_data['rnumber'],
                
                }
                subject = "[Important]"+' '+body["Name"]+' '+"has uploaded the documents for validation."
                m = 'Hello\n\n A new employee has uploaded their document their information is below:\n\n'
                #message = 'New user has been added\n'+'\n'.join(body.values())
                for i in body:
                    m = m+ i + ' '+ ':' + ' '+ body[i] + '\n'

                m = m+ "For more details please visit the website."
                send_mail(subject, m, '', [''], fail_silently=False)
                form.save()
                new.status1 = None
                new.status2 = None
                new.status3 = None
                messages.success(request, 'You data has been stored succesfully.')
                return redirect('form_submitted')
    context = {'form':form}
    return render(request, 'accounts/new_form.html', context)

def info(request):
    model = new
    return render(request, 'accounts/info.html')

def status(request):
    model = new
    return render(request, 'accounts/status.html')

def update(request, pk):
    gh = new.objects.get(id=pk)
    form = update1()
    form = update1(request.POST or None, request.FILES or None, instance = gh)
    if form.is_valid():
        if gh.status1 == False: 
            msg = gh.fname + " "+ gh.lname+ " has updated their document on Admin1's given review.\n"+gh.comment1

        if gh.status2 == False:
            msg = gh.fname + " "+ gh.lname+ " has updated their document on Admin2's given review.\n"+gh.comment2

        if gh.status3 == False:
            msg = gh.fname + " "+ gh.lname+ " has updated their document on Director's given review.\n"+gh.comment3
        gh.status1 = None
        gh.status2 = None
        gh.status3 = None
        gh.comment1 = None
        gh.comment2 = None
        gh.comment3 = None
        send_mail('[Important] Document Update', msg, '', [''], fail_silently=False)
        messages.success(request, 'You data has been updated succesfully.')
        form.save()
        return redirect('form_submitted')
    return render(request, 'accounts/update.html', {'form': form})
"""
class update(LoginRequiredMixin, UpdateView):
    template_name = 'accounts/update.html'
    model = new
    fields = ["fname", "address","lname", "email", "dob", "gender", "aadharn", "rnumber", "pann","high","senior", "aadhar","pan","graduation","masters","phd" ,"college","mobile"]
    success_url = reverse_lazy('home')
"""
      
class approve_1(LoginRequiredMixin, ListView):
    template_name = 'accounts/approve_1.html'
    context_object_name = 'news'
    model = new
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

class history1(LoginRequiredMixin, ListView):
    template_name = 'accounts/history.html'
    context_object_name = 'news'
    model = new
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    

class admin2(LoginRequiredMixin, ListView):
    template_name = 'accounts/admin2dash.html'
    context_object_name = 'news'
    model = new
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

class history2(LoginRequiredMixin, ListView):
    template_name = 'accounts/history2.html'
    context_object_name = 'news'
    model = new
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

class director(LoginRequiredMixin, ListView):
    template_name = 'accounts/directordash.html'
    context_object_name = 'news'
    model = new
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

class history3(LoginRequiredMixin, ListView):
    template_name = 'accounts/history3.html'
    context_object_name = 'news'
    model = new
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

class details(UpdateView, DetailView):
    template_name = 'accounts/new.html'
    context_object_name = 'new'
    model = new
    form_class = approval
    success_url = reverse_lazy('admin1')

    def form_valid(self, form):
        form.save()
        hi = self.get_object()
        hi.status2 = None
        hi.status3 = None
        if hi.status1 == True:
            msg = hi.fname + " " + hi.lname + ", your request has been approved by admin1 for further process."
            send_mail('[Important] Approved by Admin1', msg, '', [hi.email], fail_silently=False)
        else:
            msg = "Reason given by Admin1 for declining your request\n"+ hi.comment1
            send_mail('[Important] Declined by Admin1', msg, '', [hi.email], fail_silently=False)
        return redirect('admin1')

class details2(UpdateView, DetailView):
    template_name = 'accounts/new2.html'
    context_object_name = 'new'
    model = new
    form_class = approval2
    success_url = reverse_lazy('admin2')

    def form_valid(self, form):
        form.save()
        hi = self.get_object()
        hi.status3 = None
        if hi.status2 == True:
            msg = hi.fname + " " + hi.lname + " , your request has been approved by admin2 for further process."
            send_mail('[Important] Approved by Admin2', msg, '', [hi.email], fail_silently=False)
        else:
            msg = "Reason given by Admin1 for declining your request\n"+hi.comment2
            send_mail('[Imortant] Declined by Admin2', msg, '', [hi.email], fail_silently=False)
        return redirect('admin2')

class details3(UpdateView, DetailView):
    template_name = 'accounts/new3.html'
    context_object_name = 'new'
    model = new
    form_class = approval3
    success_url = reverse_lazy('director')

    def form_valid(self, form):
        form.save()
        hi = self.get_object()
        if hi.status3 == True:
            msg1 = hi.fname + " " + hi.lname + ", your request has been approved by director.\nFurther proceedings will be informed to you by respective staff."
            send_mail('[Important] Approved by Director', msg1, '', [hi.email], fail_silently=False)
            msg2 = hi.fname + " " + hi.lname + " has been approved by Director. \nPlease contact this person as soon as possible for further proceedings.\n"
            msg2 = msg2 + "Name: " + hi.fname+ " " + hi.lname + "\nEmail: " + hi.email + "\nMobile: " + hi.mobile
            send_mail('[Important] New person has been approved by Director', msg2, '', [], fail_silently=False) 
        if hi.status3 == False:
            msg = "Reason given by Admin1 for declining your request\n"+ hi.comment3
            send_mail('[Important] Declined by Director', msg, '', [hi.email], fail_silently=False)
        return redirect('director')
        




    

