
from os import name
from django.conf import settings

from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from . import views
from django.conf.urls.static import static
urlpatterns = [
    path('register/',views.register,name="register"),
    path('',views.secim),
    path("content/",views.content,name="content"),
    path("content/listele",views.listele,name="listele"),
    path('content/change-my-information',views.change_my_info,name="change-my-info"),
    path('admin-sorgu',views.adminsorgu,name="admin-sorgu"),
    path('benisil/<int:fileid>/',views.silFromUser,name="sil"),
    path('benisiladmin/<int:fileid>/',views.silFromAdmin),
    
    ]

urlpatterns=urlpatterns + static    (settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
