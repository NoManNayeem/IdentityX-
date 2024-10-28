# utils.py
import sqlite3
import json
import cv2
import numpy as np
from deepface import DeepFace

# Initialize the camera feed
camera = cv2.VideoCapture(0)

# Helper function to save embeddings to the database
def save_embedding(name, embedding):
    try:
        conn = sqlite3.connect('database/users.db')
        c = conn.cursor()
        c.execute("INSERT INTO users (name, embedding) VALUES (?, ?)", 
                  (name, json.dumps(embedding)))
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"Database error: {str(e)}")

# Load all embeddings from the database
def load_all_embeddings():
    try:
        conn = sqlite3.connect('database/users.db')
        c = conn.cursor()
        c.execute("SELECT name, embedding FROM users")
        users = [{"name": row[0], "embedding": json.loads(row[1])} for row in c.fetchall()]
        conn.close()
        return users
    except sqlite3.Error as e:
        print(f"Database loading error: {str(e)}")
        return []

# Perform face recognition on a frame
def perform_face_recognition(frame):
    try:
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_embedding_data = DeepFace.represent(rgb_frame, model_name="Facenet")
        
        if not frame_embedding_data:
            return frame  # No face detected
        
        frame_embedding = frame_embedding_data[0]["embedding"]
        users = load_all_embeddings()

        threshold = 10  # Adjust threshold based on testing
        for user in users:
            user_embedding = user['embedding']
            distance = np.linalg.norm(np.array(frame_embedding) - np.array(user_embedding))
            if distance <= threshold:
                cv2.putText(frame, f"Recognized: {user['name']}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                break
        return frame

    except Exception as e:
        print(f"Recognition error: {str(e)}")
        cv2.putText(frame, "Recognition error", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        return frame

# Generate frames for the video feed
def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        frame = perform_face_recognition(frame)
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
