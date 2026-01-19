@echo off
REM ===================================================================
REM AI Dispatch System - Windows 실행 스크립트
REM ===================================================================

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║         AI 배차 시스템 자동 실행 스크립트                    ║
echo ║         AI Dispatch System Auto Launcher                     ║
echo ╔══════════════════════════════════════════════════════════════╝
echo.

REM 현재 디렉토리 저장
set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%"

echo [1/5] 환경 확인 중...
echo.

REM Python 확인
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python이 설치되어 있지 않습니다!
    echo.
    echo Python 3.10 이상을 설치해주세요:
    echo https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo ✅ Python 설치 확인
python --version

echo.
echo [2/5] 가상환경 확인 중...

REM 가상환경이 없으면 생성
if not exist "venv" (
    echo 📦 가상환경을 생성합니다...
    python -m venv venv
    if errorlevel 1 (
        echo ❌ 가상환경 생성 실패!
        pause
        exit /b 1
    )
    echo ✅ 가상환경 생성 완료
) else (
    echo ✅ 가상환경 존재 확인
)

echo.
echo [3/5] 가상환경 활성화 중...

REM 가상환경 활성화
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ❌ 가상환경 활성화 실패!
    pause
    exit /b 1
)

echo ✅ 가상환경 활성화 완료

echo.
echo [4/5] 필수 패키지 확인 중...

REM requirements.txt가 있으면 패키지 설치
if exist "requirements.txt" (
    REM 패키지가 이미 설치되어 있는지 확인
    pip show fastapi >nul 2>&1
    if errorlevel 1 (
        echo 📦 필수 패키지를 설치합니다... (2-3분 소요)
        pip install -q -r requirements.txt
        if errorlevel 1 (
            echo ❌ 패키지 설치 실패!
            echo.
            echo 다음 명령어로 수동 설치해주세요:
            echo pip install -r requirements.txt
            pause
            exit /b 1
        )
        echo ✅ 패키지 설치 완료
    ) else (
        echo ✅ 패키지 설치 확인
    )
)

echo.
echo [5/5] 서버 시작 중...
echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.
echo 🚀 AI 배차 시스템을 시작합니다...
echo.
echo 📖 API 문서: http://localhost:8000/docs
echo 💚 헬스 체크: http://localhost:8000/health
echo.
echo ⚠️  서버를 종료하려면 Ctrl+C 를 누르세요
echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

REM 서버 실행
python main.py

REM 서버 종료 시
echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.
echo 👋 서버가 종료되었습니다.
echo.
pause
