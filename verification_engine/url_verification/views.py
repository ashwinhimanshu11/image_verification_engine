# url_verification/views.py
from django.shortcuts import render
from django.http import JsonResponse
from .models import URL
from .utils import search_similar_images

def verify_url(request):
    if request.method == "POST":
        url = request.POST.get('url')
        source = request.POST.get('source', 'manual')
        try:
            url_obj, created = URL.objects.get_or_create(url=url, defaults={'source': source})
            similar_images = search_similar_images(url)
            context = {
                'status': 'new' if created else 'existing',
                'date_time_added': url_obj.date_time_added,
                'similar_images': similar_images
            }
            return render(request, 'url_verification/verify_url.html', context)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return render(request, 'url_verification/verify_url.html')
