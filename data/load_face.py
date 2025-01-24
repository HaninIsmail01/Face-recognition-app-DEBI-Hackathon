import os
import dlib
import numpy as np
from app.database import add_face

# Load face detector and shape predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
face_encoder = dlib.face_descriptor_extractor()

def encode_face(image_path):
    img = dlib.load_rgb_image(image_path)
    faces = detector(img)
    
    if not faces:
        return None
    
    face = faces[0]  # Assuming we are only dealing with one face per image
    landmarks = predictor(img, face)
    face_encoding = np.array(face_encoder.compute_face_descriptor(img, landmarks))
    return face_encoding

def load_faces_from_directory(directory):
    for filename in os.listdir(directory):
        image_path = os.path.join(directory, filename)
        encoding = encode_face(image_path)
        if encoding is not None:
            name = filename.split('.')[0]  # Assume filename is the name of the person
            add_face(name, encoding)

# Example usage
load_faces_from_directory('images/dataset')
