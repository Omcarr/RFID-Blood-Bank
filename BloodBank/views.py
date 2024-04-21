from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .decoraters import unauth_user
from django.contrib.auth.models import Group
from .forms import DonorForm,CreateUserForm,DonationDriveForm,CreateAdminForm
from django.core.mail import send_mail
from django.db.models import Count

# Create your views here.

@login_required(login_url='login')
def home(request):
#     send_mail(
#     "Thank you for registration",
#     "Here is the message. hviuefvgebnv;oef vjkebvernv e",
#     "dummy.bloodbank1@gmail.com",
#     ["primesussy@gmail.com"],
#     fail_silently=False,
# )
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
	logout(request)
	return redirect('login')

@unauth_user
def Admin_register(request):
    form=CreateAdminForm()
    if request.method=='POST':
        form=CreateAdminForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')

    context={'form':form}
    return render(request,'BloodBank/admin_form.html',context)


@login_required(login_url='login')
def CreateDrive(request):
    form=DonationDriveForm()
    #get names of all veneues from db and only let the drive sav eif the venue name was unique else throw an error
    if request.method=='POST':
        form=DonationDriveForm(request.POST)
        if form.is_valid():
            venue = form.cleaned_data['Venue']
            if DonationDrive.objects.filter(Venue=venue).exists():
                # Venue already exists, raise a validation error
                form.add_error('Venue', 'A drive with this venue already exists.')
            else:
                group = Group.objects.create(name=venue)

                form.instance.created_by = request.user
                form.instance.group = group  # Associate group with the form instance
                form.save()
                return redirect('register', group_id=group.id)

    context={'form':form}
    return render(request,'BloodBank/new_drive.html',context)


@login_required(login_url='login')
def register(request, group_id):
    form = DonorForm()
    group = Group.objects.get(id=group_id)
    
    # Get blood group counts for donors within the same group
    blood_group_counts = Donor.objects.filter(groups__id=group_id).values('Bloodgroup').annotate(count=Count('Bloodgroup'))
    
    if request.method == 'POST':
        form = DonorForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['Name']
            user = User.objects.create_user(username=username)
            user.save()

            # Associate the user with the donor and the group
            donor = form.save(commit=False)
            donor.user = user
            donor.save()
            donor.groups.add(group)  # Associate the donor with the group

            return redirect('register', group_id=group.id)

    context = {'form': form, 'group_id': group_id, 'blood_group_counts': blood_group_counts}
    return render(request, 'BloodBank/register.html', context)


@login_required(login_url='login')
def admin_dashboard(request):
    drives = DonationDrive.objects.filter(created_by=request.user)
    context = {'drives': drives}
    return render(request,'BloodBank/admin_dashboard.html',context)



@login_required(login_url='login')
def drive_details(request, drive_name):
    drive = Group.objects.get(name=drive_name)
    donor_list=Donor.objects.filter(groups=drive)
    print(donor_list)
    donor_blood_group = Donor.objects.filter(groups=drive).values('Bloodgroup').annotate(count=Count('Bloodgroup'))
    context = {'drive':drive, 'donors': donor_blood_group,'donor_list':donor_list}
    return render(request, 'BloodBank/drive_dets.html', context)


#to-do
#unique drive name fix
#mail to the donor when register for a drive along with an attchment
#dd a counter to show many users have been registered through the drive