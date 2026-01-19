# 🚀 AI 배차 시스템 실행 가이드

이 문서는 AI 배차 시스템을 처음 실행하는 방법을 단계별로 설명합니다.

## 📋 목차
1. [빠른 시작](#빠른-시작)
2. [로컬 환경 실행](#로컬-환경-실행)
3. [Windows 실행 가이드](#windows-실행-가이드)
4. [Linux/macOS 실행 가이드](#linuxmacos-실행-가이드)
5. [문제 해결](#문제-해결)

---

## 🎯 빠른 시작

### 최소 요구사항
- ✅ Python 3.10 이상
- ✅ PostgreSQL 14 이상
- ✅ Redis 7 이상
- ✅ 5GB 이상 디스크 공간

### 5분 안에 시작하기

```bash
# 1. 저장소 클론
git clone https://github.com/rpaakdi1-spec/ai-dispatch-system.git
cd ai-dispatch-system/backend

# 2. 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. 패키지 설치
pip install -r requirements.txt

# 4. 서버 실행
python main.py
```

브라우저에서 http://localhost:8000/docs 접속!

---

## 🖥️ 로컬 환경 실행

### 1단계: 저장소 다운로드

**방법 1: Git 클론**
```bash
git clone https://github.com/rpaakdi1-spec/ai-dispatch-system.git
cd ai-dispatch-system
```

**방법 2: ZIP 다운로드**
1. https://github.com/rpaakdi1-spec/ai-dispatch-system 접속
2. "Code" 버튼 클릭 → "Download ZIP"
3. 다운로드 후 압축 해제
4. 터미널/CMD에서 압축 해제한 폴더로 이동

### 2단계: Python 확인

```bash
python --version
# 또는
python3 --version
```

**출력 예시:**
```
Python 3.10.11
```

3.10 미만이면 https://www.python.org/downloads/ 에서 최신 버전 설치

### 3단계: 가상환경 설정

```bash
cd backend

# 가상환경 생성
python -m venv venv

# 가상환경 활성화
# Windows (CMD):
venv\Scripts\activate.bat

# Windows (PowerShell):
venv\Scripts\Activate.ps1

# Linux/macOS:
source venv/bin/activate
```

가상환경 활성화 성공하면 프롬프트 앞에 `(venv)` 표시됨:
```
(venv) C:\ai-dispatch-system\backend>
```

### 4단계: 패키지 설치

```bash
pip install -r requirements.txt
```

설치 시간: 약 2-5분 (인터넷 속도에 따라)

### 5단계: 서버 실행

```bash
python main.py
```

**성공 메시지:**
```
🚀 Starting AI Dispatch System...
Environment: development
Debug Mode: True
✅ Database initialized successfully
✅ AI Dispatch System started on http://0.0.0.0:8000
📖 API Documentation available at http://0.0.0.0:8000/docs
```

### 6단계: API 문서 확인

브라우저에서 다음 주소 중 하나로 접속:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

---

## 🪟 Windows 실행 가이드

### 필수 프로그램 설치

#### 1. Python 설치

**winget 사용 (권장)**
```powershell
winget install Python.Python.3.12
```

**수동 설치**
1. https://www.python.org/downloads/windows/ 접속
2. "Download Python 3.12.x" 클릭
3. 설치 시 **"Add Python to PATH" 체크박스 반드시 선택!**
4. "Install Now" 클릭

#### 2. PostgreSQL 설치

**winget 사용 (권장)**
```powershell
# PowerShell을 관리자 권한으로 실행
winget install PostgreSQL.PostgreSQL
```

**수동 설치**
1. https://www.postgresql.org/download/windows/ 접속
2. "Download the installer" 클릭
3. 최신 버전 다운로드 및 설치
4. 설치 중 비밀번호 설정 (기억하기!)
5. 포트: 5432 (기본값)
6. "PostGIS" 추가 구성 요소 선택

#### 3. Redis 설치 (Memurai 사용)

**winget 사용 (권장)**
```powershell
winget install Memurai.Memurai-Developer
```

**수동 설치**
1. https://www.memurai.com/get-memurai 접속
2. "Download Memurai Developer" 클릭
3. 설치 완료 후 자동으로 서비스 시작됨

### 데이터베이스 설정

```powershell
# SQL Shell (psql) 실행
# 시작 메뉴에서 "SQL Shell (psql)" 검색

# Enter 키로 기본값 사용, 비밀번호만 입력
Server [localhost]:        # Enter
Database [postgres]:       # Enter
Port [5432]:              # Enter
Username [postgres]:      # Enter
Password:                 # 설치 시 설정한 비밀번호 입력

# 데이터베이스 생성
CREATE DATABASE ai_dispatch;
\c ai_dispatch
CREATE EXTENSION IF NOT EXISTS postgis;
\q
```

### 서버 실행

```powershell
# 프로젝트 폴더로 이동
cd C:\Users\YourName\ai-dispatch-system\backend

# 가상환경 생성
python -m venv venv

# 가상환경 활성화 (CMD)
venv\Scripts\activate.bat

# 또는 PowerShell
venv\Scripts\Activate.ps1

# 패키지 설치
pip install -r requirements.txt

# 서버 실행
python main.py
```

### 방화벽 설정

Windows 방화벽 알림이 뜨면:
- "프라이빗 네트워크 허용" 체크
- "공용 네트워크 허용" 체크 (선택사항)
- "허용" 클릭

---

## 🐧 Linux/macOS 실행 가이드

### Ubuntu/Debian

```bash
# 시스템 업데이트
sudo apt update

# Python 설치
sudo apt install python3.10 python3.10-venv python3-pip

# PostgreSQL + PostGIS 설치
sudo apt install postgresql postgresql-contrib postgis

# Redis 설치
sudo apt install redis-server

# PostgreSQL 시작
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Redis 시작
sudo systemctl start redis-server
sudo systemctl enable redis-server

# 데이터베이스 생성
sudo -u postgres psql
CREATE DATABASE ai_dispatch;
\c ai_dispatch
CREATE EXTENSION IF NOT EXISTS postgis;
\q

# 프로젝트 실행
cd ~/ai-dispatch-system/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

### macOS

```bash
# Homebrew 설치 (없는 경우)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Python 설치
brew install python@3.10

# PostgreSQL + PostGIS 설치
brew install postgresql@14 postgis

# Redis 설치
brew install redis

# PostgreSQL 시작
brew services start postgresql@14

# Redis 시작
brew services start redis

# 데이터베이스 생성
psql postgres
CREATE DATABASE ai_dispatch;
\c ai_dispatch
CREATE EXTENSION IF NOT EXISTS postgis;
\q

# 프로젝트 실행
cd ~/ai-dispatch-system/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

---

## 🔧 실행 옵션

### 개발 모드 (기본)

```bash
python main.py
```

- 자동 리로드 활성화
- 디버그 로그 출력
- 코드 변경 시 자동 재시작

### 프로덕션 모드

```bash
# Gunicorn 사용 (Linux/macOS)
pip install gunicorn
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000

# Uvicorn 직접 사용
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 백그라운드 실행

**Linux/macOS:**
```bash
nohup python main.py > server.log 2>&1 &
```

**Windows:**
```powershell
Start-Process python -ArgumentList "main.py" -WindowStyle Hidden
```

### 포트 변경

`.env` 파일 수정:
```bash
PORT=8080
```

또는 명령줄 인자:
```bash
uvicorn main:app --port 8080
```

---

## 🧪 실행 확인

### 1. 헬스 체크

```bash
curl http://localhost:8000/health
```

**응답:**
```json
{
  "status": "healthy",
  "app": "AI Dispatch System",
  "version": "1.0.0"
}
```

### 2. API 정보

```bash
curl http://localhost:8000/api/info
```

### 3. Python으로 테스트

```python
import requests

# 헬스 체크
response = requests.get('http://localhost:8000/health')
print(response.json())

# API 정보
response = requests.get('http://localhost:8000/api/info')
print(response.json())
```

### 4. 브라우저 테스트

다음 URL을 브라우저에서 열기:
- http://localhost:8000/docs

Swagger UI에서 "Try it out" 버튼으로 API 테스트 가능!

---

## 🔥 문제 해결

### 문제 1: "python: command not found"

**원인:** Python이 설치되지 않았거나 PATH에 없음

**해결:**
```bash
# Windows
py --version

# Linux/macOS
python3 --version
```

`python3` 명령어로 실행해보기

### 문제 2: "Address already in use"

**원인:** 8000 포트가 이미 사용 중

**해결:**
```bash
# 사용 중인 프로세스 확인 (Windows)
netstat -ano | findstr :8000

# 사용 중인 프로세스 확인 (Linux/macOS)
lsof -i :8000

# 프로세스 종료 (PID 확인 후)
# Windows
taskkill /F /PID <PID>

# Linux/macOS
kill -9 <PID>
```

또는 다른 포트 사용:
```bash
PORT=8080 python main.py
```

### 문제 3: "Connection refused" (PostgreSQL)

**원인:** PostgreSQL이 실행되지 않음

**해결:**
```bash
# Windows
# 서비스 앱에서 "postgresql" 검색 후 시작

# Linux
sudo systemctl start postgresql

# macOS
brew services start postgresql@14
```

### 문제 4: "Connection refused" (Redis)

**원인:** Redis가 실행되지 않음

**해결:**
```bash
# Windows (Memurai)
# 서비스 앱에서 "Memurai" 검색 후 시작

# Linux
sudo systemctl start redis-server

# macOS
brew services start redis
```

### 문제 5: 패키지 설치 실패

**원인:** pip 버전이 오래되었거나 권한 문제

**해결:**
```bash
# pip 업그레이드
python -m pip install --upgrade pip

# 패키지 재설치
pip install -r requirements.txt --no-cache-dir
```

### 문제 6: "No module named 'xxx'"

**원인:** 가상환경이 활성화되지 않음

**해결:**
```bash
# 가상환경 활성화 확인
# 프롬프트에 (venv) 표시 있는지 확인

# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate

# 패키지 재설치
pip install -r requirements.txt
```

---

## 📞 추가 도움

문제가 계속되면:
1. GitHub Issues: https://github.com/rpaakdi1-spec/ai-dispatch-system/issues
2. README 확인: https://github.com/rpaakdi1-spec/ai-dispatch-system#readme
3. 로그 파일 확인: `backend/server.log`

---

## 🎉 성공!

서버가 정상적으로 실행되었다면:
1. 📖 API 문서 읽기: http://localhost:8000/docs
2. 🧪 API 테스트하기
3. 📊 Excel 템플릿으로 데이터 입력하기
4. 🤖 AI 배차 실행하기

Happy Dispatching! 🚛
