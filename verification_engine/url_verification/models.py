from django.db import models

class URL(models.Model):
    url = models.URLField(unique=True)
    inserted_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.url

