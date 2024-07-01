# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from PIL import Image
# import requests
# import urllib.request
# import tensorflow as tf
# import tensorflow_hub as hub
# import numpy as np
# from io import BytesIO
# import json
# from .models import Image_Verification
# from .face_recognition_script import process_image
# from .face_recognition_utility import extract_face_encodings, load_image_from_url,calculate_image_hash
# from .serializers import ImageVerificationSerializer
# from django.db.models import Q

# # Load the pre-trained model
# model = None
# labels = []

# def load_model():
#     global model, labels
#     model_url = "https://www.kaggle.com/models/google/mobilenet-v2/TensorFlow2/100-224-classification/2"
#     try:
#         model = hub.load(model_url)
#         print("Model loaded successfully.")
#         labels_path = tf.keras.utils.get_file('ImageNetLabels.txt', 'https://storage.googleapis.com/download.tensorflow.org/data/ImageNetLabels.txt')
#         with open(labels_path, 'r') as f:
#             labels = f.read().splitlines()
#     except Exception as e:
#         print(f"Error loading model from {model_url}: {e}")
#         # Additional debugging information
#         import os
#         temp_dir = os.path.join(os.getenv("HOME"), ".keras", "datasets")
#         print(f"Check if the directory {temp_dir} exists and its contents.")
#         if os.path.exists(temp_dir):
#             print("Directory exists. Contents:")
#             print(os.listdir(temp_dir))
#         else:
#             print("Directory does not exist.")

# load_model()

# def preprocess_image(image):
#     image = image.resize((224, 224))
#     image = np.array(image)
#     # Ensure image has 3 color channels (RGB)
#     if image.ndim == 2:
#         image = np.stack((image,) * 3, axis=-1)
#     elif image.shape[2] == 1:
#         image = np.concatenate([image] * 3, axis=-1)
#     elif image.shape[2] > 3:
#         image = image[:, :, :3]
#     image = image.astype(np.float32) / 255.0
#     image = np.expand_dims(image, axis=0)
#     return image

# # def classify_image(image):
# #     if model is None:
# #         raise RuntimeError("Model is not loaded")
# #     processed_image = preprocess_image(image)
# #     predictions = model(processed_image)
# #     predicted_index = np.argmax(predictions, axis=-1)[0]
# #     return labels[predicted_index]

# def classify_image(image, top_k=5):
#     processed_image = preprocess_image(image)
#     predictions = model(processed_image)
#     predictions = np.array(predictions)
#     # Get the top predicted label indices
#     top_k_indices = np.argsort(predictions[0], axis=-1)[::-1][:top_k]
    
#     top_labels = [labels[idx] for idx in top_k_indices]
#     print('this is prediction indices----------------------->',top_labels)
#     return top_labels

# class image_verification(APIView):
#     def post(self, request, *args, **kwargs):
#         image = load_image_from_url(request.data['image_url'])
#         face_encodings = extract_face_encodings(image)
#         if face_encodings:
#             print("Face found")
#             result, status_code = process_image(request.data['image_url'])
#             return Response(result, status=status_code)
#         else:
#             print("No face found")
#             try:
#                 image_url = request.data['image_url']
#                 response = requests.get(image_url)
#                 image = Image.open(BytesIO(response.content))
#             except (KeyError, ValueError, requests.exceptions.RequestException, OSError) as e:
#                     try:
#                         with urllib.request.urlopen(image_url) as url:
#                             image_data = url.read()
                            
#                         image = Image.open(BytesIO(image_data))
#                     except Exception as e:
#                         return Response({"error": "Invalid request or unable to fetch image from URL"}, status=status.HTTP_400_BAD_REQUEST)

#             try:
#                 labels = classify_image(image)
#             except RuntimeError as e:
#                 return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            
#             serializer=[]     
#             query = Q()
#             for label in labels:
#                 query |= Q(labels__icontains=label)

#             image_finder = Image_Verification.objects.filter(query)

#             hold=False
#             if not Image_Verification.objects.filter(image_source=image_url):
#                 result = {"result": "unknown", "labels": labels, "meta_data":face_encodings,
#                           "image_hash":calculate_image_hash(image_url), "image_source":image_url}
#                 serializer = ImageVerificationSerializer(data=result)
#                 if serializer.is_valid():
#                  serializer.save()
#                  print("data is save in the database")
#                  hold=True
#             else:
#                 serializer = ImageVerificationSerializer(image_finder, many=True)


            
#             if image_finder.exists():
#                 if(hold):
#                     return Response( {"new image inserted and matched images":serializer.data}, status=status.HTTP_200_OK)
#                 else:
#                     return Response({"matched_images":serializer.data}, status=status.HTTP_200_OK)
            
#             else:
#                 if(hold):
#                     return Response({"new image inserted":serializer.data}, status=status.HTTP_200_OK)
#                 else:
#                     return Response({"no data will be found":serializer.data}, status=status.HTTP_200_OK)



















from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from PIL import Image
import requests
import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
from io import BytesIO
from django.shortcuts import render
from .models import Image_Verification
from .face_recognition_script import process_image
from .face_recognition_utility import extract_face_encodings, load_image_from_url, calculate_image_hash
from .serializers import ImageVerificationSerializer
from django.db.models import Q

# Load the pre-trained model
model = None
labels = []

def load_model():
    global model, labels
    model_url = "https://tfhub.dev/google/imagenet/mobilenet_v2_100_224/classification/4"
    try:
        print("Attempting to load model from URL:", model_url)
        model = hub.load(model_url)
        print("Model loaded successfully.")
        labels_path = tf.keras.utils.get_file('ImageNetLabels.txt', 'https://storage.googleapis.com/download.tensorflow.org/data/ImageNetLabels.txt')
        with open(labels_path, 'r') as f:
            labels = f.read().splitlines()
        print(f"Labels loaded successfully with {len(labels)} labels.")
    except Exception as e:
        print(f"Error loading model from {model_url}: {e}")
        import os
        temp_dir = os.path.join(os.getenv("HOME"), ".keras", "datasets")
        print(f"Check if the directory {temp_dir} exists and its contents.")
        if os.path.exists(temp_dir):
            print("Directory exists. Contents:")
            print(os.listdir(temp_dir))
        else:
            print("Directory does not exist.")

load_model()
print(f"Model: {model}")

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

def classify_image(image, top_k=5):
    if model is None:
        raise RuntimeError("The model has not been loaded successfully.")
    processed_image = preprocess_image(image)
    predictions = model(processed_image)
    predictions = np.array(predictions)
    top_k_indices = np.argsort(predictions[0], axis=-1)[::-1][:top_k]
    top_labels = [labels[idx] for idx in top_k_indices]
    return top_labels

class image_verification(APIView):
    def post(self, request, *args, **kwargs):
        try:
            image_url = request.data['image_url']
            image = load_image_from_url(image_url)
        except Exception as e:
            return Response({"error": "Invalid request or unable to fetch image from URL"}, status=status.HTTP_400_BAD_REQUEST)

        face_encodings = extract_face_encodings(image)
        print("this is length of face------------------>", len(face_encodings[0]))
      
        if len(face_encodings[0]) > 0:
            result, status_code = process_image(image_url)
            if status_code == 200:
                matched_images = result.get('matched_images', [])
                new_image = None if 'matched_images' in result else image_url
                return render(request, 'face_verification.html', {
                    'new_image': new_image,
                    'matched_images': matched_images
                })
            else:
                return Response(result, status=status_code)
        else:
            try:
                print("no face found")
                labels = classify_image(image)
            except RuntimeError as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            query = Q()
            for label in labels:
                query |= Q(labels__icontains=label)

            image_finder = Image_Verification.objects.filter(query)

            hold = False
            new_image = None
            if not Image_Verification.objects.filter(image_source=image_url).exists():
                result = {"result": "unknown", "labels": labels, "meta_data": face_encodings,
                          "image_hash": calculate_image_hash(image_url), "image_source": image_url}
                serializer = ImageVerificationSerializer(data=result)
                if serializer.is_valid():
                    serializer.save()
                    hold = True
                    new_image = image_url

            matched_images = list(image_finder.all())

            return render(request, 'image_verification.html', {
                'new_image': new_image,
                'matched_images': matched_images
            })
