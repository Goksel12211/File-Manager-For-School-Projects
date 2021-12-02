from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages

# Create your views here.

class Kullanıcı:
    Isım=str
    soyisim=str

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
            return redirect('http://127.0.0.1:8000/')

        return render(request,'register.html')

def home(request):


 
        kullanıcı1=Kullanıcı()
        kullanıcı1.Isım="goks"
        kullanıcı1.soyisim="umut oyunda 1221"

        return render(request,'index.html',{'göstermelik':kullanıcı1})
