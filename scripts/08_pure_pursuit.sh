#!/bin/bash
set -e

cd "$(dirname "$0")/.."
source install/setup.bash

echo "=== Pure Pursuit 경로추종 실행 ==="
echo "raceline/waypoint를 따라 주행합니다."

ros2 launch pure_pursuit pure_pursuit_launch.py