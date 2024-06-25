from django.contrib import admin
from django.urls import path, include
# from ..url_verification.urls import 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('image_verification.urls')),
    path('api/', include('url_verification.urls')),
]
