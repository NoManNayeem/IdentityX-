# Project Structure

```
IdentityX/
├── app.py
├── requirements.txt
├── templates/
│   ├── register.html
│   └── recognize.html
├── static/
│   ├── css/
│   │   └── styles.css
│   └── js/
│       └── scripts.js
├── models/
│   └── embeddings.pkl  # Will store user face embeddings (if using serialization)
└── database/
    └── users.db       # Automatically created on first run

```