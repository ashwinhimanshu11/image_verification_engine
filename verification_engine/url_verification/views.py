from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import URL
from .serializers import URLSerializer


from rest_framework.views import APIView


@api_view(['POST'])
def verify_url(request):
    url = request.data.get('url')
    if not url:
        return Response({"error": "URL is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        url_instance, created = URL.objects.get_or_create(url=url)
        if created:
            return Response({"message": "New URL inserted", "inserted_at": url_instance.inserted_at}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "URL already exists", "inserted_at": url_instance.inserted_at}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


