import cv2
import numpy as np

def detect_turbine_blades(video_path):
    cap = cv2.VideoCapture(video_path)
    rotations = 0
    prev_angle = None
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # Konwertuj do skali szarości
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Wykryj krawędzie
        edges = cv2.Canny(gray, 50, 150)
        
        # Wykryj linie
        lines = cv2.HoughLines(edges, 1, np.pi/180, 200)
        
        if lines is not None:
            for rho, theta in lines[0]:
                angle = theta * 180 / np.pi
                
                if prev_angle is not None:
                    # Sprawdź, czy łopata przeszła pełny obrót
                    if abs(angle - prev_angle) > 120:  # Przykładowy próg
                        rotations += 1
                
                prev_angle = angle
    
    cap.release()
    return rotations

def count_rotations(video_path):
    is_valid, message = validate_video(video_path)
    if not is_valid:
        return {"error": message}
    
    rotations = detect_turbine_blades(video_path)
    return {"rotations": rotations}