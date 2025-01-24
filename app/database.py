import sqlite3
import numpy as np
import dlib

DB_PATH = 'database/faces.db'

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

def add_face(name, encoding):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO faces (name, encoding) VALUES (?, ?)", 
              (name, encoding.tobytes()))
    conn.commit()
    conn.close()
