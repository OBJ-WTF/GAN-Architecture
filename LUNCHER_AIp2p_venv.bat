@echo off
setlocal

echo === Activation de l'environnement virtuel Python ===
if not exist venv\Scripts\activate.bat (
    echo ❌ Environnement virtuel non trouvé.
    echo Création de l'environnement...
    python -m venv venv
)

call venv\Scripts\activate.bat

echo === Installation des dépendances (si nécessaires) ===
pip install --upgrade pip
pip install -r requirements.txt

echo === CUDA Path (si nécessaire à modifier selon ta version CUDA) ===
set "CUDA_PATH=C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.3"
set "PATH=%CUDA_PATH%\bin;%CUDA_PATH%\libnvvp;%PATH%"

echo === Lancement de l'application ===
python AIp2p.py

pause
