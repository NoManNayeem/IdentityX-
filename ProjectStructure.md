# Project Structure

```
IdentityX_Project/
├── app.py                  # Main Flask app with routes, blueprint registration, and app config
├── blueprints/             # Directory for modular blueprints
│   ├── __init__.py         # Init file for the blueprints package
│   ├── register.py         # Register blueprint with user registration logic
│   └── recognize.py        # Recognize blueprint with real-time face recognition
├── database/               # Database directory (created on app startup if not exists)
│   └── users.db            # SQLite database file
├── static/                 # Static assets
│   ├── css/
│   │   └── styles.css      # Custom styling for the application
│   └── js/
│       └── scripts.js      # JavaScript for handling user card display and flash messages
├── templates/              # HTML templates for rendering views
│   ├── index.html          # Landing page for the app
│   ├── register.html       # User registration page
│   └── recognize.html      # Real-time face recognition page
├── utils.py                # Utility functions for shared resources (database, face recognition)
├── .env                    # Environment variables (e.g., secret key)
└── requirements.txt        # Project dependencies

```