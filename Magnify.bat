@echo off
cd %~dp0
pip install -r ./requirements.txt
flask run --host=localhost --port=5000
start "" http://localhost:5000