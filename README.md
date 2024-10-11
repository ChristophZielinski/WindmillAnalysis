# WindmillAnalysis
**JAK URUCHOMIĆ**<br />
Jeśli nie ma wirtualnego środowiska to najpierw:<br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;python -m venv venv<br /><br />
Jeśli już jest:
1. Otworzyć terminal w głównym katalogu windmill_analysis<br />
2. venv\Scripts\activate<br />
3. pip install -r requirements.txt<br />
4. python run.py<br />
5. Po zakończeniu ctrl+c i w terminalu deactivate<br />

**WYMAGANIA(chyba)**<br />
MATLAB
* Z zainstalowanym Image Processing Toolbox

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
