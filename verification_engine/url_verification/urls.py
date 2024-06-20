from django.urls import path
from .views import verify_url

urlpatterns = [
    path('verify/', verify_url, name='verify_url')
]