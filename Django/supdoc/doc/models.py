from django.db import models

# Create your models here.

class Doc_file(models.Model):
	name = models.CharField(max_length = 20)
	content = models.CharField(max_length = 2000)
	def __unicode__(self):
		return self.name + " " + self.content
