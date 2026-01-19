#!/bin/bash
# ===================================================================
# AI Dispatch System - EXE 빌드 스크립트 (Linux/macOS)
# ===================================================================

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║         AI 배차 시스템 실행 파일 빌드                        ║"
echo "║         Building Executable for AI Dispatch System           ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# 스크립트 디렉토리로 이동
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo -e "${BLUE}[1/4] 환경 확인 중...${NC}"
echo ""

# Python 확인
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python3가 설치되어 있지 않습니다!${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Python 설치 확인${NC}"

echo ""
echo -e "${BLUE}[2/4] PyInstaller 설치 중...${NC}"

# 가상환경 활성화
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
fi

# PyInstaller 설치
if ! pip show pyinstaller &> /dev/null; then
    echo -e "${YELLOW}📦 PyInstaller를 설치합니다...${NC}"
    pip install pyinstaller
    if [ $? -ne 0 ]; then
        echo -e "${RED}❌ PyInstaller 설치 실패!${NC}"
        exit 1
    fi
fi

echo -e "${GREEN}✅ PyInstaller 준비 완료${NC}"

echo ""
echo -e "${BLUE}[3/4] 실행 파일 빌드 중... (5-10분 소요)${NC}"
echo ""

# 기존 빌드 폴더 삭제
rm -rf build dist

# PyInstaller로 빌드
pyinstaller --clean ai-dispatch.spec

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ 빌드 실패!${NC}"
    exit 1
fi

echo -e "${GREEN}✅ 빌드 완료${NC}"

echo ""
echo -e "${BLUE}[4/4] 결과 확인 중...${NC}"
echo ""

if [ -f "dist/ai-dispatch-system" ]; then
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo -e "${GREEN}✅ 실행 파일이 생성되었습니다!${NC}"
    echo ""
    echo -e "${BLUE}📂 위치: ${SCRIPT_DIR}/dist/ai-dispatch-system${NC}"
    echo -e "${BLUE}📦 크기: $(du -h dist/ai-dispatch-system | cut -f1)${NC}"
    echo ""
    echo -e "${YELLOW}💡 사용 방법:${NC}"
    echo "   1. ./dist/ai-dispatch-system 실행"
    echo "   2. 또는 다른 위치로 복사해서 사용"
    echo ""
    echo -e "${YELLOW}⚠️  참고사항:${NC}"
    echo "   - .env 파일을 실행 파일과 같은 폴더에 두세요"
    echo "   - PostgreSQL과 Redis가 설치되어 있어야 합니다"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
else
    echo -e "${RED}❌ 실행 파일 생성 실패!${NC}"
fi

echo ""
