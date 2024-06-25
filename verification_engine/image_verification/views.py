from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from PIL import Image
import requests
import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
from io import BytesIO
from .models import Image_Verification
from .face_recognition_script import process_image
from .face_recognition_utility import extract_face_encodings, load_image_from_url
from .serializers import ImageVerificationSerializer

model = hub.load("https://tfhub.dev/google/imagenet/mobilenet_v2_100_224/classification/5")
labels_path = tf.keras.utils.get_file('ImageNetLabels.txt', 'https://storage.googleapis.com/download.tensorflow.org/data/ImageNetLabels.txt')
with open(labels_path, 'r') as f:
    labels = f.read().splitlines()

def preprocess_image(image):
    image = image.resize((224, 224))
    image = np.array(image)
    if image.ndim == 2:
        image = np.stack((image,) * 3, axis=-1)
    elif image.shape[2] == 1:
        image = np.concatenate([image] * 3, axis=-1)
    elif image.shape[2] > 3:
        image = image[:, :, :3]
    image = image.astype(np.float32) / 255.0
    image = np.expand_dims(image, axis=0)
    return image

def classify_image(image):
    processed_image = preprocess_image(image)
    predictions = model(processed_image)
    predicted_index = np.argmax(predictions, axis=-1)[0]
    return labels[predicted_index]

class ImageVerificationAPIView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            image_url = request.data['image_url']
            image = load_image_from_url(image_url)
        except (KeyError, ValueError) as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        face_encodings = extract_face_encodings(image)
        if face_encodings:
            print("face found")
            response_data, status_code = process_image(image_url)
            return Response(response_data, status=status_code)
        else:
            print("no face found")
            try:
                response = requests.get(image_url)
                image = Image.open(BytesIO(response.content))
            except (requests.exceptions.RequestException, OSError) as e:
                return Response({"error": "Unable to fetch image from URL"}, status=status.HTTP_400_BAD_REQUEST)

            label = classify_image(image)
            result = {"image_source": image_url, "label": label}
            image_finder = Image_Verification.objects.filter(label=label)
            if image_finder.exists():
                serializer = ImageVerificationSerializer(image_finder, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            serializer = ImageVerificationSerializer(data=result)
            if not Image_Verification.objects.filter(image_source=image_url):
                if serializer.is_valid():
                    serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
