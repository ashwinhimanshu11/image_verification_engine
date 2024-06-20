from django.shortcuts import render
from django.http import JsonResponse
from .models import URLRecord
from django.utils import timezone

# Create your views here.

def verify_url(request):
    url = request.GET.get('url')

    if not url:
        return JsonResponse({'error': 'No Url provided'}, status=400)

    try:
        url_entry = URLRecord.objects.get(url=url)

        return JsonResponse({
            'url': url_entry.url,
            'date_added': url_entry.date_added,
            'source': url_entry.source
        })
    except URLRecord.DoesNotExist:
        new_entry = URLRecord(url=url, source='Manual')
        new_entry.save()
        return JsonResponse({
            'message': 'New URL added',
            'url': new_entry.url,
            'date_added': new_entry.date_added,
            'source': new_entry.source
        })