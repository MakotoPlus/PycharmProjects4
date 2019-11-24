#Recuruitment/applicantctl/urls.py
from django.urls import include, path
from . import views


app_name ='accounts'

urlpatterns = [
    # ex: /
    path('signup/', views.SignUpView.as_view(), name='signup'),
]
