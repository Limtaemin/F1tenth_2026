# F1TENTH 한국어 실험용 Race Stack

이 레포는 F1TENTH 차량을 ROS2 환경에서 구동하고, 수동 조작, SLAM 맵 생성, 위치추정, 경로추종, 장애물 회피 실험을 하기 위한 자율주행 스택이다.

원본 레포를 기반으로 하되, 한국어 사용자와 실험 수업/연구 환경에서 이해하기 쉽도록 문서와 실행 스크립트를 정리하는 중이다.

---

## 1. 이 레포로 할 수 있는 것

- F1TENTH 차량 bringup
- VESC 모터/서보 제어
- LiDAR `/scan` 수신
- 조이스틱 수동 조작
- 웹 대시보드 기반 수동 조작
- RViz2를 통한 센서/맵 확인
- SLAM Toolbox 기반 맵 생성
- Particle Filter 기반 위치추정
- Pure Pursuit 기반 경로추종
- Stanley Controller 기반 경로추종 및 장애물 회피
- Safety Node 기반 충돌 방지

---

## 2. 전체 실행 흐름

일반적인 실험 순서는 다음과 같다.

```bash
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

3. 주요 폴더 구조
f1tenth/
├── docs/
│   ├── 00_전체_개요.md
│   ├── 01_설치_빌드.md
│   └── 07_config_설명.md
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
4. 폴더별 역할
폴더	역할
docs/	한국어 설명 문서
scripts/	자주 쓰는 실행 명령을 단순화한 스크립트
mission_control/	웹 대시보드, 키보드 조작, odom 튜닝 도구
src/f1tenth_system/	VESC, LiDAR, mux, teleop 등 차량 하드웨어 bringup
src/particle_filter/	저장된 맵에서 차량 위치 추정
src/pure_pursuit/	CSV raceline 기반 경로추종
src/safety_node/	충돌 위험 시 정지하는 안전 노드
src/stanley_avoidance/	Stanley 제어 + LiDAR 장애물 회피
src/state_estimation/	EKF 기반 odom/IMU 융합
5. 가장 먼저 봐야 할 문서

처음 보는 사람은 아래 순서로 읽으면 된다.

docs/00_전체_개요.md
docs/01_설치_빌드.md
docs/07_config_설명.md
6. 중요한 주의사항

이 레포는 실제 F1TENTH 차량을 움직일 수 있다.

특히 아래 토픽을 발행하는 코드는 차량을 실제로 구동할 수 있으므로 주의해야 한다.

/drive
/webop
/teleop

실차에서 실행하기 전에는 반드시 다음을 확인한다.

차량 바퀴가 바닥에서 떨어져 있는지
주변에 사람이 없는지
배터리 전압이 정상인지
VESC 연결이 정상인지
LiDAR /scan이 정상인지
/odom, /tf가 정상인지
emergency stop 또는 수동 정지 방법이 있는지
7. 현재 브랜치 목적

현재 브랜치:

korean-docs-structure

목적:

원본 기능 유지
한국어 문서 추가
실험 순서 정리
실행 스크립트 추가
config 파일 역할 설명
웹 대시보드 UI 한국어화 예정
8. 추천 작업 순서
1단계: 빌드 성공 확인
2단계: scripts 추가
3단계: 한국어 README/docs 추가
4단계: 웹 대시보드 한국어화
5단계: config 파일 주석 보강
6단계: 실험별 사용 가이드 작성

현재는 1~3단계 작업을 진행 중이다.