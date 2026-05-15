# 스크립트 내용

이 페이지는 `scripts/` 폴더에 있는 실행 스크립트 내용을 모아 보여줍니다.

수정 후에는 아래 명령으로 이 문서를 다시 생성할 수 있습니다.

```bash
python3 generate_scripts_doc.py
```


## `scripts/01_build.sh`

```bash
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
```


## `scripts/02_bringup.sh`

```bash
#!/bin/bash
set -e

cd "$(dirname "$0")/.."
source install/setup.bash

echo "=== F1TENTH Bringup 실행 ==="
echo "LiDAR, VESC, mux, teleop 등 기본 하드웨어 노드를 실행합니다."
ros2 launch f1tenth_stack bringup_launch.py
```


## `scripts/03_web_dashboard.sh`

```bash
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
```


## `scripts/04_rviz.sh`

```bash
#!/bin/bash
set -e

cd "$(dirname "$0")/.."
source install/setup.bash

echo "=== RViz2 실행 ==="
rviz2
```


## `scripts/05_slam_start.sh`

```bash
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
```


## `scripts/06_save_map.sh`

```bash
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
```


## `scripts/07_localization.sh`

```bash
#!/bin/bash
set -e

cd "$(dirname "$0")/.."
source install/setup.bash

echo "=== Particle Filter 위치추정 실행 ==="
echo "저장된 맵에서 차량 위치를 추정합니다."
echo "RViz2에서 2D Pose Estimate로 초기 위치를 잡아주세요."

ros2 launch particle_filter localize_launch.py
```


## `scripts/08_pure_pursuit.sh`

```bash
#!/bin/bash
set -e

cd "$(dirname "$0")/.."
source install/setup.bash

echo "=== Pure Pursuit 경로추종 실행 ==="
echo "raceline/waypoint를 따라 주행합니다."

ros2 launch pure_pursuit pure_pursuit_launch.py
```


## `scripts/09_stanley_avoidance.sh`

```bash
#!/bin/bash
set -e

cd "$(dirname "$0")/.."
source install/setup.bash

echo "=== Stanley Avoidance 실행 ==="
echo "Stanley 경로추종 + LiDAR 기반 장애물 회피를 실행합니다."

ros2 launch stanley_avoidance stanley_avoidance_launch.py
```
