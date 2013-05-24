from django.db import models

# Create your models here.

class Cata(models.Model):
	title = models.CharField(max_length = 30)

class Blog(models.Model):
	title = models.CharField(max_length = 30)
	content = models.CharField(max_length = 500)
	date = models.DateField()
	cate = models.ForeignKey(Cata)

