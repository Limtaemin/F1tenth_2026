#!/bin/bash
set -e

cd "$(dirname "$0")/.."
source install/setup.bash

echo "=== Stanley Avoidance 실행 ==="
echo "Stanley 경로추종 + LiDAR 기반 장애물 회피를 실행합니다."

ros2 launch stanley_avoidance stanley_avoidance_launch.py