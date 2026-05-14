#!/bin/bash
set -e

cd "$(dirname "$0")/.."
source install/setup.bash

PARAM_FILE="src/f1tenth_system/f1tenth_stack/config/f1tenth_online_async.yaml"

echo "=== SLAM Toolbox 실행 ==="
echo "사용 설정 파일: $PARAM_FILE"
echo
echo "RViz2에서 /map, /scan, /tf를 확인하세요."

ros2 launch slam_toolbox online_async_launch.py params_file:=$PARAM_FILE