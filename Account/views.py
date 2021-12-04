from django import http
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages
import tika
from Account.models import Kullanicilar,File
import pdfminer
import pdfminer.high_level

import os

def digestResume(resume): #resume is a pdf file (as str)
    text = pdfminer.high_level.extract_text(resume)
    print(text)
    
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
                """ oldFileName=file.name
                
               file.name=str(fileID)+ ".pdf"
                obj.file =file 
                obj.save()
                """
                


                

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

                