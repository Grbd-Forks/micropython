@echo off
SETLOCAL

set "venv=%1"
if "%venv%" == "" ( set "venv=py27dev" )

IF EXIST "%venv%" (
    echo "Entering virtual environment %venv%"
    echo "use deactivate to leave"
    cmd /k "%~dp0\%venv%\Scripts\activate.bat"

) ELSE (
    echo "Creating virtual environment %venv%"
    tox -c tox_dev.ini
    echo "Entering virtual environment %venv%"
    echo "use deactivate to leave"
    cmd /k "%~dp0\%venv%\Scripts\activate.bat"
)

ENDLOCAL
