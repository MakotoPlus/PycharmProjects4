#Recuruitment/applicantctl/urls.py
from django.urls import include, path
from django.conf.urls import url
from .views import index, add, add_judgment, upd
from .views.ItemDeleteView import ItemDeleteView
from .views.ItemUpdateView import ItemUpdateView

app_name ='applicantctl'

urlpatterns = [
    # ex: /
    path('', index.index_func, name='index'),
    path('list', index.index_func, name='index'),
    path('index', index.index_func, name='index'),

    # ex: /add/
    path('add/', add.add_func, name='add'),
    #url(r'^create$', T_ApplicantinfoCreateView.as_view()),
    # ex: /add/judgment/1/
    path('add/judgment/<int:pk>/', add_judgment.add_judgment_func, name='add_judgment'),
    # ex: /upd/1/
    path('upd/<int:pk>/', upd.upd_func, name='upd'),
    # ex: /delete/1/
    path('delete/<int:pk>/', ItemDeleteView.as_view(), name='delete'), 
    # ex: /judgment/1/
    path('upd/judgment/<int:pk>/', ItemUpdateView.as_view(), name='upd_judgment'),

]
