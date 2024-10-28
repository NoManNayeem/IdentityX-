# app.py
from flask import Flask, render_template, Response
from blueprints.register import register_bp
from blueprints.recognize import recognize_bp
from flask_cors import CORS
from flask_executor import Executor
from utils import generate_frames
import sqlite3



app = Flask(__name__)
app.secret_key = 'your_secret_key'
CORS(app)  # Enable CORS for cross-origin requests
executor = Executor(app)  # For background tasks

# Register blueprints for modular routes
app.register_blueprint(register_bp)
app.register_blueprint(recognize_bp)

# Route for the landing page
@app.route('/')
def index():
    return render_template('index.html')

# Video feed route
@app.route('/video_feed')
async def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Initialize database on first run
def init_db():
    import os
    os.makedirs("database", exist_ok=True)
    conn = sqlite3.connect('database/users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users 
                 (id INTEGER PRIMARY KEY, name TEXT, embedding TEXT)''')
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
