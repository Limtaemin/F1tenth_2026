# 03. SLAM 맵 생성

이 문서는 F1TENTH 차량에서 LiDAR와 odom을 이용해 SLAM 맵을 생성하고 저장하는 방법을 설명한다.

SLAM은 `Simultaneous Localization and Mapping`의 약자로, 차량이 움직이면서 주변 환경의 지도를 만들고 동시에 자기 위치를 추정하는 과정이다.

---

## 1. 이 문서의 목표

이 문서에서는 다음 내용을 다룬다.

```text
1. SLAM 실행 전 확인할 것
2. bringup 실행
3. RViz2 실행
4. SLAM 실행
5. 차량을 천천히 움직이며 맵 생성
6. 맵 저장
7. 저장된 map 파일 확인
8. 자주 생기는 문제 해결
2. SLAM에서 중요한 토픽과 frame

SLAM이 정상 동작하려면 아래 정보가 필요하다.

이름역할
/scanLiDAR 스캔 데이터
/odom차량 이동량 정보
/tf좌표계 변환
maps/생성되는 지도 좌표계
odomodometry 좌표계
base_link차량 중심 좌표계
laserLiDAR 센서 좌표계

일반적인 관계는 다음과 같다.

map
 ↓
odom
 ↓
base_link
 ↓
laser

SLAM이 잘 되려면 /scan, /odom, /tf가 모두 정상이어야 한다.

3. 실행 전 안전 체크리스트

실차에서 SLAM을 실행하기 전 아래를 확인한다.

[ ] 차량 배터리가 충분한가?
[ ] VESC가 정상 연결되어 있는가?
[ ] LiDAR가 정상 연결되어 있는가?
[ ] 주변에 사람이 없는가?
[ ] 차량을 천천히 움직일 공간이 있는가?
[ ] 긴급 정지 방법을 알고 있는가?
[ ] 최대 속도를 낮게 제한했는가?

처음 SLAM을 할 때는 빠르게 주행하지 않는다.

맵은 천천히, 부드럽게 움직일수록 잘 만들어진다.

4. 실행 순서 요약

SLAM 맵 생성의 기본 순서는 다음과 같다.

1. ROS2 환경 적용
2. 차량 bringup 실행
3. RViz2 실행
4. SLAM 실행
5. 수동 조작으로 차량 이동
6. 맵 상태 확인
7. 맵 저장

스크립트 기준으로는 아래 순서다.

cd ~/race_stack/f1tenth

source /opt/ros/foxy/setup.bash
source install/setup.bash

bash scripts/02_bringup.sh

다른 터미널에서 RViz2를 실행한다.

cd ~/race_stack/f1tenth

source /opt/ros/foxy/setup.bash
source install/setup.bash

bash scripts/04_rviz.sh

다른 터미널에서 SLAM을 실행한다.

cd ~/race_stack/f1tenth

source /opt/ros/foxy/setup.bash
source install/setup.bash

bash scripts/05_slam_start.sh

맵 저장은 아래 명령을 사용한다.

cd ~/race_stack/f1tenth

source /opt/ros/foxy/setup.bash
source install/setup.bash

bash scripts/06_save_map.sh maps/saved/my_map
5. 터미널 구성 추천

SLAM 실험 중에는 터미널을 여러 개 열어두는 것이 좋다.

터미널 1: bringup
cd ~/race_stack/f1tenth

source /opt/ros/foxy/setup.bash
source install/setup.bash

bash scripts/02_bringup.sh
터미널 2: RViz2
cd ~/race_stack/f1tenth

source /opt/ros/foxy/setup.bash
source install/setup.bash

bash scripts/04_rviz.sh
터미널 3: SLAM
cd ~/race_stack/f1tenth

source /opt/ros/foxy/setup.bash
source install/setup.bash

bash scripts/05_slam_start.sh
터미널 4: 웹 대시보드 또는 수동 조작
cd ~/race_stack/f1tenth

source /opt/ros/foxy/setup.bash
source install/setup.bash

python3 mission_control/dashboard.py

브라우저 접속:

http://localhost:5000
6. bringup 실행

먼저 차량 하드웨어 bringup을 실행한다.

cd ~/race_stack/f1tenth

source /opt/ros/foxy/setup.bash
source install/setup.bash

bash scripts/02_bringup.sh

bringup이 정상 실행되면 아래 토픽들이 나와야 한다.

ros2 topic list

확인할 주요 토픽:

/scan
/odom
/tf
/tf_static
/drive
/webop

LiDAR 확인:

ros2 topic echo /scan

odom 확인:

ros2 topic echo /odom

TF 확인:

ros2 run tf2_tools view_frames
7. RViz2 실행

SLAM 결과를 확인하려면 RViz2를 실행한다.

cd ~/race_stack/f1tenth

source /opt/ros/foxy/setup.bash
source install/setup.bash

bash scripts/04_rviz.sh

RViz2에서 확인할 항목:

Fixed Frame: map 또는 odom
LaserScan: /scan
Map: /map
TF: map, odom, base_link, laser
RobotModel 또는 TF 표시

처음에는 /map이 없거나 비어 있을 수 있다.

SLAM이 실행되고 차량이 움직이기 시작하면 /map이 생성된다.

8. SLAM 실행

SLAM은 아래 스크립트로 실행한다.

cd ~/race_stack/f1tenth

source /opt/ros/foxy/setup.bash
source install/setup.bash

bash scripts/05_slam_start.sh

이 스크립트는 보통 slam_toolbox의 online async launch를 실행한다.

직접 실행하는 형태는 대략 아래와 비슷하다.

ros2 launch slam_toolbox online_async_launch.py

이 레포에서는 설정 파일을 함께 넘길 수 있다.

ros2 launch slam_toolbox online_async_launch.py params_file:=src/f1tenth_system/f1tenth_stack/config/f1tenth_online_async.yaml

실제 실행 명령은 scripts/05_slam_start.sh 내용을 기준으로 확인한다.

sed -n '1,160p' scripts/05_slam_start.sh
9. SLAM 중 차량 움직이는 방법

SLAM 중 차량은 천천히 움직여야 한다.

웹 대시보드를 사용할 경우:

cd ~/race_stack/f1tenth

source /opt/ros/foxy/setup.bash
source install/setup.bash

python3 mission_control/dashboard.py

브라우저:

http://localhost:5000

웹 대시보드에서 다음을 권장한다.

주행 모드: 수동 조작
최대 속도: 0.2 이하
최대 조향: 0.10 ~ 0.20 정도

권장 움직임:

1. 직선으로 천천히 이동
2. 멈춤
3. 천천히 회전
4. 다시 직선 이동
5. 같은 장소를 여러 방향에서 관찰
6. 급가속, 급회전 피하기

좋은 맵을 만들기 위한 팁:

천천히 움직인다.
벽이나 장애물 주변을 여러 각도에서 본다.
너무 빠르게 회전하지 않는다.
같은 구역을 한 번 이상 지나간다.
LiDAR가 볼 수 없는 유리, 검은 물체, 반사 물체 근처는 주의한다.
10. 맵 저장

맵이 충분히 만들어졌다면 저장한다.

스크립트 사용:

cd ~/race_stack/f1tenth

source /opt/ros/foxy/setup.bash
source install/setup.bash

bash scripts/06_save_map.sh maps/saved/my_map

위 명령을 실행하면 보통 아래 파일들이 생성된다.

maps/saved/my_map.yaml
maps/saved/my_map.pgm

파일 역할:

파일역할
.yaml맵 이미지 경로, 해상도, origin, threshold 등의 메타데이터
.pgm실제 2D occupancy grid 맵 이미지

저장 결과 확인:

ls -lh maps/saved/

예상 결과:

my_map.yaml
my_map.pgm
11. 저장된 map yaml 확인

저장된 YAML 파일을 확인한다.

cat maps/saved/my_map.yaml

일반적으로 아래와 비슷한 내용이 들어 있다.

image: my_map.pgm
mode: trinary
resolution: 0.05
origin: [-10.0, -10.0, 0.0]
negate: 0
occupied_thresh: 0.65
free_thresh: 0.25

주요 항목:

항목설명
image실제 맵 이미지 파일
resolution픽셀 하나가 의미하는 실제 거리
origin맵 원점 위치
occupied_thresh점유 공간 판단 기준
free_thresh빈 공간 판단 기준
12. RViz2에서 맵 확인

맵이 저장되기 전에도 RViz2에서 /map을 확인할 수 있다.

확인할 항목:

Map display topic: /map
LaserScan display topic: /scan
TF display enabled
Fixed Frame: map

맵이 보이지 않으면 Fixed Frame을 확인한다.

추천 순서:

1. Fixed Frame을 map으로 설정
2. /map display 추가
3. /scan display 추가
4. TF display 추가
5. 차량이 움직일 때 map이 업데이트되는지 확인
13. SLAM 종료

SLAM을 종료하려면 SLAM을 실행한 터미널에서 Ctrl + C를 누른다.

웹 대시보드에서 SLAM을 실행했다면 SLAM 정지 버튼을 사용할 수 있다.

bringup도 종료하려면 bringup 터미널에서 Ctrl + C를 누른다.

필요할 경우 ROS2 프로세스를 확인한다.

ps aux | grep ros2

강제 종료가 필요할 때만 아래 명령을 사용한다.

pkill -f ros2

주의:

pkill -f ros2 명령은 실행 중인 ROS2 프로세스를 한꺼번에 종료할 수 있다.
다른 실험 노드도 함께 종료될 수 있으므로 주의해서 사용한다.
14. 자주 생기는 문제
14.1 /scan이 안 나온다

확인:

ros2 topic list
ros2 topic echo /scan

확인할 것:

[ ] LiDAR 전원이 들어와 있는가?
[ ] LiDAR USB가 연결되어 있는가?
[ ] bringup이 실행 중인가?
[ ] LiDAR 포트 설정이 맞는가?
[ ] 사용자 계정이 serial 장치에 접근 가능한가?

USB 장치 확인:

ls /dev/ttyUSB*
ls /dev/ttyACM*

권한 문제가 의심되면:

groups

필요한 경우 사용자를 dialout 그룹에 추가한다.

sudo usermod -aG dialout $USER

그 뒤 로그아웃/로그인 또는 재부팅이 필요할 수 있다.

14.2 /odom이 안 나온다

확인:

ros2 topic list
ros2 topic echo /odom

확인할 것:

[ ] VESC가 연결되어 있는가?
[ ] VESC 포트 설정이 맞는가?
[ ] bringup이 정상 실행되었는가?
[ ] 모터/인코더 관련 설정이 맞는가?

VESC 포트 확인:

ls /dev/ttyUSB*
ls /dev/ttyACM*
14.3 /tf가 안 맞는다

TF 확인:

ros2 run tf2_tools view_frames

확인할 frame:

map
odom
base_link
laser

자주 생기는 문제:

base_link와 laser가 연결되지 않음
odom과 base_link가 연결되지 않음
map과 odom이 연결되지 않음
frame 이름이 config와 launch에서 다름

frame 이름은 함부로 바꾸지 않는다.

14.4 RViz2에서 맵이 안 보인다

확인할 것:

[ ] SLAM 노드가 실행 중인가?
[ ] /map 토픽이 나오는가?
[ ] RViz2 Fixed Frame이 map인가?
[ ] Map display topic이 /map인가?
[ ] TF가 정상 연결되어 있는가?

명령어:

ros2 topic echo /map
ros2 topic list | grep map
14.5 맵이 삐뚤어지거나 겹친다

가능한 원인:

차량을 너무 빠르게 움직임
너무 빠르게 회전함
/odom 품질이 좋지 않음
LiDAR 데이터가 끊김
TF가 불안정함
바퀴가 미끄러짐
반사 물체가 많음

해결 방법:

속도를 낮춘다.
회전을 천천히 한다.
같은 구역을 여러 번 지나간다.
LiDAR가 잘 보는 벽/구조물 근처에서 테스트한다.
odom과 TF를 확인한다.
14.6 맵 저장이 안 된다

스크립트 확인:

sed -n '1,160p' scripts/06_save_map.sh

직접 저장 명령:

ros2 run nav2_map_server map_saver_cli -f maps/saved/my_map

저장 폴더가 없다면 생성한다.

mkdir -p maps/saved

다시 저장:

ros2 run nav2_map_server map_saver_cli -f maps/saved/my_map
15. 좋은 맵을 만들기 위한 권장 방법

좋은 맵을 만들기 위해서는 아래를 지킨다.

1. 낮은 속도로 주행한다.
2. 급회전을 피한다.
3. 같은 장소를 여러 방향에서 관찰한다.
4. 벽과 코너를 충분히 스캔한다.
5. 통로 끝에서 천천히 회전한다.
6. 사람이 움직이는 환경에서는 맵을 만들지 않는다.
7. 유리, 검은 물체, 반사 물체 근처는 주의한다.
8. 맵이 틀어지기 시작하면 바로 멈추고 다시 시작한다.

추천 속도:

처음 테스트: 0.1 ~ 0.2
익숙해진 뒤: 0.2 ~ 0.4

실험 환경에 따라 값은 달라질 수 있다.

16. SLAM 완료 후 다음 단계

맵 저장까지 완료했다면 다음 단계는 위치추정이다.

다음 문서:

docs/04_위치추정_particle_filter.md

위치추정 단계에서는 저장한 맵을 불러오고, 차량이 맵 위에서 어디에 있는지 추정한다.

SLAM 단계의 결과물은 보통 아래 두 파일이다.

maps/saved/my_map.yaml
maps/saved/my_map.pgm

이 두 파일은 localization과 path following 단계에서 사용된다.

17. 이 문서에서 바꾸지 않는 것

현재 단계에서는 아래 이름을 바꾸지 않는다.

/scan
/odom
/map
/tf
/tf_static
base_link
laser
odom
map

이 이름들은 SLAM, localization, RViz2, controller에서 함께 사용될 수 있다.

문서화 단계에서는 이름을 바꾸지 않고, 먼저 전체 흐름을 안정적으로 이해하는 것을 목표로 한다.
