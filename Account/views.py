from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages

from Account.models import Kullanicilar

# Create your views here.

class Kullanıcı:
    Isım=str
    soyisim=str
def secim(request):
        return render(request,'Anasayfa.html')

def register(request):
    
        if request.method == 'POST':
                firstname=request.POST['first_name']
                lastname=request.POST['last_name']
                password1=request.POST['password1']
                password2=request.POST['password2']
                username=request.POST['username']
                email=request.POST['email']

            #şifreler aynı mı
                if password1!= password2:
                        messages.info(request,'Password Does not Match ! ')
                        return redirect('http://127.0.0.1:8000/register')
        else:
                
                return render(request,'register.html')

        Kullanicilar.objects.create(first_name=firstname,last_name=lastname,password=password1,username=username,email=email)
        messages.info(request,'Succesfully user created ! ')

        return redirect('http://127.0.0.1:8000/register')
