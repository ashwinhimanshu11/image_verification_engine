
# verifier/urls.py
from django.urls import path
from .views import ImageVerificationAPIView
from .face_recognition_script import process_image

urlpatterns = [
    path('verify-images/', ImageVerificationAPIView.as_view(), name='image_verification_api'),
]
