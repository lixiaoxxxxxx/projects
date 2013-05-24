from django.db import models

# Create your models here.
#class Infomation(models.Model):
	#userid = models.CharField(max_length=20)
	#name = models.CharField(max_length=30)
	#follower_count = models.IntegerField(blank=True, null=True)
	#friend_count = models.IntegerField(blank=True, null=True)
	#mf_rate = models.DecimalField(max_digits=18, decimal_places=16)
	#statuses_count = models.IntegerField(blank=True, null=True)
	#statuses_pic_rate = models.DecimalField(max_digits=20, decimal_places = 17)
	#category = models.IntegerField(blank=True, null=True)
	#comments_count_avg= models.DecimalField(max_digits=20, decimal_places=16, blank=True, null=True)
	#reposts_count_avg = models.DecimalField(max_digits=20, decimal_places=16, blank=True, null=True)
	#client = models.CharField(max_length=30, blank=True, null=True)

class User(models.Model):
	uid = models.CharField(max_length=12)
	name = models.CharField(max_length=40)
	avater = models.CharField(max_length=60)
