@echo off
REM GUI 런처 실행 스크립트

cd /d "%~dp0"

REM 가상환경 활성화
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
)

REM GUI 런처 실행
python launcher.py

if errorlevel 1 (
    echo.
    echo ❌ 실행 실패!
    echo.
    pause
)
