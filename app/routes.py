from flask import Blueprint, request, jsonify, current_app
import base64
from app.recognition import recognize_face
from PIL import Image
import numpy as np

app_routes = Blueprint('app_routes', __name__)

# Route to serve index.html from the 'static' folder
@app_routes.route('/')
def index():
    return current_app.send_static_file('index.html')

# Route to handle face recognition
@app_routes.route('/recognize', methods=['POST'])
def recognize():
    try:
        # Get the base64 image data from the request
        data = request.get_json()
        image_data = data['image']

        # Decode the base64 image
        image_data = image_data.split(",")[1]  # Remove the "data:image/png;base64," part
        img_bytes = base64.b64decode(image_data)
        img = Image.open(BytesIO(img_bytes))
        
        # Convert the image to OpenCV format
        img = np.array(img)
        img = img[:, :, ::-1]  # Convert RGB to BGR (OpenCV format)
        
        # Process the image for face recognition
        result = recognize_face(img)
        
        return jsonify(result)
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400
