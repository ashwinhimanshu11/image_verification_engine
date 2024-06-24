# In serializers.py
from rest_framework import serializers
from .models import Image_Verification

class ImageVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image_Verification
        fields = '__all__'

