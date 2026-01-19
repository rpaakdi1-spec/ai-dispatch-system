#!/bin/bash
# ===================================================================
# AI Dispatch System - Linux/macOS 실행 스크립트
# ===================================================================

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║         AI 배차 시스템 자동 실행 스크립트                    ║"
echo "║         AI Dispatch System Auto Launcher                     ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# 스크립트 디렉토리로 이동
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo -e "${BLUE}[1/5] 환경 확인 중...${NC}"
echo ""

# Python 확인
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python3가 설치되어 있지 않습니다!${NC}"
    echo ""
    echo "Python 3.10 이상을 설치해주세요:"
    echo "  Ubuntu/Debian: sudo apt install python3.10 python3-pip python3-venv"
    echo "  macOS: brew install python@3.10"
    exit 1
fi

echo -e "${GREEN}✅ Python 설치 확인${NC}"
python3 --version

echo ""
echo -e "${BLUE}[2/5] 가상환경 확인 중...${NC}"

# 가상환경이 없으면 생성
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}📦 가상환경을 생성합니다...${NC}"
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo -e "${RED}❌ 가상환경 생성 실패!${NC}"
        exit 1
    fi
    echo -e "${GREEN}✅ 가상환경 생성 완료${NC}"
else
    echo -e "${GREEN}✅ 가상환경 존재 확인${NC}"
fi

echo ""
echo -e "${BLUE}[3/5] 가상환경 활성화 중...${NC}"

# 가상환경 활성화
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo -e "${RED}❌ 가상환경 활성화 실패!${NC}"
    exit 1
fi

echo -e "${GREEN}✅ 가상환경 활성화 완료${NC}"

echo ""
echo -e "${BLUE}[4/5] 필수 패키지 확인 중...${NC}"

# requirements.txt가 있으면 패키지 설치
if [ -f "requirements.txt" ]; then
    # 패키지가 이미 설치되어 있는지 확인
    if ! pip show fastapi &> /dev/null; then
        echo -e "${YELLOW}📦 필수 패키지를 설치합니다... (2-3분 소요)${NC}"
        pip install -q -r requirements.txt
        if [ $? -ne 0 ]; then
            echo -e "${RED}❌ 패키지 설치 실패!${NC}"
            echo ""
            echo "다음 명령어로 수동 설치해주세요:"
            echo "  pip install -r requirements.txt"
            exit 1
        fi
        echo -e "${GREEN}✅ 패키지 설치 완료${NC}"
    else
        echo -e "${GREEN}✅ 패키지 설치 확인${NC}"
    fi
fi

echo ""
echo -e "${BLUE}[5/5] 서버 시작 중...${NC}"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo -e "${GREEN}🚀 AI 배차 시스템을 시작합니다...${NC}"
echo ""
echo -e "${BLUE}📖 API 문서: http://localhost:8000/docs${NC}"
echo -e "${BLUE}💚 헬스 체크: http://localhost:8000/health${NC}"
echo ""
echo -e "${YELLOW}⚠️  서버를 종료하려면 Ctrl+C 를 누르세요${NC}"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 서버 실행
python main.py

# 서버 종료 시
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo -e "${GREEN}👋 서버가 종료되었습니다.${NC}"
echo ""
