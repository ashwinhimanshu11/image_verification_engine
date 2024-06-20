from rest_framework import serializers
from .models import Image_Verification

class ImageVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image_Verification
        fields = ['image_source', 'meta_data', 'date_time', 'image_hash']
