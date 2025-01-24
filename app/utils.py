import cv2
from skimage.feature import hog
from skimage import data, color, exposure
import numpy as np

def detect_and_crop_face(image_path):
  """
  Detects the largest face in an image and crops it.

  Args:
    image_path: Path to the image file.

  Returns:
    A NumPy array of the cropped face region, or None if no face is detected.
  """

  # Load the image
  img = cv2.imread(image_path)

  # Check if image was loaded successfully
  if img is None:
    print(f"Error: Could not load image at {image_path}")
    return None
  
  # Convert to grayscale
  gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

  # Load the cascade classifier (assuming the classifier file is in the same directory)
  # Update to use the full path to the classifier:
  face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml') 

  # Detect faces
  faces = face_cascade.detectMultiScale(gray, 1.1, 4)

  # Find the largest face
  if len(faces) > 1:
    largest_face = max(faces, key=lambda x: x[2] * x[3])  # Find face with largest area
    faces = [largest_face]

    # Crop the largest face
    for (x, y, w, h) in faces:
      face_roi = img[y:y+h, x:x+w]
      return face_roi  # Return the cropped face region
  else:
    print("No face detected in the image.")
    return None  # No face detected
  

def extract_hog_features(image_path):
  """
  Extracts HOG features from an image.

  Args:
    image_path: Path to the image file.

  Returns:
    A tuple containing:
      - HOG feature vector (1D NumPy array)
      - Visualized HOG image (optional, depending on the 'visualize' parameter)
  """

  # Load the image
  image = cv2.imread(image_path)
  image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Convert to grayscale

  # Resize the image (optional)
  image_size = (128, 128)
  image = cv2.resize(image, image_size)

  # Calculate HOG features
  fd, hog_image = hog(image, orientations=8, pixels_per_cell=(16, 16), 
                      cells_per_block=(2, 2), visualize=True) 

  # Reshape HOG features to 2D
  fd = fd.reshape(1, -1)

  return fd, hog_image