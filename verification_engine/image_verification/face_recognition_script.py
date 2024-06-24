from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Image_Verification
from .face_recognition_utility import load_image_from_url, extract_face_encodings, match_face, calculate_image_hash, encode_face_encoding, decode_face_encoding
import numpy as np
import json

# @csrf_exempt
def process_image(image_url):
    if not image_url:
        return {'error': 'No image URL provided'}, 400

    image = load_image_from_url(image_url)
    face_encodings = extract_face_encodings(image)

    if not face_encodings:
        return {'message': 'No face found'}, 200

    matched_images = []
    known_faces = Image_Verification.objects.filter(label='human')
    print(known_faces)
    known_encodings = [decode_face_encoding(face.face_encoding) for face in known_faces if face.face_encoding]

    for face_encoding in face_encodings:
        matches = match_face(face_encoding, known_encodings)
        if any(matches):
            matched_faces = [known_faces[i] for i, match in enumerate(matches) if match]
            matched_images += [face.image_source for face in matched_faces]
        else:
            # Save new face encoding and image details to database
            image_hash = calculate_image_hash(image_url)
            encoded_face = encode_face_encoding(face_encoding)
            new_image = Image_Verification(
                image_source=image_url,
                image_hash=image_hash,
                face_encoding=encoded_face,
                label="human"
            )
            new_image.set_meta_data(face_encoding)
            new_image.save()

    if matched_images:
        existing_url= Image_Verification.objects.filter(image_source=image_url)
        if(existing_url):
            print("url_found")
        else:
            hash = calculate_image_hash(image_url)
            face = encode_face_encoding(face_encoding)
            _image = Image_Verification(
                image_source=image_url,
                image_hash=hash,
                face_encoding=face,
                label="human",
            )
            _image.set_meta_data(face)
            _image.save()
        return {'matched_images': matched_images}, 200
    else:
        return {'message': 'No matching faces found, new image stored'}, 200
