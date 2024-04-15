from django.shortcuts import render,redirect
from django.forms import inlineformset_factory
from .models import *
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .decoraters import unauth_user
from django.contrib.auth.models import Group
from .forms import DonorForm,CreateUserForm
from django.core.mail import send_mail


# Create your views here.

@login_required(login_url='login')
def home(request):
    send_mail(
    "Thank you for registration",
    "Here is the message. hviuefvgebnv;oef vjkebvernv e",
    "dummy.bloodbank1@gmail.com",
    ["primesussy@gmail.com"],
    fail_silently=False,
)
    return render(request,'BloodBank/home.html')


@unauth_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password =request.POST.get('password')
        #authenticates the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user) #django inbuilt login fucntion
            return redirect('home')
        else:
            messages.info(request, 'Username OR password is incorrect')

    context = {}
    return render(request, 'BloodBank/login.html', context)
    

def logoutUser(request):
	logout(request) #django inbuilt logout function
	return redirect('login')


def register(request):
    form=DonorForm()
    if request.method=='POST':
        form=DonorForm(request.POST)
        if form.is_valid():
            form.save()
    
            return redirect('/')

    context={'form':form}
    return render(request,'BloodBank/register.html',context)

@unauth_user
def Admin_register(request):
    form=CreateUserForm()
    if request.method=='POST':
        form=CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
    
            return redirect('/')

    context={'form':form}
    return render(request,'BloodBank/admin_form.html',context)
