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
```

ROS2 환경 적용:

```bash
source /opt/ros/foxy/setup.bash
```

빌드:

```bash
bash scripts/01_build.sh
```

빌드 후 환경 적용:

```bash
source install/setup.bash
```

차량 bringup:

```bash
bash scripts/02_bringup.sh
```

웹 대시보드 실행:

```bash
bash scripts/03_web_dashboard.sh
```

브라우저 접속:

```text
http://localhost:5000
```

RViz2 실행:

```bash
bash scripts/04_rviz.sh
```

---

## 3. 전체 실험 흐름

```text
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
```

스크립트 기준 명령은 다음과 같다.

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
```

---

## 4. 주요 폴더 구조

```text
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
├── mission_control/
└── src/
```

---

## 5. 폴더별 역할

| 폴더 | 역할 |
|---|---|
| `docs/` | 한국어 설명 문서 |
| `scripts/` | 자주 쓰는 실행 명령을 단순화한 스크립트 |
| `mission_control/` | 웹 대시보드, 키보드 조작, odom 튜닝 도구 |
| `src/f1tenth_system/` | VESC, LiDAR, mux, teleop 등 차량 하드웨어 bringup |
| `src/particle_filter/` | 저장된 맵에서 차량 위치 추정 |
| `src/pure_pursuit/` | CSV raceline 기반 경로추종 |
| `src/safety_node/` | 충돌 위험 시 정지하는 안전 노드 |
| `src/stanley_avoidance/` | Stanley 제어와 LiDAR 장애물 회피 |
| `src/state_estimation/` | EKF 기반 odom/IMU 융합 관련 기능 |

---

## 6. 문서 읽는 순서

| 순서 | 문서 | 내용 |
|---|---|---|
| 1 | [docs/00_전체_개요.md](docs/00_전체_개요.md) | 전체 구조와 실험 흐름 |
| 2 | [docs/01_설치_빌드.md](docs/01_설치_빌드.md) | 설치, 의존성, 빌드 |
| 3 | [docs/02_수동조작_웹조작.md](docs/02_수동조작_웹조작.md) | 웹 대시보드와 수동 조작 |
| 4 | [docs/03_SLAM_맵생성.md](docs/03_SLAM_맵생성.md) | SLAM 맵 생성과 저장 |
| 5 | [docs/04_위치추정_particle_filter.md](docs/04_위치추정_particle_filter.md) | Particle Filter 위치추정 |
| 6 | [docs/05_경로추종_pure_pursuit.md](docs/05_경로추종_pure_pursuit.md) | Pure Pursuit 경로추종 |
| 7 | [docs/06_장애물회피_stanley_avoidance.md](docs/06_장애물회피_stanley_avoidance.md) | Stanley 장애물 회피 |
| 8 | [docs/07_config_설명.md](docs/07_config_설명.md) | config YAML 역할 |
| 9 | [docs/08_문제해결.md](docs/08_문제해결.md) | 자주 발생하는 문제 해결 |

---

## 7. 웹 대시보드

웹 대시보드는 `mission_control/dashboard.py`에서 실행된다.

```bash
cd ~/race_stack/f1tenth
source /opt/ros/foxy/setup.bash
source install/setup.bash
python3 mission_control/dashboard.py
```

브라우저 접속:

```text
http://localhost:5000
```

Flask가 없다는 오류가 나오면 아래를 실행한다.

```bash
python3 -m pip install --user flask
```

---

## 8. 중요한 ROS2 토픽

| 이름 | 의미 |
|---|---|
| `/drive` | 차량 최종 구동 명령 |
| `/webop` | 웹 대시보드 조작 명령 |
| `/teleop` | 조이스틱 또는 키보드 수동 조작 명령 |
| `/scan` | LiDAR 스캔 |
| `/odom` | 차량 odometry |
| `/map` | 맵 |
| `/tf` | 좌표계 변환 |
| `/tf_static` | 고정 좌표계 변환 |

---

## 9. 중요한 frame 이름

| frame | 의미 |
|---|---|
| `map` | 전역 맵 좌표계 |
| `odom` | odometry 좌표계 |
| `base_link` | 차량 기준 좌표계 |
| `laser` | LiDAR 센서 좌표계 |

---

## 10. 실차 실행 전 안전 체크리스트

```text
[ ] 차량 바퀴가 바닥에서 떨어져 있는가?
[ ] 주변에 사람이 없는가?
[ ] 배터리 전압이 정상인가?
[ ] VESC 연결이 정상인가?
[ ] LiDAR /scan이 정상인가?
[ ] /odom, /tf가 정상인가?
[ ] emergency stop 또는 수동 정지 방법이 있는가?
```

---

## 11. 정리 원칙

아래 파일은 레포에 올리지 않는 것을 원칙으로 한다.

```text
frames.gv
frames.pdf
build/
install/
log/
maps/saved/*.pgm
maps/saved/*.yaml
*.bak
*.tmp
```

`frames.gv`, `frames.pdf`는 `ros2 run tf2_tools view_frames` 실행 시 생성되는 결과물이다. 필요할 때마다 다시 만들 수 있으므로 Git에 저장하지 않는다.
