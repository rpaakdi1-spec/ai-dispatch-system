# 🚀 실행 파일 사용 가이드

AI 배차 시스템을 실행하는 다양한 방법을 안내합니다.

## 📋 목차
1. [간편 실행 (권장)](#간편-실행-권장)
2. [GUI 런처](#gui-런처)
3. [실행 파일 빌드](#실행-파일-빌드)
4. [실행 방법 비교](#실행-방법-비교)

---

## 🎯 간편 실행 (권장)

### Windows 사용자

**더블클릭으로 실행**

1. `backend` 폴더로 이동
2. `start.bat` 파일을 더블클릭
3. 자동으로 환경 설정 및 서버 시작!

```
backend/
  └── start.bat  ← 이 파일을 더블클릭!
```

**또는 명령 프롬프트에서:**
```cmd
cd backend
start.bat
```

### Linux/macOS 사용자

**터미널에서 실행:**
```bash
cd backend
./start.sh
```

**또는 더블클릭 (권한 설정 필요):**
```bash
chmod +x start.sh
./start.sh
```

---

## 🖼️ GUI 런처

그래픽 인터페이스로 서버를 편리하게 관리할 수 있습니다!

### 특징
- ✅ 버튼 클릭으로 서버 시작/종료
- 📊 실시간 로그 확인
- 🌐 API 문서 바로 열기
- 🎨 깔끔한 인터페이스

### Windows 실행

**방법 1: 더블클릭**
```
backend/
  └── launcher.bat  ← 이 파일을 더블클릭!
```

**방법 2: 명령 프롬프트**
```cmd
cd backend
launcher.bat
```

### Linux/macOS 실행

```bash
cd backend
./launcher.sh
```

### GUI 런처 사용법

1. **"▶ 서버 시작"** 버튼 클릭
2. 서버가 시작되면 상태가 "🟢 서버 실행 중"으로 변경
3. **"📖 API 문서"** 버튼으로 브라우저에서 API 확인
4. 로그 창에서 실시간 서버 상태 모니터링
5. **"⬛ 서버 종료"** 버튼으로 안전하게 종료

---

## 📦 실행 파일 빌드 (.exe 만들기)

독립 실행 파일(.exe)을 만들어서 Python 없이도 실행할 수 있습니다!

### Windows에서 EXE 빌드

**방법 1: 더블클릭**
```
backend/
  └── build-exe.bat  ← 이 파일을 더블클릭!
```

**방법 2: 명령 프롬프트**
```cmd
cd backend
build-exe.bat
```

**빌드 과정 (5-10분 소요)**
1. PyInstaller 설치
2. 의존성 패키지 수집
3. 실행 파일 생성
4. 완료!

**결과물:**
```
backend/dist/
  └── ai-dispatch-system.exe  ← 실행 파일!
```

### Linux/macOS에서 빌드

```bash
cd backend
./build-exe.sh
```

**결과물:**
```
backend/dist/
  └── ai-dispatch-system  ← 실행 파일!
```

### 실행 파일 사용법

1. `dist/ai-dispatch-system.exe` (또는 `ai-dispatch-system`) 복사
2. `.env` 파일도 같은 폴더에 복사
3. 실행 파일 더블클릭 또는:

**Windows:**
```cmd
ai-dispatch-system.exe
```

**Linux/macOS:**
```bash
./ai-dispatch-system
```

### 주의사항

⚠️ 실행 파일을 사용해도 다음이 필요합니다:
- ✅ PostgreSQL 설치 및 실행
- ✅ Redis 설치 및 실행
- ✅ `.env` 파일 (실행 파일과 같은 폴더)

---

## 📊 실행 방법 비교

| 방법 | 장점 | 단점 | 추천 대상 |
|------|------|------|-----------|
| **start.bat/sh** | • 간단하고 빠름<br>• 자동 환경 설정<br>• 코드 수정 가능 | • Python 필요 | 개발자, 일반 사용자 |
| **GUI 런처** | • 시각적으로 편리<br>• 실시간 로그 확인<br>• 버튼으로 제어 | • Python 필요 | GUI를 선호하는 사용자 |
| **실행 파일 (.exe)** | • Python 불필요<br>• 배포 용이<br>• 독립 실행 | • 빌드 시간 소요<br>• 파일 크기 큼 (50-100MB) | 최종 사용자, 배포용 |

---

## 🛠️ 고급 사용

### 백그라운드 실행 (Windows)

```cmd
start /B python main.py
```

### 백그라운드 실행 (Linux/macOS)

```bash
nohup python main.py > server.log 2>&1 &
```

### 프로덕션 모드 실행

```bash
# Gunicorn 사용 (Linux/macOS)
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker

# Uvicorn 직접 사용
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 서비스로 등록 (Windows)

NSSM (Non-Sucking Service Manager) 사용:
```cmd
nssm install AIDispatch "C:\path\to\python.exe" "C:\path\to\main.py"
nssm start AIDispatch
```

### 서비스로 등록 (Linux - systemd)

`/etc/systemd/system/ai-dispatch.service` 파일 생성:
```ini
[Unit]
Description=AI Dispatch System
After=network.target postgresql.service redis.service

[Service]
Type=simple
User=www-data
WorkingDirectory=/path/to/backend
Environment="PATH=/path/to/venv/bin"
ExecStart=/path/to/venv/bin/python main.py
Restart=always

[Install]
WantedBy=multi-user.target
```

서비스 시작:
```bash
sudo systemctl daemon-reload
sudo systemctl enable ai-dispatch
sudo systemctl start ai-dispatch
```

---

## 🔍 실행 확인

서버가 정상적으로 시작되었는지 확인:

### 1. 로그 확인
```
✅ AI Dispatch System started on http://0.0.0.0:8000
📖 API Documentation available at http://0.0.0.0:8000/docs
```

### 2. 브라우저 테스트
- http://localhost:8000
- http://localhost:8000/health
- http://localhost:8000/docs

### 3. 명령줄 테스트
```bash
curl http://localhost:8000/health
```

**성공 응답:**
```json
{
  "status": "healthy",
  "app": "AI Dispatch System",
  "version": "1.0.0"
}
```

---

## 🎯 실행 파일 선택 가이드

### 개발/테스트 중이라면?
👉 **start.bat/sh 사용** (가장 간단하고 빠름)

### GUI를 선호한다면?
👉 **launcher.bat/sh 사용** (시각적 제어)

### 최종 사용자에게 배포한다면?
👉 **실행 파일 빌드** (Python 설치 불필요)

### 서버에 배포한다면?
👉 **systemd 서비스** (자동 시작/재시작)

---

## 💡 팁

1. **빠른 재시작**: Ctrl+C로 종료 후 다시 실행
2. **포트 변경**: `.env` 파일에서 `PORT=8080`
3. **로그 저장**: 출력을 파일로 리다이렉트
   ```bash
   python main.py > server.log 2>&1
   ```
4. **자동 재시작**: 개발 모드에서는 코드 변경 시 자동 재시작됨

---

## 📞 문제 해결

문제가 발생하면:
1. 로그 확인
2. PostgreSQL/Redis 실행 상태 확인
3. `.env` 파일 설정 확인
4. [HOW_TO_RUN.md](HOW_TO_RUN.md) 참조

---

**Happy Dispatching! 🚛**
