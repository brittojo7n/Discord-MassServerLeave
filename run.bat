@echo off
IF NOT EXIST venv\ (
    python -m venv venv
)
call venv\Scripts\activate

python -c "import requests" 
IF %ERRORLEVEL% NEQ 0 (
    ECHO Installing missing requirements...
    python -m pip install -r requirements.txt
)
cls
python main.py