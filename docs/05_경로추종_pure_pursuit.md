# 05. 경로추종 Pure Pursuit

이 문서는 F1TENTH 차량이 waypoint 또는 raceline을 따라 주행하도록 하는 Pure Pursuit 경로추종 방법을 설명한다.

Pure Pursuit는 차량 앞쪽의 목표점을 바라보며 조향각을 계산하는 경로추종 알고리즘이다. F1TENTH 실험에서는 저장된 맵 위에서 현재 위치를 추정한 뒤, 미리 준비된 경로를 따라가도록 할 때 사용한다.

---

## 1. 이 문서의 목표

이 문서에서는 다음 내용을 다룬다.

```text
1. Pure Pursuit 개념 이해
2. waypoint / raceline 파일 역할 이해
3. 위치추정 실행
4. Pure Pursuit 실행
5. RViz2에서 경로와 차량 위치 확인
6. 속도와 lookahead distance 조정
7. 실차 테스트 순서
8. 자주 생기는 문제 해결
2. Pure Pursuit란?

Pure Pursuit는 차량이 현재 위치에서 일정 거리 앞에 있는 목표점을 선택하고, 그 목표점을 향해 조향하는 방식이다.

간단히 말하면 다음과 같다.

1. 차량의 현재 위치를 확인한다.
2. 주행 경로에서 차량 앞쪽의 목표점을 찾는다.
3. 차량이 그 목표점을 향하도록 조향각을 계산한다.
4. 계산한 속도와 조향 명령을 /drive로 보낸다.
5. 이 과정을 계속 반복한다.

여기서 차량 앞쪽의 목표점을 찾는 거리를 lookahead distance라고 한다.

3. Pure Pursuit에 필요한 정보

Pure Pursuit가 정상적으로 동작하려면 아래 정보가 필요하다.

항목설명
현재 차량 위치localization 또는 particle filter 결과
현재 차량 방향map → base_link 또는 관련 TF
주행 경로waypoint 또는 raceline CSV
목표 속도차량이 따라갈 속도
lookahead distance차량 앞쪽 목표점을 선택하는 거리
/drive최종 차량 제어 명령
4. 중요한 토픽과 frame

Pure Pursuit와 관련된 주요 토픽과 frame은 다음과 같다.

이름역할
/drive차량 구동 명령
/odom차량 odometry
/tf좌표계 변환
/map맵
/scanLiDAR 데이터
maps/전역 맵 좌표계
odomodometry 좌표계
base_link차량 중심 좌표계
laserLiDAR 센서 좌표계

일반적인 흐름은 다음과 같다.

particle_filter / localization
  ↓
현재 차량 위치 추정
  ↓
Pure Pursuit
  ↓
/drive
  ↓
VESC
  ↓
모터 / 서보
5. 실행 전 준비물

Pure Pursuit를 실행하기 전에는 아래가 준비되어 있어야 한다.

[ ] 차량 bringup이 정상 동작한다.
[ ] /scan 토픽이 나온다.
[ ] /odom 토픽이 나온다.
[ ] /tf가 정상이다.
[ ] SLAM으로 저장한 맵이 있다.
[ ] localization이 안정적으로 동작한다.
[ ] waypoint 또는 raceline 파일이 있다.

맵 파일 예시:

maps/saved/my_map.yaml
maps/saved/my_map.pgm

waypoint 또는 raceline 파일은 레포 안에서 아래 명령으로 찾아볼 수 있다.

cd ~/race_stack/f1tenth

find . -iname "*.csv" -o -iname "*waypoint*" -o -iname "*raceline*"

Pure Pursuit 관련 설정 파일은 아래 명령으로 확인한다.

cd ~/race_stack/f1tenth

find src/pure_pursuit -name "*.yaml" -o -name "*.yml" -o -name "*.py" -o -name "*.cpp" | sort
6. 실행 전 안전 체크리스트

Pure Pursuit는 차량을 실제로 움직일 수 있다.

실차에서 실행하기 전 반드시 아래를 확인한다.

[ ] 주변에 사람이 없는가?
[ ] 주행 공간이 충분한가?
[ ] 차량 바퀴를 띄운 상태에서 먼저 테스트했는가?
[ ] emergency stop 방법을 알고 있는가?
[ ] 목표 속도가 낮게 설정되어 있는가?
[ ] waypoint가 현재 맵과 같은 좌표계 기준인가?
[ ] localization 위치가 실제 차량 위치와 맞는가?
[ ] /drive 토픽을 누가 발행하는지 알고 있는가?

처음에는 반드시 낮은 속도로 테스트한다.

7. 실행 순서 요약

Pure Pursuit 실행 흐름은 다음과 같다.

1. ROS2 환경 적용
2. 차량 bringup 실행
3. RViz2 실행
4. localization 실행
5. 차량 위치가 맵 위에서 맞는지 확인
6. Pure Pursuit 실행
7. /drive 명령 확인
8. 낮은 속도로 실차 테스트

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

다른 터미널에서 Pure Pursuit 실행:

cd ~/race_stack/f1tenth

source /opt/ros/foxy/setup.bash
source install/setup.bash

bash scripts/08_pure_pursuit.sh
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
터미널 4: Pure Pursuit
cd ~/race_stack/f1tenth

source /opt/ros/foxy/setup.bash
source install/setup.bash

bash scripts/08_pure_pursuit.sh
터미널 5: 토픽 확인
cd ~/race_stack/f1tenth

source /opt/ros/foxy/setup.bash
source install/setup.bash

ros2 topic list
9. Pure Pursuit 실행 전 스크립트 확인

실제 어떤 launch 파일이나 실행 파일을 사용하는지 먼저 확인한다.

cd ~/race_stack/f1tenth

sed -n '1,200p' scripts/08_pure_pursuit.sh

Pure Pursuit 패키지 구조 확인:

cd ~/race_stack/f1tenth

find src/pure_pursuit -maxdepth 4 -type f | sort

config 파일 확인:

cd ~/race_stack/f1tenth

find src/pure_pursuit -name "*.yaml" -o -name "*.yml" | sort

CSV 경로 파일 확인:

cd ~/race_stack/f1tenth

find . -iname "*.csv" | sort
10. Pure Pursuit 실행

스크립트 사용:

cd ~/race_stack/f1tenth

source /opt/ros/foxy/setup.bash
source install/setup.bash

bash scripts/08_pure_pursuit.sh

실행 후 토픽을 확인한다.

ros2 topic list

확인할 주요 토픽:

/drive
/odom
/tf
/map
/scan

/drive 명령이 나오는지 확인한다.

ros2 topic echo /drive
11. RViz2에서 확인할 항목

Pure Pursuit를 실행할 때 RViz2에서 확인할 항목은 다음과 같다.

Fixed Frame: map
Map: /map
LaserScan: /scan
TF: map, odom, base_link, laser
차량 현재 위치
waypoint 또는 raceline
목표점 lookahead point

실제 표시 토픽 이름은 코드와 config에 따라 다를 수 있다.

관련 토픽을 찾으려면:

ros2 topic list | grep -E "path|waypoint|goal|target|pure|marker"

RViz2에서 Marker 또는 Path display를 추가해 관련 토픽을 선택한다.

12. waypoint / raceline 파일

Pure Pursuit는 보통 CSV 형태의 waypoint 또는 raceline 파일을 사용한다.

일반적인 CSV에는 아래와 같은 정보가 들어갈 수 있다.

x 좌표
y 좌표
속도
yaw 또는 heading
곡률

레포에 있는 CSV 파일을 확인한다.

cd ~/race_stack/f1tenth

find . -iname "*.csv" | sort

파일 내용을 일부 확인한다.

head -20 path/to/waypoint.csv

주의할 점:

waypoint 좌표계는 localization의 map 좌표계와 맞아야 한다.
맵이 바뀌면 기존 waypoint가 맞지 않을 수 있다.
차량 시작 위치와 waypoint 시작 위치가 너무 멀면 차량이 급하게 조향할 수 있다.
13. 주요 파라미터

Pure Pursuit에서 자주 조정하는 값은 다음과 같다.

파라미터의미
lookahead_distance차량 앞쪽 목표점을 찾는 거리
velocity 또는 target_speed목표 속도
wheelbase차량 축간거리
waypoint_pathwaypoint CSV 파일 경로
drive_topic제어 명령 출력 토픽
map_frame맵 기준 frame
base_frame차량 기준 frame

실제 파라미터 이름은 코드에 따라 다를 수 있다.

파라미터가 어디 있는지 찾으려면:

cd ~/race_stack/f1tenth

grep -R "lookahead" -n src/pure_pursuit
grep -R "velocity\\|speed" -n src/pure_pursuit
grep -R "waypoint\\|raceline\\|csv" -n src/pure_pursuit
14. lookahead distance 조정

lookahead distance는 차량이 얼마나 앞의 목표점을 볼지 결정한다.

일반적인 경향:

lookahead distance특징
너무 작음조향이 민감하고 흔들릴 수 있음
적당함경로를 안정적으로 따라감
너무 큼코너를 크게 돌거나 경로를 벗어날 수 있음

처음에는 작은 속도와 함께 보수적인 값을 사용한다.

낮은 속도: 작은 lookahead
높은 속도: 조금 더 큰 lookahead

단, 실제 값은 트랙 크기, waypoint 간격, 차량 속도에 따라 달라진다.

15. 목표 속도 조정

실차 테스트에서는 목표 속도를 낮게 시작해야 한다.

추천 시작값:

처음 테스트: 0.1 ~ 0.2
기본 확인 후: 0.2 ~ 0.5
익숙해진 뒤: 환경에 맞게 증가

속도 관련 값을 찾으려면:

cd ~/race_stack/f1tenth

grep -R "speed\\|velocity" -n src/pure_pursuit

속도를 높이기 전에 반드시 아래를 확인한다.

[ ] localization이 안정적인가?
[ ] 경로가 맵과 맞는가?
[ ] /drive 명령이 예상 범위인가?
[ ] 조향이 과도하지 않은가?
[ ] safety node가 동작 중인가?
16. 실차 테스트 순서

처음 Pure Pursuit를 실차에서 테스트할 때는 아래 순서를 권장한다.

1. 차량 바퀴를 바닥에서 띄운다.
2. bringup을 실행한다.
3. localization을 실행한다.
4. RViz2에서 차량 위치가 맞는지 확인한다.
5. Pure Pursuit를 실행한다.
6. /drive 명령이 정상 범위인지 echo로 확인한다.
7. 정지 또는 emergency stop 방법을 준비한다.
8. 바퀴를 바닥에 내린다.
9. 아주 낮은 속도로 짧게 주행한다.
10. 차량이 경로를 따라가는지 확인한다.
11. 문제가 있으면 즉시 정지한다.

/drive 확인:

ros2 topic echo /drive
17. 자주 생기는 문제
17.1 차량이 움직이지 않는다

확인할 것:

[ ] bringup이 실행 중인가?
[ ] Pure Pursuit 노드가 실행 중인가?
[ ] localization이 실행 중인가?
[ ] /drive 토픽이 발행되는가?
[ ] VESC가 연결되어 있는가?
[ ] mux가 /drive 명령을 받아들이는가?
[ ] 자율주행 모드로 전환되어 있는가?

확인 명령:

ros2 node list
ros2 topic echo /drive
17.2 차량이 엉뚱한 방향으로 간다

가능한 원인:

차량 위치추정이 틀림
waypoint 좌표계가 현재 map과 다름
차량 시작 방향이 경로 방향과 다름
좌표 frame이 잘못 설정됨
조향 부호가 반대로 적용됨

확인:

ros2 run tf2_tools view_frames
ros2 topic echo /tf

RViz2에서 /scan, 맵, 차량 위치, waypoint가 서로 맞는지 확인한다.

17.3 차량이 경로 주변에서 흔들린다

가능한 원인:

lookahead distance가 너무 작음
속도가 너무 빠름
waypoint 간격이 너무 촘촘하거나 불규칙함
localization pose가 흔들림
조향 gain이 너무 큼

해결:

속도를 낮춘다.
lookahead distance를 조금 키운다.
localization이 안정적인지 먼저 확인한다.
waypoint가 부드러운지 확인한다.
17.4 코너에서 경로를 크게 벗어난다

가능한 원인:

lookahead distance가 너무 큼
속도가 너무 빠름
waypoint가 코너를 충분히 촘촘하게 표현하지 못함
조향 제한이 너무 작음

해결:

속도를 낮춘다.
lookahead distance를 줄인다.
코너 waypoint를 다시 확인한다.
조향 제한값을 확인한다.
17.5 차량이 갑자기 급가속한다

즉시 정지한다.

확인할 것:

목표 속도가 너무 크게 설정되어 있지 않은가?
velocity 단위가 m/s 기준인지 확인했는가?
CSV 파일의 속도 값이 너무 크지 않은가?
/drive 토픽에 큰 speed 값이 들어가는가?

확인 명령:

ros2 topic echo /drive
grep -R "speed\\|velocity" -n src/pure_pursuit
17.6 waypoint 파일을 못 찾는다

오류 메시지에 파일 경로가 나올 수 있다.

확인:

cd ~/race_stack/f1tenth

find . -iname "*.csv" | sort
grep -R "csv\\|waypoint\\|raceline" -n src/pure_pursuit

config 파일에 적힌 경로가 실제 파일 위치와 맞는지 확인한다.

18. 디버깅 명령 모음
노드 확인
ros2 node list
토픽 확인
ros2 topic list
drive 명령 확인
ros2 topic echo /drive
localization pose 관련 토픽 찾기
ros2 topic list | grep -E "pose|particle|infer|local"
경로 표시 토픽 찾기
ros2 topic list | grep -E "path|waypoint|goal|target|marker|pure"
TF 확인
ros2 run tf2_tools view_frames
Pure Pursuit 코드에서 주요 파라미터 찾기
cd ~/race_stack/f1tenth

grep -R "lookahead" -n src/pure_pursuit
grep -R "speed\\|velocity" -n src/pure_pursuit
grep -R "waypoint\\|raceline\\|csv" -n src/pure_pursuit
grep -R "/drive" -n src/pure_pursuit
19. 좋은 경로추종을 위한 팁
1. 위치추정이 안정된 뒤에 Pure Pursuit를 실행한다.
2. 처음에는 속도를 낮춘다.
3. 경로와 맵이 같은 좌표계인지 확인한다.
4. RViz2에서 차량 위치와 waypoint를 함께 본다.
5. lookahead distance를 한 번에 크게 바꾸지 않는다.
6. 속도를 올릴 때는 조금씩 올린다.
7. 코너에서 벗어나면 속도와 lookahead를 먼저 낮춰본다.
8. 차량이 흔들리면 localization과 waypoint 품질을 먼저 확인한다.
20. Pure Pursuit 완료 후 다음 단계

Pure Pursuit 경로추종이 안정적으로 동작하면 다음 단계는 Stanley 기반 장애물 회피다.

다음 문서:

docs/06_장애물회피_stanley_avoidance.md

Stanley avoidance 단계에서는 경로추종에 더해 LiDAR 기반 장애물 회피를 함께 다룬다.

21. 이 문서에서 바꾸지 않는 것

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
