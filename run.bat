@echo off
python -c "import requests" 
IF %ERRORLEVEL% NEQ 0 (
    ECHO Installing missing requirements...
    python -m pip install -r requirements.txt
)
cls
python main.py
