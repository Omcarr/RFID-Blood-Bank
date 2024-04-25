from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .decoraters import unauth_user,allowed_user
from django.contrib.auth.models import Group
from .forms import DonorForm,DonationDriveForm,CreateAdminForm
from django.core.mail import send_mail
from django.db.models import Count
from django.db import transaction
from django.http import JsonResponse

from collections import defaultdict


from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Donor
from .serializers import DonorSerializer
import logging

# Create your views here.

# @login_required(login_url='login')
# @allowed_user(allowed_roles=['AdminLvl0'])
def home(request):
#     send_mail(
#     "Thank you for registration",
#     "Here is the message. hviuefvgebnv;oef vjkebvernv e",
#     "dummy.bloodbank1@gmail.com",
#     ["primesussy@gmail.com"],
#     fail_silently=False,
# )
    return render(request,'BloodBank/home.html')

# @login_required(login_url='login')
#@allowed_user(['admin0'])
def AdminHome(request):
    context={}
    return render(request,'BloodBank/adminhome.html',context)


# @unauth_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password =request.POST.get('password')
        #authenticates the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user) #django inbuilt login fucntion
            print('logged in')
            return redirect('home')
        else:
            messages.info(request, 'Username OR password is incorrect')

    context = {}
    return render(request, 'BloodBank/login.html', context)
    

def logoutUser(request):
	logout(request)
	return redirect('login')

# @unauth_user
def Admin_register(request):
    form=CreateAdminForm()
    if request.method=='POST':
        form=CreateAdminForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')

    context={'form':form}
    return render(request,'BloodBank/admin_form.html',context)


# @login_required(login_url='login')
def CreateDrive(request):
    form=DonationDriveForm()
    if request.method == 'POST':
        form = DonationDriveForm(request.POST)
        if form.is_valid():
            venue = form.cleaned_data['Venue']
            
            # Check if a drive with the same venue already exists
            if DonationDrive.objects.filter(Venue=venue).exists():
                form.add_error('Venue', 'Drive at this venue already exists.')
            else:
                with transaction.atomic():
        
                    group, created = Group.objects.get_or_create(name=venue)
                    form.instance.created_by = request.user
                    form.instance.group = group
                    form.save()
                    return redirect('register', group_id=group.id)

    context={'form':form}
    return render(request,'BloodBank/new_drive.html',context)


# @login_required(login_url='login')
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
            # latest_rfid_tag = RFIDTag.objects.latest('id')
            # #rfid_tag = RFIDTag.objects.get_or_create(RFID=rfid_value)[0]  # Retrieve or create the RFIDTag instance
            # donor.RFID = latest_rfid_tag.RFID
            latest_rfid_tag = RFIDTag.objects.latest('id')
            donor.RFID = latest_rfid_tag
            donor.save()
            donor.groups.add(group)  # Associate the donor with the group

            return redirect('register', group_id=group.id)

    context = {'form': form, 'group_id': group_id, 'blood_group_counts': blood_group_counts}
    return render(request, 'BloodBank/register.html', context)


# @login_required(login_url='login')
def admin_dashboard(request):
    drives = DonationDrive.objects.filter(created_by=request.user)[::-1]  #passing in as recent first order
    context = {'drives': drives}
    return render(request,'BloodBank/admin_dashboard.html',context)



# @login_required(login_url='login')
# def drive_details(request, drive_name):
#     drive = Group.objects.get(name=drive_name)
#     group_id = drive.id
#     donor_list=Donor.objects.filter(groups=drive)
#    #print(donor_list)
#     donor_blood_group = Donor.objects.filter(groups=drive).values('Bloodgroup').annotate(count=Count('Bloodgroup'))
#     context = {'drive':drive, 'donors': donor_blood_group,'donor_list':donor_list,'group_id':group_id,'drive_name':drive_name}
#     return render(request, 'BloodBank/drive_dets.html', context)


def drive_details(request, drive_name):
    drive = Group.objects.get(name=drive_name)
    group_id = drive.id
    
    # Filter donors with a status of 'Donated'
    donor_list = Donor.objects.filter(groups=drive, unit_status='Donated')
    
    # Aggregate donor counts by blood group
    donor_blood_group = donor_list.values('Bloodgroup').annotate(count=Count('Bloodgroup'))
    
    context = {
        'drive': drive,
        'donors': donor_blood_group,
        'donor_list': donor_list,
        'group_id': group_id,
        'drive_name': drive_name
    }
    
    return render(request, 'BloodBank/drive_dets.html', context)



logger = logging.getLogger(__name__)

@api_view(['GET', 'POST'])
def rfid_val(request):
    if request.method == 'POST':
        serializer = DonorSerializer(data=request.data)
        if serializer.is_valid():
            rfid_value = request.data.get('RFID', None)
            logger.info(f"Received RFID value: {rfid_value}")
            print(rfid_value)
            rfid_value=str(rfid_value)
            if rfid_value[0]=='1':
                rfid_value=rfid_value[1:]
                rfid_tag = RFIDTag.objects.create(RFID=rfid_value)
            elif rfid_value[0]=='0':
                rfid_value=rfid_value[1:]
                try:
                    donor = Donor.objects.get(RFID__RFID=rfid_value)
                except:
                    print("Donor with RFID value '{}' not found.".format(rfid_value))
                else:
                    donor.unit_status = 'Utilized'
                    donor.save()
                    print("Donor '{}' status updated to 'Utilized'.".format(donor))

            return render(request, 'BloodBank/rfid_val.html', {'rfid_value': rfid_value})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
             # Print the received RFID value
            # Process rfid_value as needed

            # Render the template with the RFID value
        #     return render(request, 'BloodBank/rfid_val.html', {'rfid_value': rfid_value})
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # elif request.method == 'GET':
    #     logger.info("GET request received")
    #     # Handle GET requests (optional)
    #     return Response("GET request received", status=status.HTTP_200_OK)



def main_storage(request):
    donors_moved_to_mother_bank= Donor.objects.filter(unit_status='Transferred to main bank')
    #print(donors_moved_to_mother_bank)
    blood_group_counts = defaultdict(int)
    for donor in donors_moved_to_mother_bank:
        blood_group_counts[donor.Bloodgroup] += 1
    blood_group_counts = dict(blood_group_counts)
    #print(blood_group_counts)

    context = {
        'donors_moved_to_mother_bank': donors_moved_to_mother_bank,
        'blood_group_counts': blood_group_counts
    }
    return render(request, 'BloodBank/main_storage.html', context)



def transfer_to_main(request, drive_name):
    drive = Group.objects.get(name=drive_name)
    donors_to_transfer = Donor.objects.filter(groups=drive, unit_status='Donated')
    
    for donor in donors_to_transfer:
        donor.unit_status = 'Transferred to main bank'
        donor.save()
    
    # Redirect to the main storage page after transferring donors
    return redirect('main_storage')












#to-do
#make a error 404 page with link back to home
#unique drive name fix------------------------------------------------->done
#pie charts on admin dashboard------------------------------------------------->done
#mail to the donor when register for a drive along with an attchment
#add a counter to show many users have been registered through the drive ------->can be done
#push to mainbugton on dashboad ot=r keep in local inv
#superadmin request model: admin dashboard request button to main bank
#main bank accept reject



# @api_view(['GET', 'POST'])
# def rfid_val(request):
#     if request.method == 'POST':
#         serializer = DonorSerializer(data=request.data)
#         if serializer.is_valid():
#             rfid_value = request.data.get('RFID', None)
#             logger.info(f"Received RFID value: {rfid_value}")
#             print(rfid_value)  # Print the received RFID value
#             # Process rfid_value as needed

#             # Render the template with the RFID value
#             return render(request, 'BloodBank/rfid_val.html', {'rfid_value': rfid_value})
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     # elif request.method == 'GET':
#     #     logger.info("GET request received")
#     #     # Handle GET requests (optional)
#     #     return Response("GET request received", status=status.HTTP_200_OK)
