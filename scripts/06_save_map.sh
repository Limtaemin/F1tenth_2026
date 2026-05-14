#!/bin/bash
set -e

cd "$(dirname "$0")/.."
source install/setup.bash

mkdir -p maps/saved

MAP_NAME=${1:-maps/saved/f1tenth_map}

echo "=== 맵 저장 ==="
echo "저장 경로: $MAP_NAME"
echo
echo "생성 예상 파일:"
echo "${MAP_NAME}.yaml"
echo "${MAP_NAME}.pgm"
echo

ros2 run nav2_map_server map_saver_cli -f "$MAP_NAME"