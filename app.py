from flask import Flask, render_template, Response, request, redirect, url_for, flash
from deepface import DeepFace
import numpy as np
import cv2
import sqlite3
import pickle
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'
camera = cv2.VideoCapture(0)  # Initialize camera feed

# Database setup function
def init_db():
    os.makedirs("database", exist_ok=True)
    conn = sqlite3.connect('database/users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users 
                 (id INTEGER PRIMARY KEY, name TEXT, embedding BLOB)''')
    conn.commit()
    conn.close()


# Route for the landing page
@app.route('/')
def index():
    return render_template('index.html')



# Route to register new user and save face embedding
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get("name")
        if not name:
            flash("Name is required!", "error")
            return redirect(url_for('register'))

        try:
            success, frame = camera.read()
            if not success:
                flash("Failed to capture image.", "error")
                return redirect(url_for('register'))

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            embedding_data = DeepFace.represent(rgb_frame, model_name='Facenet')

            if embedding_data:
                embedding = embedding_data[0]["embedding"]
                save_embedding(name, embedding)
                flash("User registered successfully!", "success")
                return redirect(url_for('recognize'))
            else:
                flash("Failed to generate embedding.", "error")
                return redirect(url_for('register'))

        except Exception as e:
            flash(f"Error during registration: {str(e)}", "error")
            return redirect(url_for('register'))

    return render_template('register.html')

# Route for live recognition page
@app.route('/recognize')
def recognize():
    return render_template('recognize.html')

# Function to handle video streaming with face recognition
def generate_frames():
    try:
        while True:
            success, frame = camera.read()
            if not success:
                break
            else:
                frame = perform_face_recognition(frame)
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    except GeneratorExit:
        pass

# Video feed route
@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Helper function to save embeddings to the database
def save_embedding(name, embedding):
    try:
        conn = sqlite3.connect('database/users.db')
        c = conn.cursor()
        c.execute("INSERT INTO users (name, embedding) VALUES (?, ?)", 
                  (name, pickle.dumps(embedding)))
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"Database error: {str(e)}")

# Perform face recognition on a frame
def euclidean_distance(embedding1, embedding2):
    return np.linalg.norm(np.array(embedding1) - np.array(embedding2))

def perform_face_recognition(frame):
    try:
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_embedding_data = DeepFace.represent(rgb_frame, model_name="Facenet")
        
        if not frame_embedding_data:
            print("No embedding found in frame.")
            return frame
        
        frame_embedding = frame_embedding_data[0]["embedding"]
        users = load_all_embeddings()

        threshold = 10  # Adjust threshold based on testing
        for user in users:
            user_embedding = user['embedding']
            distance = euclidean_distance(frame_embedding, user_embedding)
            if distance <= threshold:
                cv2.putText(frame, f"Recognized: {user['name']}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                break
        return frame

    except Exception as e:
        print(f"Recognition error: {str(e)}")
        cv2.putText(frame, "Recognition error", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        return frame

# Load all embeddings from the database
def load_all_embeddings():
    try:
        conn = sqlite3.connect('database/users.db')
        c = conn.cursor()
        c.execute("SELECT name, embedding FROM users")
        users = [{"name": row[0], "embedding": pickle.loads(row[1])} for row in c.fetchall()]
        conn.close()
        return users
    except sqlite3.Error as e:
        print(f"Database loading error: {str(e)}")
        return []

# Initialize database on first run
if __name__ == "__main__":
    init_db()
    app.run(debug=True)
