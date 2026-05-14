#!/bin/bash
set -e

cd "$(dirname "$0")/.."
source install/setup.bash

echo "=== 웹 대시보드 실행 ==="
echo "브라우저에서 아래 주소로 접속하세요:"
echo "http://localhost:5000"
echo
echo "다른 기기에서 접속하려면 이 PC의 IP 주소를 확인하세요:"
echo "hostname -I"
echo

python3 mission_control/dashboard.py