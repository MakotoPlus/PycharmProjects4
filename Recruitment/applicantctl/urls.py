#Recuruitment/applicantctl/urls.py
from django.urls import include, path
from django.conf.urls import url
from . import views
from .views import ItemUpdateView, ItemDeleteView

app_name ='applicantctl'

urlpatterns = [
    # ex: /
    path('', views.index, name='index'),
    path('list', views.index, name='index'),
    path('index', views.index, name='index'),
 
    # ex: /add/
    path('add/', views.add, name='add'),
    #url(r'^create$', T_ApplicantinfoCreateView.as_view()),

    # ex: /add/judgment/1/
    path('add/judgment/<int:pk>/', views.add_judgment, name='add_judgment'),

    # ex: /upd/judgment/1/
    #path('upd/judgment/<int:pk>/', views.upd_judgment, name='upd_judgment'),

    # ex: /upd/1/
    path('upd/<int:pk>/', views.upd, name='upd'),
 
    # ex: /delete/1/
    path('delete/<int:pk>/', ItemDeleteView.as_view(), name='delete'),
 
    # ex: /judgment/1/
    #path('judgment/<int:pk>/', views.judgment, name='judgment'),
    path('upd/judgment/<int:pk>/', ItemUpdateView.as_view(), name='upd_judgment'),

]
