from django.contrib import admin
from .models import Kullanicilar,File,Danisman,Juri,Anahtar_Kelimeler,Proje_Ozellikleri,Yazar

    # Register your models here.

admin.site.register(Kullanicilar)
admin.site.register(File)
admin.site.register(Danisman)
admin.site.register(Juri)
admin.site.register(Anahtar_Kelimeler)
admin.site.register(Proje_Ozellikleri)
admin.site.register(Yazar)

admin.site.site_title="TEK ADMIN UMUTTUR"

admin.site.site_header="ADMIN PANELI"

admin.site.index_title="Islemler"