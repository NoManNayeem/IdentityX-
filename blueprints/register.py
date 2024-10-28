# blueprints/register.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from utils import save_embedding, camera
import cv2
from deepface import DeepFace

register_bp = Blueprint('register_bp', __name__, template_folder='templates')

# Route to register a new user and save face embedding
@register_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get("name")
        if not name:
            flash("Name is required!", "error")
            return redirect(url_for('register_bp.register'))

        try:
            # Capture a frame from the camera
            success, frame = camera.read()
            if not success:
                flash("Failed to capture image.", "error")
                return redirect(url_for('register_bp.register'))

            # Convert frame to RGB for DeepFace processing
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            embedding_data = DeepFace.represent(rgb_frame, model_name='Facenet')

            # Save embedding if it was successfully generated
            if embedding_data:
                embedding = embedding_data[0]["embedding"]
                save_embedding(name, embedding)
                flash("User registered successfully!", "success")
                return redirect(url_for('recognize_bp.recognize'))
            else:
                flash("Failed to generate embedding.", "error")
                return redirect(url_for('register_bp.register'))

        except Exception as e:
            flash(f"Error during registration: {str(e)}", "error")
            return redirect(url_for('register_bp.register'))

    return render_template('register.html')
