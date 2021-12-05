from django.db import models
from django.db.models.fields import IntegerField
from django.db.models.fields.files import FileField

import random
import os
def generate_unique_name(path):
    def wrapper(instance, filename):
        extension = "." + filename.split('.')[-1]
        filename = str(random.randint(10,99)) + str(random.randint(10,99)) + str(random.randint(10,99)) + str(random.randint(10,99))  + extension
        return os.path.join(path, filename)
    return wrapper

# Create your models here.
class Kullanicilar(models.Model):
    username=models.CharField(max_length=50)
    password=models.CharField(max_length=50)
    email=models.CharField(max_length=50)
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)

class File(models.Model):
    file=FileField(upload_to=generate_unique_name("pics"))
    userid=IntegerField()
    
    
