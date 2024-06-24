import face_recognition
from PIL import Image as PilImage
import numpy as np
import requests
from PIL import Image
from io import BytesIO
import hashlib
import base64


def load_image_from_url(image_url):
    try:
        response = requests.get(image_url)
        image = Image.open(BytesIO(response.content))
        # Convert image to RGB mode if it's not already in that format
        if image.mode != 'RGB':
            image = image.convert('RGB')
        return image
    except Exception as e:
        # Handle exceptions (e.g., invalid URL, unable to fetch image, etc.)
        raise e

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
