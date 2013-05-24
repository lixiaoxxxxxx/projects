from django.db import models

# Create your models here.

class Hotel(models.Model):
	name = models.CharField(max_length = 20)
	city = models.CharField(max_length = 20)
	rate = models.IntegerField()
	def __unicode__(self):
		return self.name + " " + self.city + " " + str(self.rate)

class Room(models.Model):
	hotel = models.ForeignKey(Hotel)
	booker = models.CharField(max_length = 20, null= True, blank = True)
	state = models.CharField(max_length = 20)
	price = models.IntegerField()
	start_time = models.DateField(null = True, blank = True)
	end_time = models.DateField(null = True, blank = True)
	def __unicode__(self):
		return self.hotel.name + " " +  self.state + " " + self.booker
