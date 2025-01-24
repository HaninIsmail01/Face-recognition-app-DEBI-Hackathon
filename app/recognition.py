import face_recognition
import numpy as np

# Load known faces from the database
def load_known_faces():
    conn = sqlite3.connect('data/faces.db')
    c = conn.cursor()
    c.execute("SELECT name, encoding FROM faces")
    rows = c.fetchall()
    known_faces = []
    
    for row in rows:
        name = row[0]
        encoding = np.frombuffer(row[1], dtype=np.float64)
        known_faces.append({"name": name, "encoding": encoding})
    
    conn.close()
    return known_faces

# Recognize faces from the image
def recognize_face(image):
    known_faces = load_known_faces()
    
    # Find all face locations and encodings in the provided image
    face_locations = face_recognition.face_locations(image)
    face_encodings = face_recognition.face_encodings(image, face_locations)
    
    face_names = []
    for face_encoding in face_encodings:
        # Compare the detected face encoding with known face encodings
        matches = face_recognition.compare_faces([f['encoding'] for f in known_faces], face_encoding)
        name = "Unknown"
        
        # If a match is found, set the name of the person
        if True in matches:
            first_match_index = matches.index(True)
            name = known_faces[first_match_index]['name']
        
        face_names.append(name)
    
    # Return the result
    return {"face_names": face_names, "face_locations": face_locations}
