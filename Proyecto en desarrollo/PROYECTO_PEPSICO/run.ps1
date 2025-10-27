# Script de ayuda para Windows PowerShell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process -Force
python -m venv .venv; .\.venv\Scripts\Activate.ps1; pip install -r requirements.txt
$env:FLASK_APP = "app.py"
flask run --host=127.0.0.1 --port=5000
