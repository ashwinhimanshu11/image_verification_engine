from django.contrib import admin
from django.urls import path
from url_verification.views import verify_url
from .views import ImageVerificationView

urlpatterns = [
    path('verify-url/', verify_url, name='verify-url'),

]
