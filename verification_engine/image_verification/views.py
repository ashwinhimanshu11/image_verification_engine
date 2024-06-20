from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import requests
from PIL import Image as PILImage
from io import BytesIO
import imagehash
from .models import Image_Verification
from .serializers import ImageVerificationSerializer
from datetime import datetime

@csrf_exempt
def image_verification(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            image_url = data.get('image_url')
            if not image_url:
                return JsonResponse({'error': 'No image URL provided'}, status=400)
            
            # Check if the image URL already exists in the database
            existing_image = Image_Verification.objects.filter(image_source=image_url).first()
            if existing_image:
                # Retrieve similar images based on image hash
                similar_images = Image_Verification.objects.filter(image_hash=existing_image.image_hash)
                similar_image_urls = [img.image_source for img in similar_images]
                return JsonResponse({'similar_image_urls': similar_image_urls}, status=200)
            
            try:
                response = requests.get(image_url)
                if response.status_code == 200:
                    image = PILImage.open(BytesIO(response.content))
                else:
                    return JsonResponse({'error': 'Failed to download image'}, status=response.status_code)
            except Exception as e:
                return JsonResponse({'error': 'Error downloading image: {}'.format(str(e))}, status=500)
            
            # Generate image hash
            image_hash = str(imagehash.phash(image))
            
            # Store the new image and its details
            new_image = Image_Verification(
                image_source=image_url,
                date_time=datetime.now(),
                image_hash=image_hash
            )
            new_image.save()

            return JsonResponse({'success': 'Image saved successfully'}, status=201)
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON payload'}, status=400)
        except Exception as e:
            return JsonResponse({'error': 'Unexpected error: {}'.format(str(e))}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
