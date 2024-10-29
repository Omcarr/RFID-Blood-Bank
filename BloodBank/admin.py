from django.contrib import admin

# Register your models here.
from .models import *

#later add a model for qr linking
admin.site.register(Donor)
admin.site.register(DonationDrive)
admin.site.register(RFIDTag)
