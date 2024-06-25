import face_recognition
from PIL import Image, UnidentifiedImageError
import numpy as np
import requests
from PIL import Image
from io import BytesIO
import hashlib
import base64
import urllib.request

def load_image_from_url(image_url):
    try:
        with urllib.request.urlopen(image_url) as url:
            image_data = url.read()
        image = Image.open(BytesIO(image_data))
        image = image.convert('RGB')  # Ensure the image is in RGB format
        return image
    except urllib.error.HTTPError as e:
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
