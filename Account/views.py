import re
from typing import Union
from django import http
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages
import tika
from Account.models import Kullanicilar, File, Danisman, Yazar, Proje_Ozellikleri, Juri, Anahtar_Kelimeler
import pdfminer
import pdfminer.high_level

import os

from string import printable


def adminsorgu(request):
        context = None

        posts=[]
        tum_kullanicilarin_fileID_listesi=[]
        if request.method == 'POST':
                yazar_ismi = request.POST.get("yazar_isim", "")
                yazar_soyismi = request.POST.get("yazar_soyad", "")
                yazar_no = request.POST.get("yazar_numarasi", "")
                yazar_ogretim_turu = request.POST.get("yazar_ogretim_turu", "")
                teslim_tarihi = request.POST.get("teslim_donemi", "")
                ders_adi = request.POST.get("ders_adi", "")

                proje_basligi = request.POST.get("proje_basligi", "")
                ozet = request.POST.get("ozet", "")
                anahtar_kelime = request.POST.get("anahatar_kelimeler", "")
                

                
                
                
                user_ismi = request.POST.get("user_first_name", "")
                user_soyismi = request.POST.get("user_last_name", "")
                user_email = request.POST.get("user-email", "")
                user_username = request.POST.get("username", "")
                user_password = request.POST.get("password", "")
   

        
                Kullanicilar_listesi=Kullanicilar.objects.all()
                if user_username != "":
                        Kullanicilar_listesi=Kullanicilar_listesi.filter(username=user_username)
                if user_ismi != "":
                        Kullanicilar_listesi=Kullanicilar_listesi.filter(first_name=user_ismi)
                if user_soyismi != "":
                        Kullanicilar_listesi=Kullanicilar_listesi.filter(last_name=user_soyismi)
                if user_email != "":
                        Kullanicilar_listesi=Kullanicilar_listesi.filter(email=user_email)
                if user_password != "":
                        Kullanicilar_listesi=Kullanicilar_listesi.filter(password=user_password)
            
                
                for kullanici in Kullanicilar_listesi:
                        
                        userid=kullanici.id  
                        for eleman in  sorgulama_yapcam_ben(userid, yazar_ismi, yazar_soyismi, yazar_no, yazar_ogretim_turu, teslim_tarihi, ders_adi, proje_basligi, ozet, anahtar_kelime):
                                #print("Eleman " + str(eleman))
                                tum_kullanicilarin_fileID_listesi.append(eleman)        
                #GOSTERILCEK FILE IDLER
                sorgulanan_kullanici_isim=[]
                sorgulanan_kullanici_soyisim=[]
                sorgulanan_kullanici_username=[]
                sorgulanan_kullanici_password=[]
                sorgulanan_kullanici_email=[]
                
                
                sorgulanan_yazar_isim_list = []
                sorgulanan_yazar_soyisim_list = []
                sorgulanan_yazar_no_list = []
                sorgulanan_yazar_ogretim_turu = []
                sorgulanan_ders_adi_list = []
                sorgulanan_proje_baslik_list = []
                sorgulanan_teslim_dönemi_list = []
                sorgulanan_ozet_list = []
                sorgulanan_danisman_isim_list = []
                sorgulanan_danisman_soyisim_list = []
                sorgulanan_danisman_unvan_list = []
                sorgulanan_juri_isim_list = []
                sorgulanan_juri_soyisim_list = []
                sorgulanan_juri_unvan_list = []
                sorgulanan_anahtar_kelimeler_list = []
                sorgulalan_file_path_list=[]
                
                for file_id in tum_kullanicilarin_fileID_listesi:
                        sorgulalan_file_path_list.append(File.objects.get(id=file_id).file)
                        
                       
                        for yazar in Yazar.objects.filter(file_id=file_id):
                                sorgulanan_yazar_isim_list.append(yazar.first_name)
                                sorgulanan_yazar_soyisim_list.append(yazar.last_name)
                                sorgulanan_yazar_ogretim_turu.append(yazar.ogretim_turu)
                                sorgulanan_yazar_no_list.append(yazar.ogrenci_numarasi)

                        for ayar in Proje_Ozellikleri.objects.filter(file_id=file_id):
                                sorgulanan_ders_adi_list.append(ayar.ders_adi)
                                sorgulanan_proje_baslik_list.append(ayar.proje_basligi)
                                sorgulanan_ozet_list.append(ayar.özet)
                                sorgulanan_teslim_dönemi_list.append(ayar.teslim_dönemi)

                        for danisman in Danisman.objects.filter(file_id=file_id):
                                sorgulanan_danisman_isim_list.append(danisman.first_name)
                                sorgulanan_danisman_soyisim_list.append(danisman.last_name)
                                sorgulanan_danisman_unvan_list.append(danisman.unvan)

                        temp_juri_ad = []
                        temp_juri_soyad = []
                        temp_juri_unvan = []
                        for juri in Juri.objects.filter(file_id=file_id):
                                temp_juri_ad.append(juri.first_name)
                                temp_juri_soyad.append(juri.last_name)
                                temp_juri_unvan.append(juri.unvan)
                        sorgulanan_juri_isim_list.append(temp_juri_ad)
                        sorgulanan_juri_soyisim_list.append(temp_juri_soyad)
                        sorgulanan_juri_unvan_list.append(temp_juri_unvan)

                        temp_anahtar_kelime_list = []
                        for anahtar_kelime in Anahtar_Kelimeler.objects.filter(file_id=file_id):
                                temp_anahtar_kelime_list.append(anahtar_kelime.anahtar_kelime)
                        sorgulanan_anahtar_kelimeler_list.append(temp_anahtar_kelime_list)
                        
                        #KULLANICILAR
                        userid=File.objects.filter(id=file_id)[0].userid
                        sorgulalan_kullanici=Kullanicilar.objects.filter(id=userid)[0]   
                        
                        sorgulanan_kullanici_isim.append(sorgulalan_kullanici.first_name)
                        sorgulanan_kullanici_soyisim.append(sorgulalan_kullanici.last_name)     
                        sorgulanan_kullanici_email.append(sorgulalan_kullanici.email)     
                        sorgulanan_kullanici_password.append(sorgulalan_kullanici.password)     
                        sorgulanan_kullanici_username.append(sorgulalan_kullanici.username)
                for count, value in enumerate(tum_kullanicilarin_fileID_listesi):
                        post = {
                                'file_path_list': sorgulalan_file_path_list[count],
                                'yazar_isim_list': sorgulanan_yazar_isim_list[count],
                                'yazar_soy_isim_list': sorgulanan_yazar_soyisim_list[count],
                                'yazar_no_list': sorgulanan_yazar_no_list[count],
                                'yazar_ogretim_turu_list': sorgulanan_yazar_ogretim_turu[count],
                                'ders_adi_list': sorgulanan_ders_adi_list[count],
                                'proje_baslik_list': sorgulanan_proje_baslik_list[count],
                                'teslim_donem_list': sorgulanan_teslim_dönemi_list[count],
                                'ozet_list': sorgulanan_ozet_list[count],
                                'danisman_isim_list': sorgulanan_danisman_isim_list[count],
                                'danisman_soyisim_list': sorgulanan_danisman_soyisim_list[count],
                                'danisman_unvan_list': sorgulanan_danisman_unvan_list[count],
                                'anahtar_kelimeler_list': sorgulanan_anahtar_kelimeler_list[count],
                                'juri_isim_list': sorgulanan_juri_isim_list[count],
                                'juri_soyisim_list': sorgulanan_juri_soyisim_list[count],
                                'juri_unvan_list': sorgulanan_juri_unvan_list[count],
                                'kullanici_ad_list': sorgulanan_kullanici_isim[count],
                                'kullanici_soyad_list': sorgulanan_kullanici_soyisim[count],
                                'kullanici_username_list': sorgulanan_kullanici_username[count],
                                'kullanici_password_list': sorgulanan_kullanici_password[count],
                                'kullanici_email_list': sorgulanan_kullanici_email[count],
                        }
                        posts.append(post)
                        
                context = {
                "posts": posts
                }
                
        return render(request,"adminsorgu.html",context=context)
def change_my_info(request):
    userid = request.session["id"]
    new_user_name = request.POST.get("new_user_name", False)
    new_password = request.POST.get("new_password", False)
    new_email = request.POST.get("new_email", False)
    currentUser = Kullanicilar.objects.filter(id=userid)
    isim = currentUser[0].first_name
    soyisim = currentUser[0].last_name
    if not Kullanicilar.objects.filter(username=new_user_name):
        if new_email:
            currentUser.update(email=new_email)
        if new_user_name:
            currentUser.update(username=new_user_name)
        if new_password:
            currentUser.update(password=new_password)

    else:
        messages.info(request, 'Username Already Taken ! ')

    return render(request, "bilgilerUpdate.html", {
        "isim": isim,
        "soyisim": soyisim
    })


def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3


def yazara_gore_sorgula(files, yazar_ismi, yazar_soyismi, yazar_no):
    if(yazar_ismi != False):
        queryfileid = Yazar.objects.filter(first_name=yazar_ismi).fileid
        files.filter(fileid=queryfileid)
    return files


def getUserFiles(userid):
    return File.objects.filter(userid=userid)


def sorgulama_yapcam_ben(userid, yazar_ismi, yazar_soyismi, yazar_no, yazar_ogretim_turu, teslim_tarihi, ders_adi, proje_basligi, ozet, anahtar_kelime):
    files = getUserFiles(userid)
    file_id_list = []
    for file in files:
        file_id_list.append(file.id)
    if yazar_ismi != "":
        yazarlar = Yazar.objects.filter(first_name=yazar_ismi)
        yazardan_file_id_list = []
        for yazar in yazarlar:
            yazardan_file_id_list.append(yazar.file_id)
        file_id_list = intersection(file_id_list, yazardan_file_id_list)
    if yazar_soyismi != "":
        yazarlar = Yazar.objects.filter(last_name=yazar_soyismi)
        yazardan_file_id_list = []
        for yazar in yazarlar:
            yazardan_file_id_list.append(yazar.file_id)
        file_id_list = intersection(file_id_list, yazardan_file_id_list)
    if yazar_no != "":
        yazarlar = Yazar.objects.filter(ogrenci_numarasi=yazar_no)
        yazardan_file_id_list = []
        for yazar in yazarlar:
            yazardan_file_id_list.append(yazar.file_id)
        file_id_list = intersection(file_id_list, yazardan_file_id_list)
    if yazar_ogretim_turu != "":
        yazarlar = Yazar.objects.filter(ogretim_turu=yazar_ogretim_turu)
        yazardan_file_id_list = []
        for yazar in yazarlar:
            yazardan_file_id_list.append(yazar.file_id)
        file_id_list = intersection(file_id_list, yazardan_file_id_list)
    if ozet != "":
        proje_ayarlari = Proje_Ozellikleri.objects.filter(özet=ozet)
        proje_ayarindan_file_id_list = []
        for proje_ayari in proje_ayarlari:
            proje_ayarindan_file_id_list.append(proje_ayari.file_id)
        file_id_list = intersection(file_id_list, proje_ayarindan_file_id_list)

    if ders_adi != "":
        proje_ayarlari = Proje_Ozellikleri.objects.filter(ders_adi=ders_adi)
        proje_ayarindan_file_id_list = []
        for proje_ayari in proje_ayarlari:
            proje_ayarindan_file_id_list.append(proje_ayari.file_id)
        file_id_list = intersection(file_id_list, proje_ayarindan_file_id_list)

    if proje_basligi != "":
        proje_ayarlari = Proje_Ozellikleri.objects.filter(
            proje_basligi=proje_basligi)
        proje_ayarindan_file_id_list = []
        for proje_ayari in proje_ayarlari:
            proje_ayarindan_file_id_list.append(proje_ayari.file_id)
        file_id_list = intersection(file_id_list, proje_ayarindan_file_id_list)

    if teslim_tarihi != "":

        proje_ayarlari = Proje_Ozellikleri.objects.filter(
            teslim_dönemi=teslim_tarihi)
        proje_ayarindan_file_id_list = []
        for proje_ayari in proje_ayarlari:
            proje_ayarindan_file_id_list.append(proje_ayari.file_id)
        file_id_list = intersection(file_id_list, proje_ayarindan_file_id_list)
    if anahtar_kelime != "":
        nelergeldi = anahtar_kelime.split(",")
        proje_ayarindan_file_id_list = []
        for negeldi in nelergeldi:
            proje_ayarlari = Anahtar_Kelimeler.objects.filter(
                anahtar_kelime=negeldi)

            for proje_ayari in proje_ayarlari:
                proje_ayarindan_file_id_list.append(proje_ayari.file_id)
        file_id_list = intersection(file_id_list, proje_ayarindan_file_id_list)

    return file_id_list


def verileri_al_ve_Sorgula(request, userid):
    if request.method == 'POST':
        yazar_ismi = request.POST.get("yazar_isim", "")
        yazar_soyismi = request.POST.get("yazar_soyad", "")
        yazar_no = request.POST.get("yazar_numarasi", "")
        yazar_ogretim_turu = request.POST.get("yazar_ogretim_turu", "")
        teslim_tarihi = request.POST.get("teslim_donemi", "")
        ders_adi = request.POST.get("ders_adi", "")

        proje_basligi = request.POST.get("proje_basligi", "")
        ozet = request.POST.get("ozet", "")
        anahtar_kelime = request.POST.get("anahatar_kelimeler", "")
       
        files_id_list = sorgulama_yapcam_ben(userid, yazar_ismi, yazar_soyismi, yazar_no,
                                             yazar_ogretim_turu, teslim_tarihi, ders_adi, proje_basligi, ozet, anahtar_kelime)
 
        return files_id_list


def listele(request):
    userid = request.session["id"]
    file_id_list = verileri_al_ve_Sorgula(request, userid)
    sorgulanan_yazar_isim_list = []
    sorgulanan_yazar_soyisim_list = []
    sorgulanan_yazar_no_list = []
    sorgulanan_yazar_ogretim_turu = []
    sorgulanan_ders_adi_list = []
    sorgulanan_proje_baslik_list = []
    sorgulanan_teslim_dönemi_list = []
    sorgulanan_ozet_list = []
    sorgulanan_danisman_isim_list = []
    sorgulanan_danisman_soyisim_list = []
    sorgulanan_danisman_unvan_list = []
    sorgulanan_juri_isim_list = []
    sorgulanan_juri_soyisim_list = []
    sorgulanan_juri_unvan_list = []
    sorgulanan_anahtar_kelimeler_list = []
    sorgulalan_file_path_list=[]
    context = None
    if request.method == "POST":
        posts = []
        for file_id in file_id_list:
            sorgulalan_file_path_list.append(File.objects.get(id=file_id).file)
            for yazar in Yazar.objects.filter(file_id=file_id):
                sorgulanan_yazar_isim_list.append(yazar.first_name)
                sorgulanan_yazar_soyisim_list.append(yazar.last_name)
                sorgulanan_yazar_ogretim_turu.append(yazar.ogretim_turu)
                sorgulanan_yazar_no_list.append(yazar.ogrenci_numarasi)

            for ayar in Proje_Ozellikleri.objects.filter(file_id=file_id):
                sorgulanan_ders_adi_list.append(ayar.ders_adi)
                sorgulanan_proje_baslik_list.append(ayar.proje_basligi)
                sorgulanan_ozet_list.append(ayar.özet)
                sorgulanan_teslim_dönemi_list.append(ayar.teslim_dönemi)

            for danisman in Danisman.objects.filter(file_id=file_id):
                sorgulanan_danisman_isim_list.append(danisman.first_name)
                sorgulanan_danisman_soyisim_list.append(danisman.last_name)
                sorgulanan_danisman_unvan_list.append(danisman.unvan)

            temp_juri_ad = []
            temp_juri_soyad = []
            temp_juri_unvan = []
            for juri in Juri.objects.filter(file_id=file_id):
                temp_juri_ad.append(juri.first_name)
                temp_juri_soyad.append(juri.last_name)
                temp_juri_unvan.append(juri.unvan)
            sorgulanan_juri_isim_list.append(temp_juri_ad)
            sorgulanan_juri_soyisim_list.append(temp_juri_soyad)
            sorgulanan_juri_unvan_list.append(temp_juri_unvan)

            temp_anahtar_kelime_list = []
            for anahtar_kelime in Anahtar_Kelimeler.objects.filter(file_id=file_id):
                temp_anahtar_kelime_list.append(anahtar_kelime.anahtar_kelime)
            sorgulanan_anahtar_kelimeler_list.append(temp_anahtar_kelime_list)
            context = {
                'file_path_list':sorgulalan_file_path_list,
                'yazar_isim_list': sorgulanan_yazar_isim_list,
                'yazar_soy_isim_list': sorgulanan_yazar_soyisim_list,
                'yazar_no_list': sorgulanan_yazar_no_list,
                'yazar_ogretim_turu_list': sorgulanan_yazar_ogretim_turu,
                'ders_adi_list': sorgulanan_ders_adi_list,
                'proje_baslik_list': sorgulanan_proje_baslik_list,
                'teslim_donem_list': sorgulanan_teslim_dönemi_list,
                'ozet_list': sorgulanan_ozet_list,
                'danisman_isim_list': sorgulanan_danisman_isim_list,
                'danisman_soyisim_list': sorgulanan_danisman_soyisim_list,
                'danisman_unvan_list': sorgulanan_danisman_unvan_list,
                'anahtar_kelimeler_list': sorgulanan_anahtar_kelimeler_list,
                'juri_isim_list': sorgulanan_juri_isim_list,
                'juri_soyisim_list': sorgulanan_juri_soyisim_list,
                'juri_unvan_list': sorgulanan_juri_unvan_list,
            }

        for count, value in enumerate(file_id_list):
            post = {
                'file_path_list':sorgulalan_file_path_list[count],
                'yazar_isim_list': sorgulanan_yazar_isim_list[count],
                'yazar_soy_isim_list': sorgulanan_yazar_soyisim_list[count],
                'yazar_no_list': sorgulanan_yazar_no_list[count],
                'yazar_ogretim_turu_list': sorgulanan_yazar_ogretim_turu[count],
                'ders_adi_list': sorgulanan_ders_adi_list[count],
                'proje_baslik_list': sorgulanan_proje_baslik_list[count],
                'teslim_donem_list': sorgulanan_teslim_dönemi_list[count],
                'ozet_list': sorgulanan_ozet_list[count],
                'danisman_isim_list': sorgulanan_danisman_isim_list[count],
                'danisman_soyisim_list': sorgulanan_danisman_soyisim_list[count],
                'danisman_unvan_list': sorgulanan_danisman_unvan_list[count],
                'anahtar_kelimeler_list': sorgulanan_anahtar_kelimeler_list[count],
                'juri_isim_list': sorgulanan_juri_isim_list[count],
                'juri_soyisim_list': sorgulanan_juri_soyisim_list[count],
                'juri_unvan_list': sorgulanan_juri_unvan_list[count],
            }
            posts.append(post)
        context = {
            "posts": posts
        }
        print(sorgulanan_yazar_isim_list)

        # COK ONEMLI  JURI VE ANAHTAR KELIMELER  IC ICE  2D LİSTELER TEKRAR FOR AÇMALISIN HTML DE
        return render(request, "listele.html", context=context)
    return render(request, "listele.html")


def digestResume(resume, fileid):  # resume is a pdf file (as str)
    text = pdfminer.high_level.extract_text(
        resume, codec='utf-8', caching=True)
    f = open("test.txt", "w",encoding="utf-8")
    f.write(text)
    f.close()
    txtSatırlarım = []
    aldimknk = str
    fread = open("test.txt", "r", encoding="utf-8")
    txtSatırlarım = fread.readlines()
    anahtar_kelimeler = []
    anahtar_kelime_listesi = []
    keywords = []
    keywords_listesi = []
    proje_adi = str
    yazar_ismi = str
    ders_adi = str
    teslimDönemi = str
    danışman_ünvanı = str
    danışmanadı = str
    danışmansoyad = str
    ozetSatirlari = str
    bilgisayar_mühendisliği_sayac = 0
    önsöz_ve_tesekkurler_sayac = 0
    özet_sayaci = 0
    danışman_sayaci = 0
    juri_sayaci = 0
    gökselinsayac = 0
    ogrecinno = str
    ogretimTuru = str
    for i in range(0, len(txtSatırlarım)):
        if txtSatırlarım[i].__contains__("LİSANS TEZİ"):
            for k in range(i+1, len(txtSatırlarım)):
                if re.search('[a-zA-Z]+', txtSatırlarım[k]):

                    for t in range(k+2, len(txtSatırlarım)):
                        if re.search('[a-zA-Z]+', txtSatırlarım[t]):

                            yazar_ismi = txtSatırlarım[t]
                            break
                    break

        if txtSatırlarım[i].__contains__("BİLGİSAYAR MÜHENDİSLİĞİ BÖLÜMÜ"):
            bilgisayar_mühendisliği_sayac += 1
            if bilgisayar_mühendisliği_sayac == 2:
                for k in range(i+1, len(txtSatırlarım)):
                    if re.search('[a-zA-Z]+', txtSatırlarım[k]):
                        ders_adi = txtSatırlarım[k]
                        for t in range(k+2, len(txtSatırlarım)):
                            if re.search('[a-zA-Z]+', txtSatırlarım[t]):

                                proje_adi = txtSatırlarım[t]
                                break

                        break

        if txtSatırlarım[i].__contains__("ÖNSÖZ VE TEŞEKKÜR"):
            for k in range(i-1, 0, -1):
                if re.search('[a-zA-Z]+', txtSatırlarım[k]):
                    önsöz_ve_tesekkurler_sayac += 1
                    if önsöz_ve_tesekkurler_sayac == 1:

                        teslimDönemi = tarihtenDöneme(txtSatırlarım[k][25:])
                        break
        if txtSatırlarım[i].__contains__("ÖZET"):

            özet_sayaci += 1
            for k in range(i+1, len(txtSatırlarım)):
                if re.search('[a-zA-Z]+', txtSatırlarım[k]):

                    if özet_sayaci == 2:

                        for t in range(k, len(txtSatırlarım)):
                            if not(txtSatırlarım[t].__contains__("Anahtar  kelimeler")):
                                tempSatir = txtSatırlarım[t]
                                tempSatir = tempSatir.replace("\n", '')
                                ozetSatirlari = str(
                                    ozetSatirlari) + str(tempSatir)

                            else:
                                break
                        break
        if txtSatırlarım[i].__contains__("Keywords"):
            for k in range(i, len(txtSatırlarım)):
                if re.search('[a-zA-Z]+', txtSatırlarım[k]):
                    if(txtSatırlarım[k].__contains__(".")):

                        keywords = str(keywords) + \
                            txtSatırlarım[k][:len(txtSatırlarım[k])-3]
                        break
                    else:
                        keywords = str(keywords) + txtSatırlarım[k]

        if txtSatırlarım[i].__contains__("Anahtar  kelimeler:"):
            for k in range(i, len(txtSatırlarım)):
                if re.search('[a-zA-Z]+', txtSatırlarım[k]):
                    if(txtSatırlarım[k].__contains__(".")):
                        anahtar_kelimeler = str(
                            anahtar_kelimeler) + txtSatırlarım[k][:len(txtSatırlarım[k])-3]
                        break
                    else:
                        anahtar_kelimeler = str(
                            anahtar_kelimeler) + txtSatırlarım[k]

        if txtSatırlarım[i].__contains__("Danışman"):
            danışman_sayaci += 1
            for k in range(i-1, 0, -1):

                if re.search('[a-zA-Z]+', txtSatırlarım[k]):
                    if danışman_sayaci == 1:
                        danışmanünvanı = txtSatırlarım[k]
                        break
        if txtSatırlarım[i].__contains__("Danışman"):
            danışman_sayaci += 1
            for k in range(i-1, 0, -1):
                if re.search('[a-zA-Z]+', txtSatırlarım[k]):
                    if danışman_sayaci == 1:
                        danışmanünvanı = txtSatırlarım[k]

                        break

        if txtSatırlarım[i].__contains__("Jüri Üyesi"):
            juri_sayaci += 1
            for k in range(i-1, 0, -1):
                if re.search('[a-zA-Z]+', txtSatırlarım[k]):
                    if juri_sayaci == 1:
                        juri1ünvanı = txtSatırlarım[k]
                        break

                    if juri_sayaci == 2:
                        juri2ünvanı = txtSatırlarım[k]
                        break
        if txtSatırlarım[i].__contains__("Öğrenci No:"):
            gökselinsayac += 1

            for k in range(i + 1, len(txtSatırlarım)):
                if re.search('[a-zA-Z]+', txtSatırlarım[k]):
                    content = txtSatırlarım[k][11:]
                    content = content.lower()
                    tempyazarismi = yazar_ismi[:-2]

                    tempyazarismi = tempyazarismi.lower()
      

                    if(gökselinsayac == 1):
                        for key in tempyazarismi:
                            if not (key == "ç" or key == "ğ" or key == "ö" or key == "ü" or key == "ş" or key == "ı"):

                                if not set(key).difference(printable):
                                    aldimknk = str(aldimknk) + str(key)
                            else:
                                aldimknk = str(aldimknk) + str(key)
                    tempyazarismi = aldimknk

                    tempyazarismi = str(str(aldimknk)[13:])

                  
                    if content.__contains__(tempyazarismi):
                        xxxxxx = txtSatırlarım[i][12:]
                        ogrecinno = xxxxxx[:9]
                        if int(ogrecinno[5]) == 1:
                            ogretimTuru = "1.Ogretim"

                        else:
                            ogretimTuru = "2.Ogretim"

                    break


    # ANAHATAR
    for anahtarlar in anahtar_kelimeler[21:].split(","):
        y = anahtarlar[2:]
        y = y.replace("\n", "")
        anahtar_kelime_listesi.append(y)

    # Keywords
    for keyworddds in keywords[11:].split(","):
        x = keyworddds[2:]
        x = x.replace("\n", "")
        keywords_listesi.append(x)

    # DANIŞMAN

    if not danışmanünvanı.__contains__("Üyesi"):
        # danışman ünvanı aldındı.
        danışmanünvanı, danışmanisim = danışmanünvanı.split(" ", 1)
        ad = danışmanisim.rsplit(" ", 1)  # \n yok edildi.
        danışmanadı, danışmansoyad = ad[0].rsplit(
            " ", 1)  # soy isimle diğer isimler ayrıldı
    else:
        # danışman ünvanı aldındı.
        danışmanünvanı, danışmanünvanı2, danışmanünvanı3, danışmanisim = danışmanünvanı.split(
            " ", 3)
        ad = danışmanisim.rsplit(" ", 1)  # \n yok edildi.
        danışmanadı, danışmansoyad = ad[0].rsplit(
            " ", 1)  # soy isimle diğer isimler ayrıldı
        danışmanünvanı = danışmanünvanı+danışmanünvanı2+danışmanünvanı3

    # JURI 1
    juriisim = str
    juriad = str
    jurisoyad = str
    if not juri1ünvanı.__contains__("Üyesi"):
        # danışman ünvanı aldındı.
        juri1ünvanı, juriisim = juri1ünvanı.split(" ", 1)
        juriad = juriisim.rsplit(" ", 1)  # \n yok edildi.
        # soy isimle diğer isimler ayrıldı
        juriad, jurisoyad = juriad[0].rsplit(" ", 1)
    else:
        # danışman ünvanı aldındı.
        juri1ünvanı, juriünvanı2, juriünvanı3, juriisim = juri1ünvanı.split(
            " ", 3)
        ad = juriisim.rsplit(" ", 1)  # \n yok edildi.
        # soy isimle diğer isimler ayrıldı
        juriad, jurisoyad = ad[0].rsplit(" ", 1)
        juri1ünvanı = juri1ünvanı+juriünvanı2+juriünvanı3

    # JURI 2
    juri2isim = str
    juri2ad = str
    juri2soyad = str
    if not juri2ünvanı.__contains__("Üyesi"):
        # danışman ünvanı aldındı.
        juri2ünvanı, juri2isim = juri2ünvanı.split(" ", 1)
        juri2ad = juri2isim.rsplit(" ", 1)  # \n yok edildi.
        juri2ad, juri2soyad = juri2ad[0].rsplit(
            " ", 1)  # soy isimle diğer isimler ayrıldı
    else:
        # danışman ünvanı aldındı.
        juri2ünvanı, juri2ünvanı2, juri2ünvanı3, juri2isim = juri2ünvanı.split(
            " ", 3)
        ad = juri2isim.rsplit(" ", 1)  # \n yok edildi.
        # soy isimle diğer isimler ayrıldı
        juri2ad, juri2soyad = ad[0].rsplit(" ", 1)
        juri2ünvanı = juri2ünvanı+juri2ünvanı2+juri2ünvanı3

    # DB ISLEMLERI
    Danisman.objects.create(file_id=fileid, first_name=danışmanadı,
                            last_name=danışmansoyad, unvan=danışmanünvanı)
    Juri.objects.create(file_id=fileid, first_name=juriad,
                        last_name=jurisoyad, unvan=juri1ünvanı)
    Juri.objects.create(file_id=fileid, first_name=juri2ad,
                        last_name=juri2soyad, unvan=juri2ünvanı)
    for kelime in anahtar_kelime_listesi:
        Anahtar_Kelimeler.objects.create(file_id=fileid, anahtar_kelime=kelime)
    for kelime in keywords_listesi:
        Anahtar_Kelimeler.objects.create(file_id=fileid, anahtar_kelime=kelime)

    Proje_Ozellikleri.objects.create(
        file_id=fileid, özet=ozetSatirlari[13:], teslim_dönemi=teslimDönemi, proje_basligi=proje_adi[:-2], ders_adi=ders_adi[:-2])


    Yazar.objects.create(file_id=fileid, first_name=yazar_ismi[:-2].rsplit(" ", 1)[
                         0], last_name=yazar_ismi[:-2].rsplit(" ", 1)[1], ogrenci_numarasi=ogrecinno, ogretim_turu=ogretimTuru)


def tarihtenDöneme(cümle):
    ay = cümle[3:5]
    yil = cümle[6:10]

    if int(ay) < 9:
        # İlkbahar
        cümle = "İlkbahar Dönemi" + str(yil) + " -- " + str(int(yil)+1)
    else:
        cümle = "Sonbahar Dönemi" + str(int(yil)-1) + " -- " + str(yil)
    return cümle


# Create your views here.
def content(request):
    userid = None
    try:

        userid = request.session["id"]
    except:
        print("GERI AL GERI AL")

    file = request.FILES.get('FOX', "")
    if file != "" and id:

        newFileID = File.objects.create(file=file, userid=userid).id
        # digestResume(file,newFileID)

        newFile = File.objects.filter(id=newFileID)[0]
        print(newFile.file.name)
        digestResume(newFile.file.name, newFileID)

    return render(request, "kullaniciEkrani.html")


def secim(request):
    isExited = request.GET.get("exit", False)

    return render(request, 'Anasayfa.html')


def register(request):
    if request.method == 'POST':
        firstname = request.POST.get('first_name', False)
        lastname = request.POST.get('last_name', False)
        password1 = request.POST.get('password1', False)
        password2 = request.POST.get('password2', False)
        username = request.POST.get('username', False)
        email = request.POST.get('email', False)
        # KULLANICI GİRİŞ YAPMAK İSİTOYRUSE
        if firstname == False and lastname == False and password1 == False and username == False and email == False:
            username = request.POST['loginusername']
            password = request.POST['loginpassword']
            if Kullanicilar.objects.filter(username=username, password=password):
                id = Kullanicilar.objects.get(username=username).id
                request.session['id'] = id
                return redirect("http://127.0.0.1:8000/content/?id="+str(id))
        # şifreler aynı mı
        else:
            if password1 != password2:
                messages.info(request, 'Password Does not Match ! ')
                return redirect('http://127.0.0.1:8000/register')

            if Kullanicilar.objects.filter(username=username):
                messages.info(request, 'Username Already Has Taken ! ')
                return redirect('http://127.0.0.1:8000/register')

            Kullanicilar.objects.create(
                first_name=firstname, last_name=lastname, password=password1, username=username, email=email)
            messages.info(request, 'Succesfully user created ! ')
            return redirect('http://127.0.0.1:8000/register')
    return render(request, 'register.html')
