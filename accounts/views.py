from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import new, employer
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

from django.contrib.auth.mixins import AccessMixin
from django.contrib.auth.models import Group
from .decorators import unauthenticated_user, allowed_users
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from braces.views import GroupRequiredMixin
from django.core.mail import send_mail
from django.contrib import messages
from django.template.loader import get_template
import accounts


# Create your views here.

def home(request):
    return render(request, 'accounts/home.html')

@login_required(login_url='login')
def form_submitted(request):
    return render(request, 'accounts/form_submitted.html')

@login_required(login_url='login')
def nodetail(request):
    return render(request, 'accounts/nodetail.html')

@login_required(login_url='login')
def nodetail2(request):
    return render(request, 'accounts/nodetail2.html')

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
            
            return redirect('register')

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
            elif request.user.groups.filter(name = 'admin1').exists():
                return redirect('admin1')
            elif request.user.groups.filter(name = 'admin2').exists():
                return redirect('admin2')
            elif request.user.groups.filter(name = 'director').exists():
                return redirect('director')
            else:
                return HttpResponse('Sorry')
        else:
            messages.error(request, "Username, password or email is incorrect.")
            return redirect('register')
                 

    context = {}
    return render(request, 'accounts/register.html', context)


    

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
@allowed_users(allowed_roles=['employee'])
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
                    m = m + i + ' '+ ':' + ' '+ body[i] + '\n'

                m = m+ "For more details please visit the website https://hr-onboarding-cli.herokuapp.com/"
                send_mail(subject, m, '', ['accept1iiitl@gmail.com'], fail_silently=False)
                form.save()
                new.status1 = None
                new.status2 = None
                new.status3 = None
                messages.success(request, 'You data has been stored successfully.')
                return redirect('form_submitted')
            
    context = {'form':form}
    return render(request, 'accounts/new_form.html', context)

@allowed_users(allowed_roles=['employee'])
def info(request):
    model = new
    return render(request, 'accounts/info.html')

@allowed_users(allowed_roles=['employee'])
def status(request):
    model = new
    return render(request, 'accounts/status.html')

@allowed_users(allowed_roles=['employee'])
def update(request, pk):
    gh = new.objects.get(id=pk)
    form = update1()
    form = update1(request.POST or None, request.FILES or None, instance = gh)
    if form.is_valid():
        if gh.status1 == False: 
            msg = gh.fname + " "+ gh.lname+ " has updated their document on Admin1's given review.\n\n"+"Review: "+gh.comment1

        if gh.status2 == False:
            msg = gh.fname + " "+ gh.lname+ " has updated their document on Admin2's given review.\n\n"+"Review: "+gh.comment2

        if gh.status3 == False:
            msg = gh.fname + " "+ gh.lname+ " has updated their document on Director's given review.\n\n"+"Review: "+gh.comment3
        gh.status1 = None
        gh.status2 = None
        gh.status3 = None
        gh.comment1 = None
        gh.comment2 = None
        gh.comment3 = None
        send_mail('[Important] Document Update', msg, '', ['accept1iiitl@gmail.com'], fail_silently=False)
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

     
class approve_1(AccessMixin, ListView):
    
    template_name = 'accounts/approve_1.html'
    context_object_name = 'news'
    model = new
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        if not self.request.user.groups.filter(name="admin1").exists():
            # Redirect the user to somewhere else - add your URL here
            return HttpResponse("You are not authorized to view this page")

        # Checks pass, let http method handlers process the request
        return super().dispatch(request, *args, **kwargs)


class history1(AccessMixin, ListView):
    template_name = 'accounts/history.html'
    context_object_name = 'news'
    model = new
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        if not self.request.user.groups.filter(name="admin1").exists():
            # Redirect the user to somewhere else - add your URL here
            return HttpResponse("You are not authorized to view this page")

        # Checks pass, let http method handlers process the request
        return super().dispatch(request, *args, **kwargs)
    

class admin2(AccessMixin, ListView):
    template_name = 'accounts/admin2dash.html'
    context_object_name = 'news'
    model = new
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        if not self.request.user.groups.filter(name="admin2").exists():
            # Redirect the user to somewhere else - add your URL here
            return HttpResponse("You are not authorized to view this page")

        # Checks pass, let http method handlers process the request
        return super().dispatch(request, *args, **kwargs)


class history2(AccessMixin, ListView):
    template_name = 'accounts/history2.html'
    context_object_name = 'news'
    model = new
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        if not self.request.user.groups.filter(name="admin2").exists():
            # Redirect the user to somewhere else - add your URL here
            return HttpResponse("You are not authorized to view this page")

        # Checks pass, let http method handlers process the request
        return super().dispatch(request, *args, **kwargs)


class director(AccessMixin, ListView):
    template_name = 'accounts/directordash.html'
    context_object_name = 'news'
    model = new
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        if not self.request.user.groups.filter(name="director").exists():
            # Redirect the user to somewhere else - add your URL here
            return HttpResponse("You are not authorized to view this page")

        # Checks pass, let http method handlers process the request
        return super().dispatch(request, *args, **kwargs)


class history3(AccessMixin, ListView):
    template_name = 'accounts/history3.html'
    context_object_name = 'news'
    model = new
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        if not self.request.user.groups.filter(name="director").exists():
            # Redirect the user to somewhere else - add your URL here
            return HttpResponse("You are not authorized to view this page")

        # Checks pass, let http method handlers process the request
        return super().dispatch(request, *args, **kwargs)

class details(AccessMixin, UpdateView, DetailView):
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
        body = {
                    'Name': hi.fname+" "+hi.lname,                
                    'E-mail': hi.email,
                    'Phone number': hi.mobile,
                    'Registration Number': hi.rnumber,
                
                }
        if hi.status1 == True:
            msg2 = "Hello\n\nA new applicant has been approved by Admin1."
            for i in body:
                    msg2 = msg2+ i + ' '+ ':' + ' '+ body[i] + '\n'
            msg2 = msg2+ "For more details please visit the website https://hr-onboarding-cli.herokuapp.com/"
            msg1 = hi.fname + " " + hi.lname + ", your request has been approved by admin1 for further process."
            send_mail('[Important] Approved by Admin1', msg1, '', [hi.email], fail_silently=False)
            send_mail('[Important]'+ hi.fname+" "+hi.lname+'has been approved by Admin1', msg2, '', ['accept2iiitl@gmail.com'], fail_silently=False)
        else:
            msg = "Reason given by Admin1 for declining your request\n"+ hi.comment1 + "\n\n Please update your details on https://hr-onboarding-cli.herokuapp.com/"
            send_mail('[Important] Declined by Admin1', msg, '', [hi.email], fail_silently=False)
        return redirect('admin1')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        if not self.request.user.groups.filter(name="admin1").exists():
            # Redirect the user to somewhere else - add your URL here
            return HttpResponse("You are not authorized to view this page")

        # Checks pass, let http method handlers process the request
        return super().dispatch(request, *args, **kwargs)



class details2(AccessMixin, UpdateView, DetailView):
    template_name = 'accounts/new2.html'
    context_object_name = 'new'
    model = new
    form_class = approval2
    success_url = reverse_lazy('admin2')

    def form_valid(self, form):
        form.save()
        hi = self.get_object()
        hi.status3 = None
        body = {
                    'Name': hi.fname+" "+hi.lname,                
                    'E-mail': hi.email,
                    'Phone number': hi.mobile,
                    'Registration Number': hi.rnumber,
                
                }
        if hi.status2 == True:
            msg2 = "Hello\n\nA new applicant has been approved by Admin2."
            for i in body:
                    msg2 = msg2+ i + ' '+ ':' + ' '+ body[i] + '\n'
            msg2 = msg2+ "For more details please visit the website https://hr-onboarding-cli.herokuapp.com/"
            msg = hi.fname + " " + hi.lname + " , your request has been approved by admin2 for further process."
            send_mail('[Important]'+ hi.fname+" "+hi.lname+'has been approved by Admin2', msg2, '', ['accept3iiitl@gmail.com'], fail_silently=False)
            send_mail('[Important] Approved by Admin2', msg, '', [hi.email], fail_silently=False)
        else:
            msg = "Reason given by Admin2 for declining your request\n\n"+hi.comment2 + "\n\n Please update your details on https://hr-onboarding-cli.herokuapp.com/"
            send_mail('[Imortant] Declined by Admin2', msg, '', [hi.email], fail_silently=False)
        return redirect('admin2')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        if not self.request.user.groups.filter(name="admin2").exists():
            # Redirect the user to somewhere else - add your URL here
            return HttpResponse("You are not authorized to view this page")

        # Checks pass, let http method handlers process the request
        return super().dispatch(request, *args, **kwargs)



class details3(AccessMixin, UpdateView, DetailView):
    group_required = u"director"
    template_name = 'accounts/new3.html'
    context_object_name = 'new'
    model = new
    form_class = approval3
    success_url = reverse_lazy('director')
    
    

    def form_valid(self, form):
        x = employer.objects.values_list('email', flat = True)
        form.save()
        hi = self.get_object()
        if hi.status3 == True:
            msg1 = hi.fname + " " + hi.lname + ", your request has been approved by director.\nFurther proceedings will be informed to you by respective staff."
            send_mail('[Important] Approved by Director', msg1, '', [hi.email], fail_silently=False)
            msg2 = hi.fname + " " + hi.lname + " has been approved by Director. \n\nPlease contact this person as soon as possible for further proceedings of respected departments.\n"
            msg2 = msg2 + "Name: " + hi.fname+ " " + hi.lname + "\nEmail: " + hi.email + "\nMobile: " + hi.mobile
            send_mail('[Important] New person has been approved by Director', msg2, '', x, fail_silently=False) 
        if hi.status3 == False:
            msg = "Reason given by Director for declining your request\n\n"+ hi.comment3 + "\n\n Please update your details on https://hr-onboarding-cli.herokuapp.com/"
            send_mail('[Important] Declined by Director', msg, '', [hi.email], fail_silently=False)
        return redirect('director')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        if not self.request.user.groups.filter(name="director").exists():
            # Redirect the user to somewhere else - add your URL here
            return HttpResponse("You are not authorized to view this page")

        # Checks pass, let http method handlers process the request
        return super().dispatch(request, *args, **kwargs)
        




    

