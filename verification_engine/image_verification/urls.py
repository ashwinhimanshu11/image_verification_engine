
# verifier/urls.py
from django.urls import path
from .views import image_verification
from .face_recognition_script import process_image

urlpatterns = [
    path('verify-images/', image_verification.as_view(), name='image_verification_api'),
]
