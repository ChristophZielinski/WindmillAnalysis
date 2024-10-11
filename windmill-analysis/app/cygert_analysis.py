import cv2
import numpy as np
from INUSER.Model import Model
from INUSER.View import View

class CygertAnalysis:
    def __init__(self, video_path):
        self.model = Model(video_path, isCamera=False)
        self.view = View()
        self.model.restart()  # Inicjalizacja turbiny

    def get_processed_frame(self):
        ret, frame = self.model.update()
        if ret:
            frame = self.view.draw(frame, self.model)
            _, buffer = cv2.imencode('.jpg', frame)
            return buffer.tobytes()
        return None

    def get_turbine_data(self):
        turbine_data = []
        for turbine in self.model.turbines:
            freq = turbine.get_freq()
            if freq is not None:
                turbine_data.append({'frequency': freq})
        return turbine_data