#!/bin/bash
set -e

cd "$(dirname "$0")/.."
source install/setup.bash

echo "=== Particle Filter 위치추정 실행 ==="
echo "저장된 맵에서 차량 위치를 추정합니다."
echo "RViz2에서 2D Pose Estimate로 초기 위치를 잡아주세요."

ros2 launch particle_filter localize_launch.py