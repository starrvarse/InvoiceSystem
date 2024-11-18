
@echo off
echo Building Invoice Management System...

REM Create virtual environment
python -m venv venv
call venv\Scripts\activate

REM Install requirements
pip install -r requirements.txt
pip install pyinstaller

REM Build executable
pyinstaller invoice_system.spec

REM Create README.txt
echo Invoice Management System > README.txt
echo Version 1.0 >> README.txt
echo. >> README.txt
echo Created by Arif Hussain >> README.txt
echo BigSur Corporation >> README.txt
echo. >> README.txt
echo For support, please contact: >> README.txt
echo Email: support@bigsur.com >> README.txt

REM Create installer
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer.iss

echo Build complete!
pause