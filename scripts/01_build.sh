#!/bin/bash
set -e

cd "$(dirname "$0")/.."

echo "=== F1TENTH 빌드 시작 ==="
colcon build --symlink-install

echo
echo "=== setup.bash 적용 ==="
source install/setup.bash

echo
echo "빌드 완료"
echo "다음부터는 아래 명령어로 환경을 적용하세요:"
echo "source install/setup.bash"