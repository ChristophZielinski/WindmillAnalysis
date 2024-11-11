# WindmillAnalysis
**JAK URUCHOMIĆ**<br />

Przy pierwszym uruchomieniu:
1. Otworzyć terminal w głównym katalogu windmill_analysis<br />
2. python -m venv venv<br />
3. venv\Scripts\activate<br />
4. pip install -r requirements.txt<br />
5. python run.py<br />
6. Po zakończeniu ctrl+c i w terminalu deactivate<br />

Przy kolejnym uruchomieniu
1. venv\Scripts\activate<br />
2. python run.py<br />
3. Po zakończeniu ctrl+c i w terminalu deactivate<br />

**WYMAGANIA**<br />
MATLAB
* Z zainstalowanym Image Processing Toolbox

Python
* Zainstalowanie najnowszej wersji Python

matlab.engine dla Pythona
* Do integracji między Pythonem a MATLAB-em

matlabPyrTools
* Zewnętrzna biblioteka MATLAB używana w projekcie

FFmpeg
* Do manipulacji plikami wideo (jeśli nie jest już obsługiwane przez OpenCV)

Pliki wideo do analizy
* Przykładowe lub własne pliki wideo do przetwarzania

Odpowiednia konfiguracja środowiska
* Ustawienie zmiennych środowiskowych, ścieżek itp.

Wydajny komputer
* Ze względu na obliczeniowo intensywne przetwarzanie wideo
