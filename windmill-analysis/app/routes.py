from flask import request, jsonify, render_template, send_file, Response
from app import app
from app.utils import save_file
from app.matlab_integration import analyze_turbine_vibrations
#from INUSER.Model import Model
#from INUSER.View import View
import cv2
import numpy as np
import os
import logging
import io

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
# Konfiguracja logowania
logging.basicConfig(level=logging.DEBUG)
cygert_analysis = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/mit_analysis')
def mit_analysis():
    return render_template('mit_analysis.html')

@app.route('/cygert_analysis')
def cygert_analysis_page():
    return render_template('cygert_analysis.html')

@app.route('/list_uploads')
def list_uploads():
    upload_folder = app.config['UPLOAD_FOLDER']
    files = [f for f in os.listdir(upload_folder) if os.path.isfile(os.path.join(upload_folder, f))]
    return jsonify({'files': files})

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    upload_folder = app.config['UPLOAD_FOLDER']
    logging.info(f"Upload folder path: {upload_folder}")
    os.makedirs(upload_folder, exist_ok=True)
    file_path = save_file(file)
    
    if file_path:
        logging.info(f"File uploaded successfully to: {file_path}")
        return jsonify({'message': 'File uploaded successfully', 'path': os.path.basename(file_path)}), 200
    logging.error("File upload failed")
    return jsonify({'error': 'File upload failed'}), 400

@app.route('/analyze', methods=['POST'])
def analyze_video():
    logging.info(f"Current working directory: {os.getcwd()}")

    if 'file' not in request.form:
        logging.error("No file specified")
        return jsonify({'error': 'No file specified'}), 400
    
    file_name = request.form['file']
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
    
    if not os.path.exists(file_path):
        logging.error(f"File not found: {file_path}")
        return jsonify({'error': 'File not found'}), 400
    
    alpha = float(request.form.get('alpha', 50))
    fl = float(request.form.get('fl', 0.2))
    fh = float(request.form.get('fh', 0.25))
    fs = float(request.form.get('fs', 24))

    logging.debug(f"Analysis parameters: alpha={alpha}, fl={fl}, fh={fh}, fs={fs}")
    logging.info(f"Starting analysis for file: {file_path}")

    result = analyze_turbine_vibrations(file_path, alpha, fl, fh, fs)
    if 'error' in result:
        logging.error(f"Analysis failed: {result['error']}")
        return jsonify(result), 400
    
    logging.info("Analysis completed successfully")
    
    output_file = os.path.basename(result['output_file'])
    output_file_path = os.path.join(app.config['RESULTS_FOLDER'], output_file)

    if os.path.exists(output_file_path):
        result['output_file'] = f'/results/{output_file}'
    else:
        return jsonify({'error': 'Output file not found'}), 400
    
    return jsonify(result), 200

@app.route('/results/<path:filename>')
def serve_video(filename):
    video_path = os.path.join(app.config['RESULTS_FOLDER'], filename)
    logging.info(f"Attempting to serve video from: {video_path}")
    if not os.path.exists(video_path):
        logging.error(f"Video file not found: {video_path}")
        return jsonify({'error': f'Video file not found: {video_path}'}), 404
    return send_file(video_path)

inuser_model = None
inuser_view = None

@app.route('/cygert_analysis')
def cygert_analysis():
    return render_template('cygert_analysis.html')

@app.route('/init_model')
def init_model():
    global inuser_model, inuser_view
    try:
        video_path = os.path.join(app.config['UPLOAD_FOLDER'], 'Farma1.MOV')
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Plik wideo nie istnieje: {video_path}")
        inuser_model = Model(video_path, isCamera=False)
        inuser_view = View()
        logging.info("Model i widok zainicjalizowane pomyślnie")
        return jsonify({'success': True})
    except Exception as e:
        logging.error(f"Błąd podczas inicjalizacji modelu: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/video_feed')
def video_feed():
    def generate():
        global inuser_model, inuser_view
        if inuser_model is None or inuser_view is None:
            logging.error("Model lub widok nie jest zainicjalizowany")
            return

        while True:
            try:
                ret, frame = inuser_model.update()
                if not ret:
                    logging.warning("Nie można odczytać klatki z wideo")
                    break
                
                frame = inuser_view.draw(frame, inuser_model)
                _, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            except Exception as e:
                logging.error(f"Błąd podczas generowania klatki: {str(e)}")
                break

    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/background_removed_feed')
def background_removed_feed():
    def generate():
        global inuser_model
        if inuser_model is None:
            logging.error("Model nie jest zainicjalizowany")
            return

        while True:
            try:
                bg_removed = inuser_model.get_background_removed()
                _, buffer = cv2.imencode('.jpg', bg_removed)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            except Exception as e:
                logging.error(f"Błąd podczas generowania klatki z usuniętym tłem: {str(e)}")
                break

    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/turbine_data')
def turbine_data():
    global inuser_model
    if inuser_model:
        try:
            data = inuser_model.get_turbine_data()
            return jsonify(data)
        except Exception as e:
            logging.error(f"Błąd podczas pobierania danych turbiny: {str(e)}")
            return jsonify({'error': str(e)}), 500
    return jsonify([])

@app.route('/get_fps')
def get_fps():
    global inuser_model
    if inuser_model:
        return jsonify({'fps': inuser_model.get_fps()})
    return jsonify({'fps': 0})

@app.route('/remove_turbine', methods=['POST'])
def remove_turbine():
    global inuser_model
    if inuser_model:
        inuser_model.remove_turbine()
        return jsonify({'success': True})
    return jsonify({'error': 'Model nie jest zainicjalizowany'}), 400

@app.route('/add_turbine', methods=['POST'])
def add_turbine():
    global inuser_model
    if inuser_model:
        inuser_model.add_turbine()
        return jsonify({'success': True})
    return jsonify({'error': 'Model nie jest zainicjalizowany'}), 400

@app.route('/find_turbines', methods=['POST'])
def find_turbines():
    global inuser_model
    if inuser_model:
        inuser_model.find_turbines()
        return jsonify({'success': True})
    return jsonify({'error': 'Model nie jest zainicjalizowany'}), 400

@app.route('/start_analysis', methods=['POST'])
def start_analysis():
    global inuser_model
    if inuser_model:
        inuser_model.start_analysis()
        return jsonify({'success': True})
    return jsonify({'error': 'Model nie jest zainicjalizowany'}), 400

@app.route('/stop_analysis', methods=['POST'])
def stop_analysis():
    global inuser_model
    if inuser_model:
        inuser_model.stop_analysis()
        return jsonify({'success': True})
    return jsonify({'error': 'Model nie jest zainicjalizowany'}), 400