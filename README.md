# F1TENTH 한국어 실험용 Race Stack

이 레포는 F1TENTH 차량을 ROS2 환경에서 구동하고, 수동 조작, 웹 조작, SLAM 맵 생성, 위치추정, 경로추종, 장애물 회피 실험을 하기 위한 자율주행 스택이다.

원본 레포의 ROS2 패키지 구조는 유지하면서, 한국어 사용자와 실험 수업/연구 환경에서 이해하기 쉽도록 문서와 실행 스크립트를 정리하고 있다.

> 기준 레포: `subratpp/f1tenth`  
> 현재 작업 브랜치: `korean-docs-structure`

---

## 1. 이 레포로 할 수 있는 것

- F1TENTH 차량 bringup
- VESC 기반 모터/서보 제어
- LiDAR `/scan` 수신
- 조이스틱 또는 키보드 기반 수동 조작
- 웹 대시보드 기반 수동 조작
- RViz2를 통한 센서, TF, 맵 확인
- SLAM Toolbox 기반 맵 생성
- Particle Filter 기반 위치추정
- Pure Pursuit 기반 경로추종
- Stanley Controller 기반 경로추종 및 장애물 회피
- Safety Node 기반 충돌 방지

---

## 2. 빠른 시작

작업 경로는 아래를 기준으로 설명한다.

```bash
cd ~/race_stack/f1tenth

ROS2 환경 적용:

source /opt/ros/foxy/setup.bash

빌드:

bash scripts/01_build.sh

빌드 후 환경 적용:

source install/setup.bash

차량 bringup:

bash scripts/02_bringup.sh

웹 대시보드 실행:

bash scripts/03_web_dashboard.sh

브라우저 접속:

http://localhost:5000

RViz2 실행:

bash scripts/04_rviz.sh
3. 전체 실험 흐름

일반적인 실험 순서는 다음과 같다.

빌드
  ↓
차량 bringup
  ↓
웹 대시보드 또는 수동 조작 확인
  ↓
RViz2로 /scan, /odom, /tf 확인
  ↓
SLAM으로 맵 생성
  ↓
맵 저장
  ↓
저장된 맵 기반 위치추정
  ↓
Pure Pursuit 경로추종
  ↓
Stanley 장애물 회피 주행

스크립트 기준 명령은 다음과 같다.

# 1. 빌드
bash scripts/01_build.sh

# 2. 환경 적용
source install/setup.bash

# 3. 차량 bringup
bash scripts/02_bringup.sh

# 4. 웹 대시보드 실행
bash scripts/03_web_dashboard.sh

# 5. RViz2 실행
bash scripts/04_rviz.sh

# 6. SLAM 맵 생성
bash scripts/05_slam_start.sh

# 7. 맵 저장
bash scripts/06_save_map.sh maps/saved/my_map

# 8. 위치추정 실행
bash scripts/07_localization.sh

# 9. Pure Pursuit 경로추종
bash scripts/08_pure_pursuit.sh

# 10. Stanley 장애물 회피 주행
bash scripts/09_stanley_avoidance.sh
4. 주요 폴더 구조
f1tenth/
├── docs/
│   ├── 00_전체_개요.md
│   ├── 01_설치_빌드.md
│   ├── 02_수동조작_웹조작.md
│   ├── 03_SLAM_맵생성.md
│   ├── 04_위치추정_particle_filter.md
│   ├── 05_경로추종_pure_pursuit.md
│   ├── 06_장애물회피_stanley_avoidance.md
│   ├── 07_config_설명.md
│   └── 08_문제해결.md
│
├── scripts/
│   ├── 01_build.sh
│   ├── 02_bringup.sh
│   ├── 03_web_dashboard.sh
│   ├── 04_rviz.sh
│   ├── 05_slam_start.sh
│   ├── 06_save_map.sh
│   ├── 07_localization.sh
│   ├── 08_pure_pursuit.sh
│   └── 09_stanley_avoidance.sh
│
├── mission_control/
│   ├── dashboard.py
│   ├── key_teleop.py
│   └── odom_tuner.py
│
└── src/
    ├── f1tenth_system/
    ├── particle_filter/
    ├── pure_pursuit/
    ├── safety_node/
    ├── stanley_avoidance/
    └── state_estimation/
5. 폴더별 역할
폴더역할
docs/0한국어 설명 문서
scripts/0자주 쓰는 실행 명령을 단순화한 스크립트
mission_control/웹 대시보드, 키보드 조작, odom 튜닝 도구
src/f1tenth_system/VESC, LiDAR, mux, teleop 등 차량 하드웨어 bringup
src/particle_filter/저장된 맵에서 차량 위치 추정
src/pure_pursuit/CSV raceline 기반 경로추종
src/safety_node/충돌 위험 시 정지하는 안전 노드
src/stanley_avoidance/Stanley 제어와 LiDAR 장애물 회피
src/state_estimation/EKF 기반 odom/IMU 융합 관련 기능
6. 문서 읽는 순서

처음 보는 사람은 아래 순서로 읽으면 된다.

순서문서내용
1docs/00_전체_개요.md
전체 구조와 실험 흐름
2docs/01_설치_빌드.md
설치, 의존성, 빌드
3docs/02_수동조작_웹조작.md
웹 대시보드와 수동 조작
4docs/03_SLAM_맵생성.md
SLAM 맵 생성과 저장
5docs/04_위치추정_particle_filter.md
Particle Filter 위치추정
6docs/05_경로추종_pure_pursuit.md
Pure Pursuit 경로추종
7docs/06_장애물회피_stanley_avoidance.md
Stanley 장애물 회피
8docs/07_config_설명.md
config YAML 역할
9docs/08_문제해결.md
자주 발생하는 문제 해결
7. 웹 대시보드

웹 대시보드는 mission_control/dashboard.py에서 실행된다.

실행:

cd ~/race_stack/f1tenth

source /opt/ros/foxy/setup.bash
source install/setup.bash

python3 mission_control/dashboard.py

브라우저 접속:

http://localhost:5000

웹 대시보드에서 할 수 있는 것:

차량 Bringup 시작/정지
SLAM 시작/정지
맵 저장
수동 모드 / 자율주행 모드 전환
/webop 기반 수동 조작
최대 속도 / 최대 조향 제한 설정

Flask가 없다는 오류가 나오면 아래를 실행한다.

python3 -m pip install --user flask
8. 중요한 ROS2 토픽

아래 이름들은 여러 노드가 함께 사용하므로 함부로 바꾸면 안 된다.

이름의미
/drive차량 최종 구동 명령
/webop웹 대시보드 조작 명령
/teleop조이스틱 또는 키보드 수동 조작 명령
/scanLiDAR 스캔
/odom차량 odometry
/map맵
/tf좌표계 변환
/tf_static고정 좌표계 변환
9. 중요한 frame 이름

아래 frame 이름도 여러 설정 파일과 launch 파일에서 공유될 수 있다.

frame의미
maps/전역 맵 좌표계
odomodometry 좌표계
base_link차량 기준 좌표계
laserLiDAR 센서 좌표계

주의할 점:

frame 이름을 바꾸면 RViz2, SLAM, localization, controller가 함께 깨질 수 있다.
이름 변경은 문서 정리 단계에서 하지 않는다.
먼저 전체 흐름이 정상 동작하는 것을 확인한 뒤에만 변경한다.
10. 실차 실행 전 안전 체크리스트

이 레포는 실제 F1TENTH 차량을 움직일 수 있다.

특히 아래 토픽을 발행하는 코드는 차량을 실제로 구동할 수 있으므로 주의해야 한다.

/drive
/webop
/teleop

실차에서 실행하기 전에는 반드시 다음을 확인한다.

[ ] 차량 바퀴가 바닥에서 떨어져 있는가?
[ ] 주변에 사람이 없는가?
[ ] 배터리 전압이 정상인가?
[ ] VESC 연결이 정상인가?
[ ] LiDAR /scan이 정상인가?
[ ] /odom, /tf가 정상인가?
[ ] emergency stop 또는 수동 정지 방법이 있는가?
11. 자주 쓰는 확인 명령

토픽 목록:

ros2 topic list

LiDAR 확인:

ros2 topic echo /scan

odom 확인:

ros2 topic echo /odom

drive 명령 확인:

ros2 topic echo /drive

TF 확인:

ros2 run tf2_tools view_frames

노드 확인:

ros2 node list

launch 파일 찾기:

find src -name "*.launch.py" | sort

config 파일 찾기:

find src -name "*.yaml" -o -name "*.yml" | sort
12. 현재 브랜치 목적

현재 브랜치:

korean-docs-structure

목적:

원본 ROS2 패키지 구조 유지
한국어 문서 추가
실험 순서 정리
실행 스크립트 추가
config 파일 역할 설명
웹 대시보드 UI 한국어화
실험자가 바로 따라 할 수 있는 문서 세트 구성

현재는 패키지 구조를 크게 바꾸지 않고, 문서와 실행 흐름을 정리하는 단계다.

13. 정리 원칙

아래 파일은 레포에 올리지 않는 것을 원칙으로 한다.

frames.gv
frames.pdf
build/
install/
log/
maps/saved/*.pgm
maps/saved/*.yaml
*.bak
*.tmp

frames.gv, frames.pdf는 ros2 run tf2_tools view_frames 실행 시 생성되는 결과물이다. 필요할 때마다 다시 만들 수 있으므로 Git에 저장하지 않는다.

맵 파일도 실험 환경마다 달라지므로 기본적으로 Git에 저장하지 않는다. 필요한 예제 맵이 생기면 별도 폴더와 설명을 만들어 관리한다.
