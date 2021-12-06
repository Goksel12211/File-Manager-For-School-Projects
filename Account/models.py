from django.db import models
from django.db.models.fields import IntegerField
from django.db.models.fields.files import FileField
import uuid

import random
import os
def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('pics/', filename)

# Create your models here.
class Kullanicilar(models.Model):
    username=models.CharField(max_length=50)
    password=models.CharField(max_length=50)
    email=models.CharField(max_length=50)
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
#
class File(models.Model):
    file=FileField(upload_to=get_file_path)
    userid=IntegerField()

class Danisman(models.Model):
    file_id=IntegerField()
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    unvan=models.CharField(max_length=50)

class Juri(models.Model):
    file_id=IntegerField()
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    unvan=models.CharField(max_length=50)

class Anahtar_Kelimeler(models.Model):
    file_id=IntegerField()
    anahtar_kelime=models.CharField(max_length=50)

class Proje_Ozellikleri(models.Model):
    file_id=IntegerField()
    özet=models.CharField(max_length=50)
    teslim_dönemi=models.CharField(max_length=50)
    proje_basligi=models.CharField(max_length=50)
    ders_adi=models.CharField(max_length=50)

class Yazar(models.Model):
    file_id=IntegerField()
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    ogrenci_numarasi=models.CharField(max_length=50)
    ogretim_turu=models.CharField(max_length=50)


    
    
