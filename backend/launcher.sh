#!/bin/bash
# GUI 런처 실행 스크립트

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# 가상환경 활성화
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
fi

# GUI 런처 실행
python3 launcher.py
