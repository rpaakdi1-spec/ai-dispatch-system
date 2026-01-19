# 팔레트 기반 AI 냉동·냉장 배차 시스템

🚛 **AI-Based Dispatch System for Frozen/Refrigerated Cargo Transportation**

냉동/냉장 화물 운송을 위한 AI 기반 자동 배차 시스템입니다. 40대의 냉동/냉장 차량과 하루 평균 110건의 주문을 효율적으로 처리합니다.

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-green.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 📋 목차

- [핵심 기능](#-핵심-기능)
- [시스템 아키텍처](#-시스템-아키텍처)
- [시작하기](#-시작하기)
- [API 문서](#-api-문서)
- [엑셀 템플릿 사용법](#-엑셀-템플릿-사용법)
- [데이터 모델](#-데이터-모델)
- [기술 스택](#-기술-스택)
- [개발 로드맵](#-개발-로드맵)

## 🎯 핵심 기능

### ✅ 주요 목표
- **공차율 및 헛운행 최소화**: 빈 차량의 이동 거리를 최소화
- **온도대별 자동 매칭**: 냉동/냉장/상온 화물에 맞는 차량 자동 배정
- **팔레트 단위 적재 관리**: 톤수가 아닌 팔레트 개수로 용량 최적화
- **의사결정 시간 70% 단축**: 배차 담당자의 업무 시간 대폭 단축
- **실시간 GPS 모니터링**: 삼성 UVIS 연동으로 실시간 위치 추적

### 🌡️ 온도대 관리
- **냉동 (Frozen)**: -18°C ~ -25°C
- **냉장 (Chilled)**: 0°C ~ 6°C
- **상온 (Ambient)**: 실온

### 🤖 AI 배차 로직

#### Hard Constraints (절대 위반 불가)
- ✅ 온도대 매칭 (냉동 화물 → 냉동 차량만)
- ✅ 팔레트 수 초과 금지
- ✅ 중량 초과 금지
- ✅ 타임 윈도우 준수
- ✅ 기사 근무시간 준수

#### Soft Constraints (최적화 목표)
- 📉 공차거리 최소화
- 📉 총 주행거리 최소화
- ⚖️ 차량/기사 간 업무 균형

## 🏗️ 시스템 아키텍처

```
┌─────────────────────────────────────────────────┐
│          Frontend (React) - 예정               │
│  - 주문 관리 화면                                │
│  - AI 배차 화면                                  │
│  - 실시간 모니터링 대시보드                        │
└────────────────┬────────────────────────────────┘
                 │ HTTP/WebSocket
┌────────────────▼────────────────────────────────┐
│              Backend (FastAPI)                   │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐      │
│  │ Routes   │  │ Services │  │ Models   │      │
│  └──────────┘  └──────────┘  └──────────┘      │
└─────┬──────────────┬──────────────┬─────────────┘
      │              │              │
      ▼              ▼              ▼
┌──────────┐  ┌──────────┐  ┌──────────┐
│PostgreSQL│  │  Redis   │  │UVIS API  │
│(PostGIS) │  │  Cache   │  │   GPS    │
└──────────┘  └──────────┘  └──────────┘
```

## 📁 프로젝트 구조

```
webapp/
├── backend/                 # FastAPI 백엔드
│   ├── config/             # 설정 파일
│   │   ├── settings.py     # 환경 변수 설정
│   │   ├── database.py     # PostgreSQL 연결
│   │   └── redis.py        # Redis 연결
│   ├── models/             # 데이터베이스 모델
│   │   ├── vehicle.py      # 차량 모델
│   │   ├── client.py       # 거래처 모델
│   │   ├── order.py        # 주문 모델
│   │   └── gps_log.py      # GPS 로그
│   ├── routes/             # API 라우터
│   ├── services/           # 비즈니스 로직
│   │   ├── geocoding.py    # 네이버 지도 지오코딩
│   │   ├── routing.py      # 경로 계산
│   │   ├── vrp_solver.py   # OR-Tools 배차 로직
│   │   └── uvis.py         # UVIS GPS 연동
│   ├── utils/              # 유틸리티
│   │   └── excel_processor.py
│   ├── main.py             # FastAPI 메인
│   └── requirements.txt    # Python 패키지
│
├── data/                   # 데이터 디렉토리
│   ├── templates/          # 엑셀 템플릿
│   │   ├── clients_template.xlsx
│   │   ├── orders_template.xlsx
│   │   └── vehicles_template.xlsx
│   └── uploads/            # 업로드 파일
│
├── frontend/               # React 프론트엔드 (예정)
│
└── docs/                   # 문서
```

## 🚀 시작하기

### 필수 요구사항

- **Python** 3.10 이상
- **PostgreSQL** 14 이상 (PostGIS 확장 포함)
- **Redis** 7 이상 (Windows: [Memurai](https://www.memurai.com/) 권장)
- **Node.js** 18 이상 (프론트엔드, 예정)

### 1. 저장소 클론

```bash
git clone <repository-url>
cd webapp
```

### 2. 백엔드 설정

#### 가상환경 생성 및 활성화

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate
```

#### 패키지 설치

```bash
pip install -r requirements.txt
```

#### 환경 변수 설정

```bash
# .env.example을 .env로 복사
cp .env.example .env

# .env 파일을 편집하여 실제 값 입력
# 특히 다음 항목들은 반드시 설정:
# - DATABASE_URL
# - NAVER_MAP_CLIENT_ID
# - NAVER_MAP_CLIENT_SECRET
# - UVIS_API_KEY (선택사항)
```

### 3. 데이터베이스 설정

#### PostgreSQL 설치 및 실행

**Windows:**
```powershell
# PostgreSQL 설치 (winget 사용)
winget install PostgreSQL.PostgreSQL

# 또는 공식 사이트에서 다운로드
# https://www.postgresql.org/download/windows/
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib postgis
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

#### 데이터베이스 생성

```bash
# PostgreSQL에 접속
psql -U postgres

# 데이터베이스 생성
CREATE DATABASE ai_dispatch;

# PostGIS 확장 활성화
\c ai_dispatch
CREATE EXTENSION IF NOT EXISTS postgis;

# 종료
\q
```

### 4. Redis 설정

**Windows (Memurai 사용):**
```powershell
# Memurai 설치
winget install Memurai.Memurai-Developer
```

**Linux:**
```bash
sudo apt install redis-server
sudo systemctl start redis-server
sudo systemctl enable redis-server
```

### 5. 서버 실행

```bash
cd backend
python main.py
```

서버가 `http://localhost:8000`에서 실행됩니다.

### 6. API 문서 확인

브라우저에서 다음 주소를 엽니다:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📖 API 문서

### 주요 엔드포인트

#### 기본 정보
- `GET /` - API 루트
- `GET /health` - 헬스 체크
- `GET /api/info` - API 정보 및 설정

#### 차량 관리 (예정)
- `GET /api/vehicles` - 차량 목록 조회
- `POST /api/vehicles` - 차량 등록
- `GET /api/vehicles/{vehicle_id}` - 차량 상세 조회
- `PUT /api/vehicles/{vehicle_id}` - 차량 정보 수정
- `DELETE /api/vehicles/{vehicle_id}` - 차량 삭제

#### 거래처 관리 (예정)
- `GET /api/clients` - 거래처 목록 조회
- `POST /api/clients` - 거래처 등록
- `POST /api/clients/upload` - 엑셀 일괄 업로드
- `GET /api/clients/{client_id}` - 거래처 상세 조회

#### 주문 관리 (예정)
- `GET /api/orders` - 주문 목록 조회
- `POST /api/orders` - 주문 등록
- `POST /api/orders/upload` - 엑셀 일괄 업로드

#### AI 배차 (예정)
- `POST /api/dispatch/optimize` - 배차 최적화 실행
- `GET /api/dispatch/routes` - 배차 결과 조회
- `POST /api/dispatch/assign` - 배차 확정

#### GPS 추적 (예정)
- `GET /api/gps/vehicles/{vehicle_id}` - 차량 위치 조회
- `GET /api/gps/vehicles` - 전체 차량 위치 조회
- `GET /api/gps/events` - GPS 이벤트 조회

## 📊 엑셀 템플릿 사용법

엑셀 템플릿 파일은 `data/templates/` 디렉토리에 있습니다.

### 1. 거래처 마스터 업로드

**파일**: `clients_template.xlsx`

| 필드 | 설명 | 예시 |
|------|------|------|
| 거래처코드 | 고유 ID | CUST-0001 |
| 거래처명 | 상호명 | (주)서울냉동 |
| 구분 | 상차/하차/양쪽 | 양쪽 |
| 주소 | 기본 주소 | 서울 송파구 문정동 123 |
| 상차가능시작 | HH:MM 형식 | 09:00 |
| 상차가능종료 | HH:MM 형식 | 17:00 |
| 지게차유무 | Y/N | Y |
| 대형차진입 | Y/N | Y |

### 2. 주문 업로드

**파일**: `orders_template.xlsx`

| 필드 | 설명 | 예시 |
|------|------|------|
| 주문번호 | 고유 ID | ORD-001 |
| 상차거래처코드 | 상차 거래처 | CUST-0001 |
| 하차거래처코드 | 하차 거래처 | CUST-0100 |
| 온도대 | 냉동/냉장/상온 | 냉동 |
| 팔레트수 | 개수 | 6 |
| 중량(kg) | 킬로그램 | 3000 |

### 3. 차량 마스터 업로드

**파일**: `vehicles_template.xlsx`

| 필드 | 설명 | 예시 |
|------|------|------|
| 차량코드 | 고유 ID | TRUCK-001 |
| UVIS단말기ID | UVIS 매핑 | UVIS-DVC-12345 |
| 차량타입 | 냉동/냉장/겸용/상온 | 냉동 |
| 최대팔레트 | 개수 | 16 |
| 최대중량(kg) | 킬로그램 | 10000 |

## 📊 데이터 모델

### Vehicle (차량)
```json
{
  "vehicle_id": "TRUCK-001",
  "vehicle_type": "frozen",
  "max_pallets": 16,
  "max_weight_kg": 10000,
  "temperature_range_min": -25.0,
  "temperature_range_max": -15.0
}
```

### Client (거래처)
```json
{
  "client_id": "CUST-0001",
  "client_name": "(주)서울냉동",
  "service_type": "both",
  "address": "서울 송파구 문정동 123",
  "latitude": 37.5665,
  "longitude": 126.9780,
  "has_forklift": true
}
```

### Order (주문)
```json
{
  "order_id": "ORD-001",
  "pickup_client_id": "CUST-0001",
  "delivery_client_id": "CUST-0100",
  "temperature_type": "frozen",
  "required_pallets": 6,
  "weight_kg": 3000,
  "status": "pending"
}
```

## 🛠️ 기술 스택

### Backend
- **Framework**: FastAPI
- **Database**: PostgreSQL + PostGIS
- **Cache**: Redis
- **Optimization**: Google OR-Tools
- **Map API**: Naver Maps (Geocoding, Directions)
- **GPS**: Samsung UVIS API

### Frontend (예정)
- **Framework**: React 18
- **UI Library**: Ant Design
- **Map**: Naver Maps JavaScript API
- **Real-time**: Socket.IO

### DevOps
- **Cloud**: AWS / Naver Cloud Platform
- **CI/CD**: GitHub Actions
- **Monitoring**: Prometheus + Grafana

## 📈 예상 성과

| 지표 | 도입 전 | 목표 |
|------|---------|------|
| 배차 소요시간 | 2~3시간 | 30분 이내 |
| 공차율 | 30% | 15% 이하 |
| 평균 적재율 | 60% | 80% 이상 |
| 정시 도착률 | 85% | 95% 이상 |
| 온도 이탈 사고 | 월 5건 | 월 1건 이하 |

## 📋 개발 로드맵

### ✅ Phase 1: PoC (4주) - 진행 중
- [x] 프로젝트 구조 설정
- [x] 데이터베이스 모델 설계
- [x] 기본 설정 및 의존성 관리
- [x] 엑셀 템플릿 생성
- [x] 지오코딩 서비스 구현
- [x] 경로 계산 서비스 구현
- [x] VRP 솔버 구현
- [ ] API 라우터 구현
- [ ] 간단한 웹 UI

### 📅 Phase 2: Pilot (8주)
- [ ] 실제 규모 적용 (40대/110건)
- [ ] AI 배차 고도화
- [ ] 실시간 대시보드
- [ ] UVIS 전체 연동
- [ ] 통계 리포트

### 📅 Phase 3: Production
- [ ] 동적 재배차
- [ ] ETA 예측 ML 모델
- [ ] 모바일 앱 (기사용)
- [ ] 고객용 추적 시스템

## 🔐 보안 고려사항

- ✅ API 키는 환경 변수로 관리 (`.env`)
- ✅ Git에 민감 정보 커밋 금지 (`.gitignore`)
- ✅ HTTPS 통신 필수 (프로덕션)
- ✅ JWT 기반 인증 (구현 예정)
- ✅ CORS 설정으로 허용 도메인 제한

## 📄 라이선스

MIT License

## 🤝 기여

기여를 환영합니다! Pull Request를 제출해주세요.

## 📞 문의

프로젝트 관련 문의사항이 있으시면 이슈를 등록해주세요.

---

**Made with ❤️ for efficient cold chain logistics**
