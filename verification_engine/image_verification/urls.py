
# verifier/urls.py
from django.urls import path
from .views import image_verification

urlpatterns = [
    path('verify-imagess/', image_verification, name='image_verification_api'),
]
