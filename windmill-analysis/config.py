import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    # Uzyskaj ścieżkę do głównego katalogu projektu (windmill-analysis)
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    # Ustaw UPLOAD_FOLDER jako podkatalog 'uploads' w głównym katalogu projektu
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
    RESULTS_FOLDER = os.path.join(BASE_DIR, 'results')
    ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov'}

    VIDEO_ANALYSIS = {
        'EDGE_THRESHOLD_LOW': 50,
        'EDGE_THRESHOLD_HIGH': 150,
        'HOUGH_THRESHOLD': 200,
        'ROTATION_ANGLE_THRESHOLD': 120
    }