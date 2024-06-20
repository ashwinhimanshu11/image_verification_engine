from django.db import models

# Create your models here.
class URLRecord(models.Model):
    url = models.URLField(unique=True)
    date_added = models.DateTimeField(auto_now_add=True)
    source = models.CharField(max_length=255)

    def __str__(self):
        self.url