from django.conf.urls import url
from django.contrib import admin
from views import page ,  Create , Update , Delete , List , Detail

urlpatterns = [
    url(r'^home$' , page , name = "home"),
    url(r'^create$' , Create , name = "Create"),
    url(r'^(?P<slug>[\w-]+)/edit$' , Update , name = "Update"),
    url(r'^(?P<slug>[\w-]+)/delete$' , Delete , name = "Delete"),
    url(r'^$' , List , name = "List"),
    url(r'^(?P<slug>[\w-]+)/$' , Detail , name = 'Detail'),
]
