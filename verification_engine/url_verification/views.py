# url_verification/views.py
from django.shortcuts import render
from django.http import JsonResponse
from .models import URL
from .utils import search_similar_images
from datetime import datetime
import pytz

def get_ist_time(utc_time):
    ist = pytz.timezone('Asia/Kolkata')
    utc_time = utc_time.replace(tzinfo=pytz.utc)
    ist_time = utc_time.astimezone(ist)
    return ist_time.strftime('%B %d, %Y, %I:%M %p')

def verify_url(request):
    if request.method == "POST":
        url = request.POST.get('url')
        source = request.POST.get('source', 'manual')
        try:
            url_obj, created = URL.objects.get_or_create(url=url, defaults={'source': source})
            similar_images = search_similar_images(url)
            
            # Format date_time_added to IST
            date_time_added_ist = get_ist_time(url_obj.date_time_added)
            
            context = {
                'status': 'New' if created else 'Existing',
                'date_time_added': date_time_added_ist,
                'similar_images': similar_images
            }
            return render(request, 'url_verification/verify_url.html', context)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return render(request, 'url_verification/verify_url.html')

