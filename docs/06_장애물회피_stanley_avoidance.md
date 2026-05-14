# 06. 장애물회피 Stanley Avoidance

이 문서는 F1TENTH 차량에서 Stanley Controller 기반 경로추종과 LiDAR 기반 장애물 회피를 실행하는 방법을 설명한다.

Stanley avoidance 단계는 Pure Pursuit보다 더 위험할 수 있다. 차량이 경로를 따라가면서 동시에 장애물을 피하려고 조향 명령을 만들기 때문이다. 실차에서 실행하기 전에는 반드시 낮은 속도와 넓은 공간에서 테스트해야 한다.

---

## 1. 이 문서의 목표

이 문서에서는 다음 내용을 다룬다.

```text
1. Stanley Controller 개념 이해
2. 장애물 회피 흐름 이해
3. 실행 전 준비물 확인
4. bringup 실행
5. localization 실행
6. Stanley avoidance 실행
7. RViz2와 토픽으로 상태 확인
8. 실차 안전 테스트 순서
9. 자주 생기는 문제 해결
2. Stanley Controller란?

Stanley Controller는 차량이 목표 경로를 따라가도록 조향각을 계산하는 경로추종 알고리즘이다.

Pure Pursuit가 차량 앞쪽의 목표점을 바라보는 방식이라면, Stanley Controller는 보통 다음 두 가지 오차를 이용한다.

1. heading error
2. cross-track error
heading error

heading error는 차량이 바라보는 방향과 경로가 진행되는 방향 사이의 각도 차이다.

차량 방향과 경로 방향이 같으면 heading error가 작다.
차량이 경로와 다른 방향을 보고 있으면 heading error가 크다.
cross-track error

cross-track error는 차량이 경로에서 옆으로 얼마나 벗어나 있는지를 의미한다.

차량이 경로 위에 있으면 cross-track error가 작다.
차량이 경로 왼쪽이나 오른쪽으로 벗어나 있으면 cross-track error가 커진다.

Stanley Controller는 이 두 오차를 줄이는 방향으로 조향 명령을 만든다.

3. 장애물 회피의 기본 흐름

Stanley avoidance는 보통 아래 흐름으로 동작한다.

LiDAR /scan 수신
  ↓
차량 앞쪽 장애물 거리 확인
  ↓
장애물이 없으면 Stanley 경로추종
  ↓
장애물이 있으면 회피 조향 계산
  ↓
/drive로 속도와 조향 명령 발행

즉, 기본은 경로추종이고 장애물이 감지되면 조향을 바꿔 장애물을 피하려는 구조다.

4. 중요한 토픽과 frame

Stanley avoidance와 관련된 주요 토픽과 frame은 다음과 같다.

이름역할
/drive차량 구동 명령
/scanLiDAR 스캔 데이터
/odom차량 odometry
/map맵
/tf좌표계 변환
maps/전역 맵 좌표계
odomodometry 좌표계
base_link차량 중심 좌표계
laserLiDAR 센서 좌표계

일반적인 흐름:

localization
  ↓
현재 차량 위치 추정
  ↓
Stanley avoidance
  ↓
/drive
  ↓
VESC
  ↓
모터 / 서보

장애물 회피까지 포함하면 다음과 같다.

/scan
  ↓
장애물 감지
  ↓
Stanley avoidance
  ↓
/drive
5. 실행 전 준비물

Stanley avoidance를 실행하기 전에는 아래가 준비되어 있어야 한다.

[ ] 차량 bringup이 정상 동작한다.
[ ] /scan 토픽이 나온다.
[ ] /odom 토픽이 나온다.
[ ] /tf가 정상이다.
[ ] SLAM으로 저장한 맵이 있다.
[ ] localization이 안정적으로 동작한다.
[ ] 경로 파일 또는 raceline 파일이 있다.
[ ] Pure Pursuit 또는 기본 경로추종이 먼저 테스트되어 있다.

Stanley avoidance 관련 파일은 아래 명령으로 확인한다.

cd ~/race_stack/f1tenth

find src/stanley_avoidance -maxdepth 5 -type f | sort

설정 파일 확인:

cd ~/race_stack/f1tenth

find src/stanley_avoidance -name "*.yaml" -o -name "*.yml" | sort

코드에서 주요 파라미터 찾기:

cd ~/race_stack/f1tenth

grep -R "stanley\|obstacle\|avoid\|scan\|drive\|speed" -n src/stanley_avoidance
6. 실행 전 안전 체크리스트

Stanley avoidance는 차량을 실제로 움직일 수 있다.

실차에서 실행하기 전 반드시 아래를 확인한다.

[ ] 넓고 안전한 테스트 공간인가?
[ ] 주변에 사람이 없는가?
[ ] 장애물은 부드럽거나 충돌 위험이 낮은 물체인가?
[ ] emergency stop 방법을 알고 있는가?
[ ] 목표 속도가 낮게 설정되어 있는가?
[ ] 장애물 감지 거리가 너무 짧지 않은가?
[ ] 차량 바퀴를 띄운 상태에서 먼저 테스트했는가?
[ ] /drive 명령이 예상 범위인지 확인했는가?
[ ] localization이 안정적인가?
[ ] /scan이 정상인가?

처음 테스트할 때는 장애물을 차량 앞에 바로 두지 말고, 충분한 거리를 두고 천천히 접근시킨다.

7. 실행 순서 요약

Stanley avoidance 실행 흐름은 다음과 같다.

1. ROS2 환경 적용
2. 차량 bringup 실행
3. RViz2 실행
4. localization 실행
5. 차량 위치가 맵 위에서 맞는지 확인
6. Stanley avoidance 실행
7. /drive 명령 확인
8. 낮은 속도로 실차 테스트
9. 장애물 회피 반응 확인

스크립트 기준 실행 순서:

cd ~/race_stack/f1tenth

source /opt/ros/foxy/setup.bash
source install/setup.bash

bash scripts/02_bringup.sh

다른 터미널에서 RViz2 실행:

cd ~/race_stack/f1tenth

source /opt/ros/foxy/setup.bash
source install/setup.bash

bash scripts/04_rviz.sh

다른 터미널에서 localization 실행:

cd ~/race_stack/f1tenth

source /opt/ros/foxy/setup.bash
source install/setup.bash

bash scripts/07_localization.sh

다른 터미널에서 Stanley avoidance 실행:

cd ~/race_stack/f1tenth

source /opt/ros/foxy/setup.bash
source install/setup.bash

bash scripts/09_stanley_avoidance.sh
8. 터미널 구성 추천
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
터미널 3: localization
cd ~/race_stack/f1tenth

source /opt/ros/foxy/setup.bash
source install/setup.bash

bash scripts/07_localization.sh
터미널 4: Stanley avoidance
cd ~/race_stack/f1tenth

source /opt/ros/foxy/setup.bash
source install/setup.bash

bash scripts/09_stanley_avoidance.sh
터미널 5: 토픽 확인
cd ~/race_stack/f1tenth

source /opt/ros/foxy/setup.bash
source install/setup.bash

ros2 topic list
9. Stanley avoidance 실행 전 스크립트 확인

실제 어떤 launch 파일이나 실행 파일을 사용하는지 먼저 확인한다.

cd ~/race_stack/f1tenth

sed -n '1,200p' scripts/09_stanley_avoidance.sh

패키지 구조 확인:

cd ~/race_stack/f1tenth

find src/stanley_avoidance -maxdepth 5 -type f | sort

config 파일 확인:

cd ~/race_stack/f1tenth

find src/stanley_avoidance -name "*.yaml" -o -name "*.yml" | sort

CSV 또는 경로 파일 확인:

cd ~/race_stack/f1tenth

find . -iname "*.csv" | sort
10. Stanley avoidance 실행

스크립트 사용:

cd ~/race_stack/f1tenth

source /opt/ros/foxy/setup.bash
source install/setup.bash

bash scripts/09_stanley_avoidance.sh

실행 후 토픽을 확인한다.

ros2 topic list

확인할 주요 토픽:

/drive
/scan
/odom
/tf
/map

/drive 명령 확인:

ros2 topic echo /drive

LiDAR 입력 확인:

ros2 topic echo /scan
11. RViz2에서 확인할 항목

Stanley avoidance를 실행할 때 RViz2에서 확인할 항목은 다음과 같다.

Fixed Frame: map
Map: /map
LaserScan: /scan
TF: map, odom, base_link, laser
차량 현재 위치
주행 경로 또는 raceline
장애물 감지 영역
회피 목표점 또는 marker

실제 표시 토픽 이름은 코드와 config에 따라 다를 수 있다.

관련 토픽을 찾으려면:

ros2 topic list | grep -E "path|waypoint|goal|target|marker|stanley|obstacle|avoid"

RViz2에서 Marker, Path, LaserScan display를 추가해 관련 토픽을 선택한다.

12. 장애물 감지 확인

장애물 회피가 제대로 되려면 /scan 값이 정상이어야 한다.

확인:

ros2 topic echo /scan

LiDAR 거리 값에서 ranges가 정상적으로 변하는지 본다.

장애물을 차량 앞쪽에 천천히 가져가면 앞쪽 각도 범위의 거리 값이 줄어들어야 한다.

주의:

실차 테스트에서는 차량 앞에 사람을 세워 장애물 테스트를 하지 않는다.
처음에는 박스, 스펀지, 콘 같은 충돌 위험이 낮은 물체를 사용한다.
13. 주요 파라미터

Stanley avoidance에서 자주 조정하는 값은 다음과 같다.

파라미터의미
stanley_gain경로 오차 보정 강도
target_speed목표 속도
obstacle_distance장애물 감지 기준 거리
avoidance_gain회피 조향 강도
max_steering_angle최대 조향 제한
wheelbase차량 축간거리
waypoint_pathwaypoint 또는 raceline 파일 경로
drive_topic제어 명령 출력 토픽
scan_topicLiDAR 입력 토픽

실제 파라미터 이름은 코드에 따라 다를 수 있다.

파라미터가 어디 있는지 찾으려면:

cd ~/race_stack/f1tenth

grep -R "gain\|speed\|velocity\|obstacle\|distance\|steer\|wheelbase" -n src/stanley_avoidance
14. Stanley gain 조정

stanley_gain은 차량이 경로에서 벗어났을 때 얼마나 강하게 복귀하려고 하는지를 결정한다.

일반적인 경향:

Stanley gain특징
너무 작음경로로 천천히 돌아오거나 경로를 잘 못 따라감
적당함부드럽게 경로를 따라감
너무 큼조향이 민감해지고 좌우로 흔들릴 수 있음

처음에는 기본값을 유지하고, 문제가 있을 때 조금씩 바꾼다.

15. 장애물 감지 거리 조정

obstacle_distance 또는 비슷한 이름의 파라미터는 장애물을 얼마나 멀리서 감지할지 결정한다.

일반적인 경향:

장애물 감지 거리특징
너무 짧음늦게 피해서 충돌 위험 증가
적당함안정적으로 회피 가능
너무 김너무 일찍 회피하거나 불필요하게 흔들림

처음 테스트할 때는 보수적으로 설정한다.

낮은 속도에서는 짧은 거리도 가능하지만,
실차 안전을 위해 처음에는 여유 있는 거리로 테스트한다.
16. 목표 속도 조정

실차 테스트에서는 목표 속도를 낮게 시작해야 한다.

추천 시작값:

처음 테스트: 0.1 ~ 0.2
기본 확인 후: 0.2 ~ 0.4
익숙해진 뒤: 환경에 맞게 증가

속도 관련 값을 찾으려면:

cd ~/race_stack/f1tenth

grep -R "speed\|velocity" -n src/stanley_avoidance

속도를 높이기 전에 반드시 아래를 확인한다.

[ ] localization이 안정적인가?
[ ] /scan이 끊기지 않는가?
[ ] 장애물 감지 거리가 충분한가?
[ ] /drive 명령이 예상 범위인가?
[ ] emergency stop이 준비되어 있는가?
17. 실차 테스트 순서

처음 Stanley avoidance를 실차에서 테스트할 때는 아래 순서를 권장한다.

1. 차량 바퀴를 바닥에서 띄운다.
2. bringup을 실행한다.
3. localization을 실행한다.
4. RViz2에서 차량 위치가 맞는지 확인한다.
5. Stanley avoidance를 실행한다.
6. /drive 명령이 정상 범위인지 echo로 확인한다.
7. /scan 값이 정상인지 확인한다.
8. 정지 또는 emergency stop 방법을 준비한다.
9. 바퀴를 바닥에 내린다.
10. 아주 낮은 속도로 짧게 주행한다.
11. 부드러운 장애물을 멀리 두고 반응을 확인한다.
12. 문제가 있으면 즉시 정지한다.

/drive 확인:

ros2 topic echo /drive

/scan 확인:

ros2 topic echo /scan
18. 자주 생기는 문제
18.1 차량이 움직이지 않는다

확인할 것:

[ ] bringup이 실행 중인가?
[ ] Stanley avoidance 노드가 실행 중인가?
[ ] localization이 실행 중인가?
[ ] /drive 토픽이 발행되는가?
[ ] VESC가 연결되어 있는가?
[ ] mux가 /drive 명령을 받아들이는가?
[ ] 목표 속도가 0으로 되어 있지 않은가?

확인 명령:

ros2 node list
ros2 topic echo /drive
18.2 차량이 경로를 따라가지 못한다

가능한 원인:

localization이 틀림
waypoint 좌표계가 현재 map과 다름
Stanley gain이 너무 작거나 큼
차량 시작 방향이 경로 방향과 다름
조향 부호가 반대로 적용됨

확인:

ros2 run tf2_tools view_frames
ros2 topic echo /tf

RViz2에서 /scan, 맵, 차량 위치, waypoint가 서로 맞는지 확인한다.

18.3 차량이 좌우로 심하게 흔들린다

가능한 원인:

Stanley gain이 너무 큼
속도가 너무 빠름
localization pose가 흔들림
waypoint가 불규칙함
조향 제한이 너무 큼

해결:

속도를 낮춘다.
Stanley gain을 낮춘다.
localization이 안정적인지 먼저 확인한다.
waypoint가 부드러운지 확인한다.
18.4 장애물을 못 피한다

가능한 원인:

/scan이 정상적으로 들어오지 않음
장애물 감지 거리가 너무 짧음
LiDAR 각도 범위 설정이 잘못됨
회피 조향 강도가 너무 작음
속도가 너무 빠름
장애물이 LiDAR에 잘 보이지 않음

확인:

ros2 topic echo /scan
grep -R "obstacle\|scan\|distance\|avoid" -n src/stanley_avoidance

해결:

속도를 낮춘다.
장애물 감지 거리를 늘린다.
LiDAR가 장애물을 실제로 보고 있는지 확인한다.
충돌 위험이 낮은 장애물로 다시 테스트한다.
18.5 장애물이 없는데도 회피한다

가능한 원인:

LiDAR 노이즈
장애물 감지 거리 기준이 너무 큼
바닥이나 차량 일부를 장애물로 인식
scan 각도 범위 설정이 넓거나 잘못됨
반사 물체 또는 유리

확인:

ros2 topic echo /scan

해결:

LiDAR scan을 RViz2에서 확인한다.
장애물 감지 거리 기준을 조정한다.
scan 사용 각도 범위를 확인한다.
차량 자체가 LiDAR에 보이는지 확인한다.
18.6 차량이 갑자기 급가속한다

즉시 정지한다.

확인할 것:

목표 속도가 너무 크게 설정되어 있지 않은가?
velocity 단위가 m/s 기준인지 확인했는가?
CSV 파일의 속도 값이 너무 크지 않은가?
/drive 토픽에 큰 speed 값이 들어가는가?

확인 명령:

ros2 topic echo /drive
grep -R "speed\|velocity" -n src/stanley_avoidance
19. 디버깅 명령 모음
노드 확인
ros2 node list
토픽 확인
ros2 topic list
drive 명령 확인
ros2 topic echo /drive
LiDAR 확인
ros2 topic echo /scan
localization pose 관련 토픽 찾기
ros2 topic list | grep -E "pose|particle|infer|local"
경로 / 장애물 표시 토픽 찾기
ros2 topic list | grep -E "path|waypoint|goal|target|marker|stanley|obstacle|avoid"
TF 확인
ros2 run tf2_tools view_frames
Stanley avoidance 코드에서 주요 파라미터 찾기
cd ~/race_stack/f1tenth

grep -R "gain\|speed\|velocity\|obstacle\|distance\|steer\|wheelbase" -n src/stanley_avoidance
grep -R "/drive\|/scan\|/odom" -n src/stanley_avoidance
20. 좋은 장애물 회피 테스트를 위한 팁
1. 위치추정이 안정된 뒤에 실행한다.
2. 처음에는 속도를 낮춘다.
3. 장애물은 부드럽고 가벼운 물체를 사용한다.
4. 사람을 장애물로 세워 테스트하지 않는다.
5. 장애물을 차량 바로 앞에 두지 않는다.
6. RViz2에서 /scan이 장애물을 보는지 먼저 확인한다.
7. /drive 명령이 예상 범위인지 먼저 확인한다.
8. 파라미터는 한 번에 하나씩만 바꾼다.
9. 문제가 생기면 즉시 정지한다.
21. Stanley avoidance 완료 후 다음 단계

Stanley avoidance까지 문서화했다면 다음 단계는 문제해결 문서다.

다음 문서:

docs/08_문제해결.md

문제해결 문서에는 빌드 오류, Flask 오류, VESC 오류, LiDAR 오류, TF 오류, SLAM 오류, localization 오류, 주행 오류를 모아 정리한다.

22. 이 문서에서 바꾸지 않는 것

현재 단계에서는 아래 이름을 바꾸지 않는다.

/drive
/webop
/teleop
/scan
/odom
/map
/tf
/tf_static
base_link
laser
odom
map

이 이름들은 bringup, localization, controller, RViz2에서 함께 사용될 수 있다.

문서화 단계에서는 이름을 바꾸지 않고, 먼저 전체 흐름을 안정적으로 이해하는 것을 목표로 한다.
