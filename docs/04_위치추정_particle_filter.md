# 04. 위치추정 Particle Filter

이 문서는 저장된 맵 위에서 F1TENTH 차량의 위치를 추정하는 방법을 설명한다.

위치추정은 차량이 이미 만들어진 맵 안에서 “내가 지금 어디에 있는지”를 계산하는 과정이다. 이 레포에서는 `particle_filter` 패키지를 사용해 위치를 추정한다.

---

## 1. 이 문서의 목표

이 문서에서는 다음 내용을 다룬다.

```text
1. 위치추정이 왜 필요한지 이해
2. Particle Filter의 역할 이해
3. 저장된 맵 준비
4. bringup 실행
5. RViz2 실행
6. localization 실행
7. RViz2에서 위치 확인
8. 위치가 틀어질 때 확인할 것
2. 위치추정이 필요한 이유

SLAM 단계에서는 차량이 움직이면서 맵을 만든다.

하지만 경로추종이나 장애물 회피를 하려면, 먼저 차량이 저장된 맵 위에서 현재 어디에 있는지 알아야 한다.

예를 들어 Pure Pursuit나 Stanley controller는 다음 정보가 필요하다.

차량의 현재 위치
차량의 현재 방향
주행할 waypoint 또는 raceline
맵 기준 좌표계

위치추정이 불안정하면 차량은 경로를 제대로 따라가지 못한다.

3. Particle Filter란?

Particle Filter는 여러 개의 후보 위치를 동시에 유지하면서, LiDAR 관측값과 맵을 비교해 가장 그럴듯한 차량 위치를 찾는 방식이다.

간단히 말하면 다음과 같다.

1. 차량이 있을 법한 위치 후보를 여러 개 뿌린다.
2. 차량이 움직이면 후보 위치도 같이 움직인다.
3. LiDAR로 본 주변 모양과 저장된 맵을 비교한다.
4. 실제 관측과 잘 맞는 후보는 살린다.
5. 안 맞는 후보는 줄인다.
6. 최종적으로 가장 그럴듯한 위치를 추정한다.

여기서 각각의 위치 후보를 particle이라고 부른다.

4. 위치추정에서 중요한 토픽과 frame

위치추정이 정상 동작하려면 아래 정보가 필요하다.

이름역할
/scanLiDAR 스캔 데이터
/odom차량 이동량 정보
/map저장된 맵 또는 map server가 제공하는 맵
/tf좌표계 변환
maps/전역 맵 좌표계
odomodometry 좌표계
base_link차량 중심 좌표계
laserLiDAR 센서 좌표계

일반적인 frame 관계는 다음과 같다.

map
 ↓
odom
 ↓
base_link
 ↓
laser

주의할 점:

map, odom, base_link, laser 이름은 여러 노드가 공유한다.
문서화 단계에서는 이 이름을 바꾸지 않는다.
5. 실행 전 준비물

위치추정을 하려면 먼저 SLAM 단계에서 만든 맵이 있어야 한다.

보통 아래 두 파일이 필요하다.

maps/saved/my_map.yaml
maps/saved/my_map.pgm

파일 확인:

cd ~/race_stack/f1tenth

ls -lh maps/saved/

예상 결과:

my_map.yaml
my_map.pgm

my_map.yaml 안의 image 항목이 .pgm 파일을 제대로 가리키는지 확인한다.

cat maps/saved/my_map.yaml

예시:

image: my_map.pgm
mode: trinary
resolution: 0.05
origin: [-10.0, -10.0, 0.0]
negate: 0
occupied_thresh: 0.65
free_thresh: 0.25
6. 실행 전 안전 체크리스트

실차에서 위치추정을 실행하기 전 아래를 확인한다.

[ ] 저장된 맵 파일이 있는가?
[ ] 차량이 맵을 만들었던 환경과 같은 장소에 있는가?
[ ] LiDAR가 정상 연결되어 있는가?
[ ] VESC가 정상 연결되어 있는가?
[ ] /scan 토픽이 나오는가?
[ ] /odom 토픽이 나오는가?
[ ] /tf가 정상인가?
[ ] RViz2에서 map, odom, base_link, laser를 볼 수 있는가?

위치추정 자체는 차량을 바로 움직이지 않을 수 있지만, bringup과 다른 제어 노드가 함께 실행되어 있을 수 있으므로 실차 안전 확인은 항상 필요하다.

7. 실행 순서 요약

위치추정의 기본 실행 흐름은 다음과 같다.

1. ROS2 환경 적용
2. 차량 bringup 실행
3. RViz2 실행
4. 저장된 맵 확인
5. localization 실행
6. RViz2에서 차량 위치 확인
7. 초기 위치가 틀리면 조정

스크립트 기준:

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
터미널 4: 토픽 확인
cd ~/race_stack/f1tenth

source /opt/ros/foxy/setup.bash
source install/setup.bash

ros2 topic list
9. localization 실행 전 스크립트 확인

실제 어떤 launch 파일과 map 파일을 사용하는지 먼저 확인한다.

cd ~/race_stack/f1tenth

sed -n '1,200p' scripts/07_localization.sh

particle_filter 관련 launch 파일을 찾으려면:

find src/particle_filter -name "*.launch.py" -o -name "*.yaml" -o -name "*.yml" | sort

전체 레포에서 localization 관련 파일을 찾으려면:

find src -iname "*local*" -o -iname "*particle*" -o -iname "*amcl*" | sort
10. localization 실행

스크립트 사용:

cd ~/race_stack/f1tenth

source /opt/ros/foxy/setup.bash
source install/setup.bash

bash scripts/07_localization.sh

실행 후 아래 토픽이 나오는지 확인한다.

ros2 topic list

확인할 후보 토픽:

/map
/scan
/odom
/tf
/tf_static
/particle_filter/viz/inferred_pose
/particle_filter/viz/particles
/pose
/inferred_pose

실제 토픽 이름은 launch/config 파일에 따라 다를 수 있으므로 ros2 topic list 결과를 기준으로 확인한다.

11. RViz2에서 확인할 항목

RViz2에서 다음 항목을 확인한다.

Fixed Frame: map
Map: /map
LaserScan: /scan
TF: map, odom, base_link, laser
Pose 또는 inferred pose
Particle cloud

추천 순서:

1. Fixed Frame을 map으로 설정한다.
2. Map display를 추가하고 /map을 선택한다.
3. LaserScan display를 추가하고 /scan을 선택한다.
4. TF display를 켠다.
5. particle 또는 pose 관련 토픽을 추가한다.
6. 차량 위치가 실제 위치와 비슷한지 확인한다.
12. 초기 위치 설정

Particle Filter는 처음 시작할 때 차량의 초기 위치가 필요할 수 있다.

초기 위치가 틀리면 RViz2에서 차량 위치가 엉뚱한 곳에 보일 수 있다.

일반적으로 초기 위치는 다음 방법 중 하나로 설정한다.

RViz2의 2D Pose Estimate 도구 사용
config 파일의 초기 pose 값 수정
launch 파일에서 초기 pose 인자 전달
particle filter 노드가 제공하는 초기화 토픽 사용

RViz2에서 설정하는 경우:

1. RViz2 상단의 2D Pose Estimate 선택
2. 맵 위에서 차량이 실제로 있는 위치 클릭
3. 차량이 바라보는 방향으로 드래그
4. particle들이 주변으로 모이는지 확인

초기 위치를 주고 나서 차량을 아주 천천히 움직이면 particle이 실제 위치 근처로 수렴해야 한다.

13. 정상 동작 판단 기준

위치추정이 정상이라면 다음과 같이 보인다.

맵 위의 차량 위치가 실제 차량 위치와 비슷하다.
차량을 앞으로 움직이면 RViz2에서도 앞으로 움직인다.
차량을 회전시키면 RViz2에서도 같은 방향으로 회전한다.
LaserScan이 맵의 벽과 대체로 겹친다.
particle들이 차량 주변에 모인다.
시간이 지나도 pose가 갑자기 튀지 않는다.

특히 /scan이 맵의 벽과 잘 맞는지 확인하는 것이 중요하다.

14. 위치가 틀어질 때 확인할 것

위치가 실제와 다르면 아래를 확인한다.

[ ] 차량이 저장된 맵과 같은 환경에 있는가?
[ ] 맵 파일이 올바른가?
[ ] RViz2 Fixed Frame이 map인가?
[ ] /scan이 정상적으로 나오고 있는가?
[ ] /odom이 정상적으로 나오고 있는가?
[ ] /tf 연결이 정상인가?
[ ] 초기 위치를 제대로 줬는가?
[ ] LiDAR 방향이 실제와 반대로 설정되어 있지 않은가?
[ ] base_link와 laser frame 위치가 맞는가?
15. 주요 확인 명령
토픽 목록 확인
ros2 topic list
LiDAR 확인
ros2 topic echo /scan
odom 확인
ros2 topic echo /odom
map 확인
ros2 topic echo /map
TF 확인
ros2 run tf2_tools view_frames
노드 확인
ros2 node list
particle filter 노드 확인
ros2 node list | grep -i particle
pose 관련 토픽 찾기
ros2 topic list | grep -E "pose|particle|infer|local"
16. 자주 생기는 문제
16.1 맵이 안 보인다

확인할 것:

[ ] map server 또는 particle_filter가 맵을 publish하고 있는가?
[ ] /map 토픽이 나오는가?
[ ] RViz2 Fixed Frame이 map인가?
[ ] Map display topic이 /map인가?
[ ] map yaml 경로가 맞는가?

확인 명령:

ros2 topic list | grep map
ros2 topic echo /map
16.2 particle이 안 보인다

확인할 것:

[ ] particle 관련 display를 추가했는가?
[ ] particle topic 이름이 맞는가?
[ ] particle_filter 노드가 실행 중인가?
[ ] 초기 위치가 설정되어 있는가?

토픽 찾기:

ros2 topic list | grep -E "particle|pose|infer"
16.3 위치가 엉뚱한 곳에서 시작한다

가능한 원인:

초기 위치가 설정되지 않음
맵 파일이 다른 장소의 맵임
map origin이 예상과 다름
RViz2에서 2D Pose Estimate를 안 줌

해결:

1. RViz2 Fixed Frame을 map으로 설정한다.
2. 2D Pose Estimate로 실제 차량 위치를 찍는다.
3. 차량 방향을 실제 방향과 맞춘다.
4. 천천히 움직이며 particle이 모이는지 확인한다.
16.4 차량이 움직이면 위치가 튄다

가능한 원인:

odom이 불안정함
LiDAR scan이 끊김
TF가 끊기거나 frame 이름이 다름
차량이 너무 빠르게 움직임
바퀴가 미끄러짐

확인:

ros2 topic echo /odom
ros2 topic echo /scan
ros2 run tf2_tools view_frames

해결:

속도를 낮춘다.
급회전을 피한다.
odom과 LiDAR 연결을 확인한다.
TF frame 이름을 확인한다.
16.5 LaserScan과 맵이 겹치지 않는다

확인할 것:

[ ] 초기 위치가 맞는가?
[ ] 차량 방향이 맞는가?
[ ] laser frame 위치가 맞는가?
[ ] LiDAR가 차량에 제대로 고정되어 있는가?
[ ] 맵이 현재 환경과 같은가?

RViz2에서 /scan이 맵의 벽과 대체로 겹쳐야 한다.

겹치지 않으면 2D Pose Estimate를 다시 주거나, 맵과 실제 환경이 같은지 확인한다.

17. 좋은 위치추정을 위한 팁
1. SLAM으로 만든 맵과 같은 환경에서 테스트한다.
2. 시작 위치를 맵 위에서 정확히 맞춘다.
3. 처음에는 낮은 속도로 움직인다.
4. 급가속과 급회전을 피한다.
5. LiDAR가 볼 수 있는 벽이나 구조물이 있는 곳에서 시작한다.
6. 사람이 많이 움직이는 환경에서는 위치추정이 흔들릴 수 있다.
7. 유리, 검은 물체, 반사 물체가 많은 환경은 피한다.
18. 위치추정 완료 후 다음 단계

위치추정이 안정적으로 되면 다음 단계는 경로추종이다.

다음 문서:

docs/05_경로추종_pure_pursuit.md

경로추종 단계에서는 현재 위치를 기준으로 waypoint 또는 raceline을 따라 차량을 움직인다.

위치추정이 안정적이지 않으면 경로추종도 안정적으로 동작하지 않는다.

19. 이 문서에서 바꾸지 않는 것

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
