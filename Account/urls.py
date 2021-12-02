
from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from . import views
urlpatterns = [
    path('register/',views.register,name="register"),
    path('',views.secim),
    path("content/",views.content,name="content"),
    ]
