
from os import name
from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from . import views
urlpatterns = [
    path('register/',views.register,name="register"),
    path('',views.secim),
    path("content/",views.content,name="content"),
    path("content/listele",views.listele,name="listele"),
    path('content/change-my-information',views.change_my_info,name="change-my-info"),
    path('admin-sorgu',views.adminsorgu,name="admin-sorgu"),
    ]
