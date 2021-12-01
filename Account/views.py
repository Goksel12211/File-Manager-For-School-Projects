from django.http.response import HttpResponse
from django.shortcuts import render

# Create your views here.

class Kullanıcı:
    Isım=str
    soyisim=str

def home(request):


 
        kullanıcı1=Kullanıcı()
        kullanıcı1.Isım="goks"
        kullanıcı1.soyisim="umut oyunda 1221"

        return render(request,'index.html',{'göstermelik':kullanıcı1})
