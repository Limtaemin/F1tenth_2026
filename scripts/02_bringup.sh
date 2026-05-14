#!/bin/bash
set -e

cd "$(dirname "$0")/.."
source install/setup.bash

echo "=== F1TENTH Bringup 실행 ==="
echo "LiDAR, VESC, mux, teleop 등 기본 하드웨어 노드를 실행합니다."
ros2 launch f1tenth_stack bringup_launch.py