#Recuruitment/mytest/urls.py
from django.urls import include, path
from django.conf.urls import url
from . import views

app_name ='mytest'

urlpatterns = [
    # ex: /
    path('', views.index, name='index'),
    path('index', views.index, name='index'),
    # ex: /mail
    path('mail', views.mail, name='mail'),
    # ex: /templatemail
    path('templatemail', views.templatemail, name='templatemail'),
    # ex: /download_excel
    path('download_excel', views.download_excel, name='download_excel'),
]
