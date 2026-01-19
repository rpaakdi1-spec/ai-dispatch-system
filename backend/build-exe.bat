@echo off
REM ===================================================================
REM AI Dispatch System - EXE 빌드 스크립트
REM ===================================================================

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║         AI 배차 시스템 실행 파일 빌드                        ║
echo ║         Building Executable for AI Dispatch System           ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

REM 현재 디렉토리 저장
set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%"

echo [1/4] 환경 확인 중...
echo.

REM Python 확인
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python이 설치되어 있지 않습니다!
    pause
    exit /b 1
)

echo ✅ Python 설치 확인

echo.
echo [2/4] PyInstaller 설치 중...

REM 가상환경 활성화
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
)

REM PyInstaller 설치
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo 📦 PyInstaller를 설치합니다...
    pip install pyinstaller
    if errorlevel 1 (
        echo ❌ PyInstaller 설치 실패!
        pause
        exit /b 1
    )
)

echo ✅ PyInstaller 준비 완료

echo.
echo [3/4] 실행 파일 빌드 중... (5-10분 소요)
echo.

REM 기존 빌드 폴더 삭제
if exist "build" rmdir /s /q build
if exist "dist" rmdir /s /q dist

REM PyInstaller로 빌드
pyinstaller --clean ai-dispatch.spec

if errorlevel 1 (
    echo ❌ 빌드 실패!
    pause
    exit /b 1
)

echo ✅ 빌드 완료

echo.
echo [4/4] 결과 확인 중...
echo.

if exist "dist\ai-dispatch-system.exe" (
    echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    echo.
    echo ✅ 실행 파일이 생성되었습니다!
    echo.
    echo 📂 위치: %SCRIPT_DIR%dist\ai-dispatch-system.exe
    echo 📦 크기: 
    for %%A in (dist\ai-dispatch-system.exe) do echo    %%~zA bytes
    echo.
    echo 💡 사용 방법:
    echo    1. dist\ai-dispatch-system.exe 파일을 더블클릭
    echo    2. 또는 명령 프롬프트에서 실행
    echo.
    echo ⚠️  참고사항:
    echo    - .env 파일을 exe와 같은 폴더에 두세요
    echo    - PostgreSQL과 Redis가 설치되어 있어야 합니다
    echo.
    echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
) else (
    echo ❌ 실행 파일 생성 실패!
)

echo.
pause
