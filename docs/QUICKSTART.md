# 빠른 시작 가이드 (Quick Start Guide)

이 문서는 AI 배차 시스템을 빠르게 설치하고 실행하는 방법을 안내합니다.

## 📋 사전 요구사항

다음 소프트웨어가 설치되어 있어야 합니다:

- Python 3.10 이상
- PostgreSQL 14 이상
- Redis 7 이상
- Git

## 🚀 빠른 설치 (5분 완성)

### 1단계: 저장소 클론 및 이동

```bash
git clone <repository-url>
cd webapp/backend
```

### 2단계: Python 가상환경 생성

**Windows:**
```powershell
python -m venv venv
venv\Scripts\activate
```

**Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3단계: 패키지 설치

```bash
pip install -r requirements.txt
```

### 4단계: 환경 변수 설정

`.env` 파일이 이미 생성되어 있습니다. 필요한 경우 수정하세요:

```bash
# Windows
notepad .env

# Linux/macOS
nano .env
```

**필수 설정 항목:**
- `DATABASE_URL`: PostgreSQL 연결 문자열
- `NAVER_MAP_CLIENT_ID`: 네이버 지도 API 클라이언트 ID (이미 설정됨)
- `NAVER_MAP_CLIENT_SECRET`: 네이버 지도 API 시크릿 (이미 설정됨)

### 5단계: PostgreSQL 데이터베이스 생성

```bash
# PostgreSQL에 접속
psql -U postgres

# 명령어 실행
CREATE DATABASE ai_dispatch;
\c ai_dispatch
CREATE EXTENSION IF NOT EXISTS postgis;
\q
```

### 6단계: Redis 시작

**Windows (Memurai):**
```powershell
# Memurai가 이미 설치되어 있다면 자동으로 실행됩니다
# 서비스 시작 확인:
Get-Service Memurai
```

**Linux:**
```bash
sudo systemctl start redis-server
sudo systemctl status redis-server
```

### 7단계: 서버 실행

```bash
python main.py
```

서버가 `http://localhost:8000`에서 실행됩니다!

## ✅ 설치 확인

브라우저에서 다음 URL을 열어 설치를 확인하세요:

1. **API 루트**: http://localhost:8000/
2. **헬스 체크**: http://localhost:8000/health
3. **API 문서**: http://localhost:8000/docs

## 📝 다음 단계

1. **Excel 템플릿 다운로드**
   - 거래처: `data/templates/clients_template.xlsx`
   - 주문: `data/templates/orders_template.xlsx`
   - 차량: `data/templates/vehicles_template.xlsx`

2. **데이터 입력**
   - 템플릿에 실제 데이터 입력
   - API를 통해 업로드 (구현 예정)

3. **AI 배차 실행**
   - 주문 데이터 준비
   - 배차 최적화 API 호출
   - 결과 확인

## 🐛 문제 해결

### PostgreSQL 연결 오류
```
Error: could not connect to server
```

**해결책:**
- PostgreSQL이 실행 중인지 확인
- `.env` 파일의 `DATABASE_URL`이 올바른지 확인
- 데이터베이스 `ai_dispatch`가 생성되었는지 확인

### Redis 연결 오류
```
Error: Error connecting to Redis
```

**해결책:**
- Redis 서버가 실행 중인지 확인
- 포트 6379가 사용 가능한지 확인

### 패키지 설치 오류
```
Error: Failed building wheel for xxx
```

**해결책:**
- Python 버전 확인 (3.10 이상 필요)
- `pip install --upgrade pip` 실행
- 개별 패키지 수동 설치: `pip install <package-name>`

### 네이버 지도 API 오류
```
Error: Invalid API key
```

**해결책:**
- 네이버 클라우드 플랫폼에서 API 키 발급
- `.env` 파일에 올바른 키 입력
- API 사용량 제한 확인

## 📚 추가 문서

- [README.md](../README.md) - 전체 프로젝트 개요
- [API 문서](http://localhost:8000/docs) - Swagger UI
- [데이터 모델](../README.md#-데이터-모델) - 데이터 구조 설명

## 💬 도움말

문제가 해결되지 않으면 GitHub Issues에 문의하세요.

---

**Happy Dispatching! 🚛**
