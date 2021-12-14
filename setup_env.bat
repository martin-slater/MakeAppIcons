@echo off

IF EXIST .pyenv\. (
    echo Deleting existing environment
    del /F /S /Q .pyenv > NUL
)

echo Creating environment
python3 -m venv .pyenv
.pyenv\Scripts\python.exe -m pip install --upgrade pip > NUL

echo Install requirements
call .pyenv/Scripts/activate.bat
pip3 install -r requirements.txt

