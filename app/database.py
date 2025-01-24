import sqlite3
import numpy as np
import csv

DB_PATH = 'data/faces.db'  # Note: database should be .db, not .csv

# Create the database and table if it doesn't exist
def create_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(''' 
        CREATE TABLE IF NOT EXISTS faces (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            encoding BLOB NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Load known faces from the CSV file
def load_faces_from_csv(csv_file_path):
    faces = []
    
    try:
        with open(csv_file_path, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                name = row['name']
                encoding_str = row['encoding']
                
                # Convert encoding from string to numpy array
                encoding = np.fromstring(encoding_str.strip('[]'), sep=',')
                
                faces.append({"name": name, "encoding": encoding})
    except FileNotFoundError:
        print(f"CSV file {csv_file_path} not found.")
    
    return faces

# Add a new face to the database
def add_face(name, encoding):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO faces (name, encoding) VALUES (?, ?)", 
              (name, encoding.tobytes()))  # Convert numpy array to bytes
    conn.commit()
    conn.close()

# Get all known faces from the database
def get_known_faces():
    conn = sqlite3.connect(DB_PATH)
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

# Example usage
if __name__ == "__main__":
    # Create the database and table
    create_db()
    
    # Load faces from CSV and add them to the database
    faces = load_faces_from_csv('data/faces.csv')  # Specify the correct path to your CSV file
    for face in faces:
        add_face(face['name'], face['encoding'])
    
    # Retrieve and display all known faces
    known_faces = get_known_faces()
    for known_face in known_faces:
        print(f"Name: {known_face['name']}, Encoding: {known_face['encoding']}")
