# blueprints/recognize.py
from flask import Blueprint, render_template, Response
from utils import generate_frames

recognize_bp = Blueprint('recognize_bp', __name__, template_folder='templates')

# Route for live recognition page
@recognize_bp.route('/recognize')
def recognize():
    return render_template('recognize.html')

# Video feed route for real-time recognition
@recognize_bp.route('/recognize_feed')
def recognize_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
