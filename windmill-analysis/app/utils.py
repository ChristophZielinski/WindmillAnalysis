import os
from werkzeug.utils import secure_filename
from app import app

ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_file(file, target_folder=None):
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        if target_folder is None:
            target_folder = app.config['UPLOAD_FOLDER']
        file_path = os.path.join(target_folder, filename)
        file.save(file_path)
        return file_path
    return None

def validate_video(file_path):
    # Sprawdź, czy plik istnieje
    if not os.path.exists(file_path):
        return False, "File does not exist"
    
    # Sprawdź, czy plik można otworzyć jako wideo
    import cv2
    cap = cv2.VideoCapture(file_path)
    if not cap.isOpened():
        return False, "Cannot open video file"
    
    # Sprawdź długość wideo
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if frame_count < 30:  # Przykładowy próg
        return False, "Video is too short"
    
    cap.release()
    return True, "Video is valid"