# url_verification/models.py
from django.db import models

class URL(models.Model):
    url = models.TextField(unique=True)
    date_time_added = models.DateTimeField(auto_now_add=True)
    source = models.TextField()
