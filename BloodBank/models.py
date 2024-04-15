from django.db import models

# Create your models here.
class Donor(models.Model):
	Name = models.CharField(max_length=200, null=True)
	Age= models.PositiveIntegerField()
	Bloodgroup=models.CharField(max_length=10)
	Phone = models.CharField(max_length=200, null=True)
	Email = models.CharField(max_length=200, null=True)
	RFID=models.CharField(max_length=20,null=True)

	# profile_pic = models.ImageField(default="default_pfp.png", null=True, blank=True)

	date_created = models.DateTimeField(auto_now_add=True, null=True)
	def __str__(self):
			return self.Name