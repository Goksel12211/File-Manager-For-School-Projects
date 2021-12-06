from django.contrib import admin
from .models import Kullanicilar,File

    # Register your models here.

admin.site.register(Kullanicilar)
admin.site.register(File)

admin.site.site_title="TEK ADMIN UMUTTUR"

admin.site.site_header="ADMIN PANELI"

admin.site.index_title="Islemler"