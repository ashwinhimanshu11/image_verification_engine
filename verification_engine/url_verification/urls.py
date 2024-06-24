# url_verification/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('verify_url/', views.verify_url, name='verify_url'),
    path('', views.verify_url, name='verify_url'),
]
