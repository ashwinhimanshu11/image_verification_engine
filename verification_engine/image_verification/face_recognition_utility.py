import face_recognition
from PIL import Image, UnidentifiedImageError
import numpy as np
import requests
from PIL import Image
from io import BytesIO
import hashlib
import base64
import urllib.request
import requests
from django.http import JsonResponse

def load_image_from_url(image_url):
    try:
        with urllib.request.urlopen(image_url) as url:
            image_data = url.read()
            
        image = Image.open(BytesIO(image_data))
        image = image.convert('RGB')  # Ensure the image is in RGB format
        return image
    except urllib.error.HTTPError as e:
        try:
              response = requests.get(image_url)
              image = Image.open(BytesIO(response.content))
              image = image.convert('RGB')  # Ensure the image is in RGB format
              return image
        except Exception as e:
                raise ValueError('Error downloading image:')

        if e.code == 403:
            raise ValueError("Access to the image URL is forbidden.")
        else:
            raise ValueError(f"HTTP error occurred: {e}")
    except (urllib.error.URLError, OSError, UnidentifiedImageError) as e:
        raise ValueError("Could not load the image from the provided URL.")
    




def extract_face_encodings(image):
    # Convert PIL image to numpy array
    image_np = np.array(image)
    
    # Detect faces and extract face encodings
    face_locations = face_recognition.face_locations(image_np)
    face_encodings = face_recognition.face_encodings(image_np, face_locations)
    
    return face_encodings



def match_face(face_encoding, known_encodings):
    matches = face_recognition.compare_faces(known_encodings, face_encoding)
    return matches

def calculate_image_hash(image_url):
    return hashlib.md5(image_url.encode()).hexdigest()

def encode_face_encoding(face_encoding):
    return base64.b64encode(np.array(face_encoding)).decode('utf-8')

def decode_face_encoding(encoded_face):
    return np.frombuffer(base64.b64decode(encoded_face.encode('utf-8')), dtype=np.float64)









# import face_recognition
# from PIL import Image, UnidentifiedImageError, ImageEnhance
# import numpy as np
# import requests
# from io import BytesIO
# import hashlib
# import base64
# import urllib.request
# import cv2

# def load_image_from_url(image_url):
#     try:
#         with urllib.request.urlopen(image_url) as url:
#             image_data = url.read()
            
#         image = Image.open(BytesIO(image_data))
#         image = image.convert('RGB')  # Ensure the image is in RGB format
#         return image
#     except urllib.error.HTTPError as e:
#         try:
#             response = requests.get(image_url)
#             image = Image.open(BytesIO(response.content))
#             image = image.convert('RGB')  # Ensure the image is in RGB format
#             return image
#         except Exception as e:
#             raise ValueError('Error downloading image:')

#         if e.code == 403:
#             raise ValueError("Access to the image URL is forbidden.")
#         else:
#             raise ValueError(f"HTTP error occurred: {e}")
#     except (urllib.error.URLError, OSError, UnidentifiedImageError) as e:
#         raise ValueError("Could not load the image from the provided URL.")

# def rotate_image(image, angle):
#     # Rotate the image by the specified angle
#     center = (image.shape[1] // 2, image.shape[0] // 2)
#     M = cv2.getRotationMatrix2D(center, angle, 1)
#     rotated = cv2.warpAffine(image, M, (image.shape[1], image.shape[0]))
#     return rotated

# def sharpen_image(image):
#     # Convert to PIL image
#     pil_image = Image.fromarray(image)
#     enhancer = ImageEnhance.Sharpness(pil_image)
#     sharp_image = enhancer.enhance(2.0)  # Increase sharpness by a factor of 2
#     return np.array(sharp_image)

# def extract_face_encodings(image):
#     # Convert PIL image to numpy array
#     image_np = np.array(image)
    
#     # Sharpen the image to handle blurring
#     sharpened_image = sharpen_image(image_np)
    
#     best_encodings = []
#     best_locations = []
    
#     # Try different rotations
#     for angle in range(0, 360, 15):
#         rotated_image = rotate_image(sharpened_image, angle)
        
#         # Detect faces and extract face encodings
#         face_locations = face_recognition.face_locations(rotated_image)
#         face_encodings = face_recognition.face_encodings(rotated_image, face_locations)
        
#         # If faces are found, return the results
#         if face_encodings:
#             if len(face_encodings) > len(best_encodings):
#                 best_encodings = face_encodings
#                 best_locations = face_locations
    
#     return best_encodings, best_locations

# def match_face(face_encoding, known_encodings):
#     matches = face_recognition.compare_faces(known_encodings, face_encoding)
#     return matches

# def calculate_image_hash(image_url):
#     return hashlib.md5(image_url.encode()).hexdigest()

# def encode_face_encoding(face_encoding):
#     return base64.b64encode(np.array(face_encoding)).decode('utf-8')

# def decode_face_encoding(encoded_face):
#     return np.frombuffer(base64.b64decode(encoded_face.encode('utf-8')), dtype=np.float64)

