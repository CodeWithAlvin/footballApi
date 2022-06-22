from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("api/<slug>",views.api,name="api"),
    path("",views.home,name="home"),

]
