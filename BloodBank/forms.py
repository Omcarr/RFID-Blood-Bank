from django.forms import ModelForm
from .models import Donor,DonationDrive
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']

class DonorForm(ModelForm):
    class Meta:
        model=Donor
        fields='__all__'
        exclude=['unit_status']



class DonationDriveForm(ModelForm):
    class Meta:
        model=DonationDrive
        fields='__all__'