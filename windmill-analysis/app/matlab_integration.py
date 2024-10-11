import matlab.engine
import os

def analyze_turbine_vibrations(video_path, alpha=100.0, fl=0.2, fh=0.25, fs=24.0):
    eng = matlab.engine.start_matlab()
    
    try:
        # Ustaw ścieżkę do folderu z kodem MATLAB
        matlab_code_path = os.path.abspath('vidmag')
        eng.addpath(eng.genpath(matlab_code_path))
        
        # Ustaw katalog roboczy na folder z kodem MATLAB
        eng.cd(matlab_code_path)
        
        # Wywołaj funkcję setPath z kodu MATLAB
        eng.setPath(nargout=0)
        
        # Przygotuj argumenty dla funkcji phaseAmplify
        outDir = os.path.abspath('results')  # Zmieniono ścieżkę wyjściową
        os.makedirs(outDir, exist_ok=True)  # Upewnij się, że folder istnieje
        # Parametry zgodne z reproduceResultsSiggraph13.m
        sigma = 5.0
        temporalFilter = eng.eval('@FIRWindowBP')
        pyrType = 'halfOctave'
        scaleVideo = 2.0/3.0 if scaleAndClipLargeVideos else 1.0

        # Upewnij się, że wszystkie numeryczne parametry są float
        alpha = float(alpha)
        fl = float(fl)
        fh = float(fh)
        fs = float(fs)

        # Wywołaj funkcję phaseAmplify
        result = eng.phaseAmplify(video_path, alpha, fl, fh, fs, outDir, 
                                  'sigma', sigma,
                                  'pyrType', pyrType,
                                  'temporalFilter', temporalFilter,
                                  'scaleVideo', scaleVideo,
                                  nargout=1)
        # Znajdź wygenerowany plik wideo
        output_video = None
        print(os.path.basename(video_path))
        for file in os.listdir(outDir):
            if file.endswith('.mp4') and file.startswith(result):
                output_video = os.path.join(outDir, file)
                break
        if output_video is None:
            raise Exception("Output video file not found")
        # Konwertuj wynik MATLAB na słownik Pythona
        python_result = {
            "output_file": output_video,
            "magnification": alpha,
            "low_freq": fl,
            "high_freq": fh,
            "sampling_rate": fs,
            "input_video": video_path,
            "output_dir": outDir,
            "sigma": sigma,
            "pyr_type": pyrType,
            "scale_video": scaleVideo
        }
        return python_result
    except Exception as e:
        return {"error": str(e)}
    finally:
        eng.quit()

# Globalna zmienna kontrolująca skalowanie wideo
scaleAndClipLargeVideos = True

def set_scale_and_clip_large_videos(value):
    global scaleAndClipLargeVideos
    scaleAndClipLargeVideos = value