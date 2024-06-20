from django.db import models
import json

class Image_Verification(models.Model):
    image_source = models.URLField(unique=True)
    meta_data = models.JSONField()
    date_time = models.DateTimeField(auto_now_add=True)
    image_hash = models.CharField(max_length=255, unique=True)

    def set_meta_data(self, encoding):
        self.meta_data = json.dumps(encoding)

    def get_meta_data(self):
        return json.loads(self.meta_data)
