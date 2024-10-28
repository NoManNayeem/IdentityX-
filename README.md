
# IdentityX

IdentityX is a Flask-based application that utilizes deep learning for facial recognition. This project allows users to register their faces and perform live recognition using a camera feed.

## Features

- **User Registration**: Capture and save facial embeddings for new users.
- **Live Recognition**: Identify registered users in real-time using video streaming.
- **Database Integration**: Store user information and embeddings in a SQLite database.

## Requirements

- Python 3.12
- Flask
- DeepFace
- OpenCV
- SQLite
- NumPy

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/NoManNayeem/IdentityX-.git
    cd IdentityX
    ```

2. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

3. Set up the database by running the application for the first time:
    ```bash
    python app.py
    ```

## Usage

- Start the Flask application:
    ```bash
    python app.py
    ```
- Open your browser and navigate to `http://127.0.0.1:5000/` to access the application.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [Flask](https://flask.palletsprojects.com/) - The web framework used.
- [DeepFace](https://github.com/serengil/deepface) - A lightweight face recognition library.
- [OpenCV](https://opencv.org/) - A library for computer vision tasks.
