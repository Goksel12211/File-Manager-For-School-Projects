from django.db import models
from django.db.models.fields import IntegerField
from django.db.models.fields.files import FileField

# Create your models here.
class Kullanicilar(models.Model):
    username=models.CharField(max_length=50)
    password=models.CharField(max_length=50)
    email=models.CharField(max_length=50)
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
class File(models.Model):
    file=FileField(upload_to='pics')
    userid=IntegerField()
 
