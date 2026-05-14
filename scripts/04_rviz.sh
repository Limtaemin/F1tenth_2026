#!/bin/bash
set -e

cd "$(dirname "$0")/.."
source install/setup.bash

echo "=== RViz2 실행 ==="
rviz2