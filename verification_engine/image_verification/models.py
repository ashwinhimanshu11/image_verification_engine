from django.db import models
import json
import base64
import numpy as np
class Image_Verification(models.Model):
    image_source = models.URLField()
    meta_data = models.JSONField(null=True)
    date_time = models.DateTimeField(auto_now_add=True)
    image_hash = models.CharField(max_length=255, null=True)
    label= models.CharField(max_length=255,  null=True)
    face_encoding=models.TextField(null=True)

    def set_meta_data(self, face_encoding):
        # Convert face_encoding to list
        face_encoding_list = face_encoding.tolist() if isinstance(face_encoding, np.ndarray) else face_encoding
        self.meta_data = json.dumps(face_encoding_list)

    def get_meta_data(self):
        return json.loads(self.meta_data)
    
    def set_face_encoding(self, encoding):
        self.encoding = base64.b64encode(np.array(encoding)).decode('utf-8')

    def get_face_encoding(self):
         return np.frombuffer(base64.b64decode(self.encoding.encode('utf-8')), dtype=np.float64)
