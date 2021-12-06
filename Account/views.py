from django import http
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages
import tika
from Account.models import Kullanicilar,File
import pdfminer
import pdfminer.high_level

import os



def listele(request):
        userid=request.session["id"]
        return render ( request, "listele.html",{"userid":userid})

import re
def digestResume(resume): #resume is a pdf file (as str)
        text = pdfminer.high_level.extract_text(resume,codec='utf-8',caching =True)
        f = open("test.txt", "w",encoding="utf-8")
        f.write(text)
        f.close()
        txtSatırlarım=[]
        fread = open("test.txt", "r",encoding="utf-8")
        txtSatırlarım=fread.readlines()
        anahtar_kelimeler=[]
        anahtar_kelime_listesi=[]
        keywords=[]
        keywords_listesi=[]
        proje_adi=str
        yazar_ismi=str
        ders_adi=str
        teslimDönemi=str
        danışman_ünvanı=str
        danışmanadı=str
        danışmansoyad=str
        ozetSatirlari=str
        bilgisayar_mühendisliği_sayac=0
        önsöz_ve_tesekkurler_sayac=0
        özet_sayaci=0
        danışman_sayaci=0
        juri_sayaci=0
        
        for i in range(0,len(txtSatırlarım)):
                #print("  " + txtSatırlarım[i] + "  ")
                if txtSatırlarım[i].__contains__("LİSANS TEZİ"):
                        for k in range(i+1,len(txtSatırlarım)): 
                                if re.search('[a-zA-Z]+',txtSatırlarım[k]) :
                                        
                                        for t in range(k+2,len(txtSatırlarım)): 
                                                if re.search('[a-zA-Z]+',txtSatırlarım[t]) :
                                                        
                                                        yazar_ismi=txtSatırlarım[t]
                                                        break
                                        break
                 
                if txtSatırlarım[i].__contains__("BİLGİSAYAR MÜHENDİSLİĞİ BÖLÜMÜ"):
                        bilgisayar_mühendisliği_sayac+=1
                        if bilgisayar_mühendisliği_sayac==2:
                                for k in range(i+1,len(txtSatırlarım)): 
                                        if re.search('[a-zA-Z]+',txtSatırlarım[k]) :
                                                ders_adi=txtSatırlarım[k]
                                                for t in range(k+2,len(txtSatırlarım)): 
                                                        if re.search('[a-zA-Z]+',txtSatırlarım[t]) :
                                                        
                                                                proje_adi=txtSatırlarım[t]
                                                                break
                                                
                                                break
                
                if txtSatırlarım[i].__contains__("ÖNSÖZ VE TEŞEKKÜR"):
                        for k in range(i-1,0,-1): 
                                if re.search('[a-zA-Z]+',txtSatırlarım[k]) :
                                        önsöz_ve_tesekkurler_sayac+=1
                                        if önsöz_ve_tesekkurler_sayac ==1:
                                                
                                                teslimDönemi=tarihtenDöneme(txtSatırlarım[k][25:])
                                                break
                if txtSatırlarım[i].__contains__("ÖZET"):
                        
                        özet_sayaci+=1
                        for k in range(i+1,len(txtSatırlarım)):
                                if re.search('[a-zA-Z]+',txtSatırlarım[k]) :
                                        
                                        if özet_sayaci ==2:
                                                

                                                for t in range(k+1,len(txtSatırlarım)): 
                                                        if  not( txtSatırlarım[t].__contains__("Anahtar  kelimeler") ):
                                                                tempSatir=txtSatırlarım[t]
                                                                tempSatir=tempSatir.replace("\n",'')
                                                                ozetSatirlari=str(ozetSatirlari) + str(tempSatir)
                                                        
                                                        else:
                                                                break
                                                break
                if txtSatırlarım[i].__contains__("Keywords") :
                        for k in range(i,len(txtSatırlarım)):
                                 if re.search('[a-zA-Z]+',txtSatırlarım[k]) :
                                        if(txtSatırlarım[k].__contains__(".")):
                                                                                      
                                                keywords= str(keywords) +  txtSatırlarım[k][:len(txtSatırlarım[k])-3]
                                                break
                                        else :
                                                keywords= str(keywords) +  txtSatırlarım[k]
       
                if txtSatırlarım[i].__contains__("Anahtar  kelimeler:") :
                        for k in range(i,len(txtSatırlarım)):
                                 if re.search('[a-zA-Z]+',txtSatırlarım[k]) :
                                        if(txtSatırlarım[k].__contains__(".")):
                                                anahtar_kelimeler= str(anahtar_kelimeler) +  txtSatırlarım[k][:len(txtSatırlarım[k])-3]
                                                break
                                        else :
                                                anahtar_kelimeler= str(anahtar_kelimeler) +  txtSatırlarım[k]
        
        
                if txtSatırlarım[i].__contains__("Danışman") :
                        danışman_sayaci+=1
                        for k in range(i-1,0,-1):

                                if re.search('[a-zA-Z]+',txtSatırlarım[k]) :
                                        if danışman_sayaci==1:  
                                                danışmanünvanı=txtSatırlarım[k]
                                                break
                if txtSatırlarım[i].__contains__("Danışman") :
                        danışman_sayaci+=1
                        for k in range(i-1,0,-1):
                                if re.search('[a-zA-Z]+',txtSatırlarım[k]) :
                                        if danışman_sayaci==1:  
                                                danışmanünvanı=txtSatırlarım[k]
                                           

                                                break

                if txtSatırlarım[i].__contains__("Jüri Üyesi") :
                        juri_sayaci+=1
                        for k in range(i-1,0,-1):
                                if re.search('[a-zA-Z]+',txtSatırlarım[k]) :
                                        if juri_sayaci==1:  
                                                juri1ünvanı=txtSatırlarım[k]
                                                break
                                                
                                        if juri_sayaci==2:
                                                juri2ünvanı=txtSatırlarım[k]
                                                break


        
        
        
        
        
        
        #ANAHATAR 
        for anahtarlar in anahtar_kelimeler[21:].split(","):
                y=anahtarlar[2:]
                y=y.replace("\n","")
                anahtar_kelime_listesi.append(y)
        
        #Keywords
        for keyworddds in keywords[11:].split(","):
                x=keyworddds[2:]
                x=x.replace("\n","")
                keywords_listesi.append(x)
        
        #DANIŞMAN
        

        if not  danışmanünvanı.__contains__("Üyesi"):
                danışmanünvanı,danışmanisim=danışmanünvanı.split(" ",1) # danışman ünvanı aldındı.
                ad=danışmanisim.rsplit(" ",1)  # \n yok edildi.
                danışmanadı,danışmansoyad=ad[0].rsplit(" ",1) # soy isimle diğer isimler ayrıldı    
        else:
                danışmanünvanı,danışmanünvanı2,danışmanünvanı3,danışmanisim=danışmanünvanı.split(" ",3) # danışman ünvanı aldındı.
                ad=danışmanisim.rsplit(" ",1)  # \n yok edildi.
                danışmanadı,danışmansoyad=ad[0].rsplit(" ",1) # soy isimle diğer isimler ayrıldı    
                danışmanünvanı=danışmanünvanı+danışmanünvanı2+danışmanünvanı3


        #JURI 1
        juriisim=str
        juriad=str
        jurisoyad=str
        if not  juri1ünvanı.__contains__("Üyesi"):
                juri1ünvanı,juriisim=juri1ünvanı.split(" ",1) # danışman ünvanı aldındı.
                juriad=juriisim.rsplit(" ",1)  # \n yok edildi.
                juriad,jurisoyad=juriad[0].rsplit(" ",1) # soy isimle diğer isimler ayrıldı    
        else:
                juri1ünvanı,juriünvanı2,juriünvanı3,juriisim=juri1ünvanı.split(" ",3) # danışman ünvanı aldındı.
                ad=juriisim.rsplit(" ",1)  # \n yok edildi.
                juriad,jurisoyad=ad[0].rsplit(" ",1) # soy isimle diğer isimler ayrıldı    
                juri1ünvanı=juri1ünvanı+juriünvanı2+juriünvanı3



        # JURI 2 
        juri2isim=str
        juri2ad=str
        juri2soyad=str
        if not  juri2ünvanı.__contains__("Üyesi"):
                juri2ünvanı,juri2isim=juri2ünvanı.split(" ",1) # danışman ünvanı aldındı.
                juri2ad=juri2isim.rsplit(" ",1)  # \n yok edildi.
                juri2ad,juri2soyad=juri2ad[0].rsplit(" ",1) # soy isimle diğer isimler ayrıldı    
        else:
                juri2ünvanı,juri2ünvanı2,juri2ünvanı3,juri2isim=juri2ünvanı.split(" ",3) # danışman ünvanı aldındı.
                ad=juri2isim.rsplit(" ",1)  # \n yok edildi.
                juri2ad,juri2soyad=ad[0].rsplit(" ",1) # soy isimle diğer isimler ayrıldı    
                juri2ünvanı=juri2ünvanı+juri2ünvanı2+juri2ünvanı3
        print(danışmanünvanı)
        print(danışmanadı)
        print(danışmansoyad)
        print("++++++++++++")
        print(juri1ünvanı)
        print(juriad)
        print(jurisoyad)
        print("++++++++++++")
        print(juri2ünvanı)
        print(juri2ad)
        print(juri2soyad)


            
        
       
def tarihtenDöneme(cümle):
        ay=cümle[3:5]
        yil=cümle[6:10]

        if int(ay) <9:
                #İlkbahar
                cümle="İlkbahar Dönemi" + str(yil) + " -- " + str(int(yil)+1)
        else:
                cümle="Sonbahar Dönemi" + str(int(yil)-1) + " -- " + str(yil)
        return cümle
        
        




# Create your views here.
def content(request):
        userid=None
        try:
                
               userid=request.session["id"]
        except:
                print("GERI AL GERI AL")  

        file=request.FILES.get('FOX',"")
        if file!="" and  id:    
                
                #digestResume(file)
                
                newFileID= File.objects.create(file=file,userid=userid).id
                
                newFile=File.objects.filter(id=newFileID)[0]
                print(newFile.file.name)
                digestResume(newFile.file.name)
               
                

        return render(request,"kullaniciEkrani.html")
        
def secim(request):
        return render(request,'Anasayfa.html')


def register(request):
        if request.method == 'POST':
                        firstname=request.POST.get('first_name',False)
                        lastname=request.POST.get('last_name',False)
                        password1=request.POST.get('password1',False)
                        password2=request.POST.get('password2',False)
                        username=request.POST.get('username',False)
                        email=request.POST.get('email',False)
                        #KULLANICI GİRİŞ YAPMAK İSİTOYRUSE
                        if firstname==False and lastname== False and password1== False and username==False and email==False:
                                username=request.POST['loginusername']
                                password=request.POST['loginpassword']
                                if Kullanicilar.objects.filter(username=username,password=password):
                                        id=Kullanicilar.objects.get(username=username).id
                                        request.session['id']=id
                                        return redirect("http://127.0.0.1:8000/content/?id="+str(id))
                        #şifreler aynı mı
                        else:
                                if password1!= password2:
                                        messages.info(request,'Password Does not Match ! ')
                                        return redirect('http://127.0.0.1:8000/register')
                        
                                if Kullanicilar.objects.filter(username=username):
                                        print(username  )
                                        messages.info(request,'Username Already Has Taken ! ')
                                        return redirect('http://127.0.0.1:8000/register')

                                Kullanicilar.objects.create(first_name=firstname,last_name=lastname,password=password1,username=username,email=email)
                                messages.info(request,'Succesfully user created ! ')
                                return redirect('http://127.0.0.1:8000/register')       
        return render(request,'register.html')

                