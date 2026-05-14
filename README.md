# F1TENTH 한국어 실험용 Race Stack

이 레포는 F1TENTH 차량을 ROS2 환경에서 구동하고, 수동 조작, 웹 조작, SLAM 맵 생성, 위치추정, 경로추종, 장애물 회피 실험을 하기 위한 자율주행 스택이다.

원본 레포의 ROS2 패키지 구조는 유지하면서, 한국어 사용자와 실험 수업/연구 환경에서 이해하기 쉽도록 문서와 실행 스크립트를 정리하고 있다.

> 기준 레포: `subratpp/f1tenth`  
> 현재 private 작업 레포: `Limtaemin/F1tenth_2026`

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

## 2. 이 레포의 큰 구조

이 레포는 크게 4개 영역으로 보면 된다.

| 영역 | 설명 |
|---|---|
| `src/` | 실제 ROS2 패키지 코드 |
| `scripts/` | 자주 쓰는 실행 명령을 단순화한 스크립트 |
| `mission_control/` | 웹 대시보드, 키보드 조작, odom 튜닝 도구 |
| `docs/` | 한국어 설명 문서 |

---

## 3. 주요 기능 한눈에 보기

| 기능 | 관련 패키지/파일 | 설명 |
|---|---|---|
| 차량 bringup | `src/f1tenth_system/` | VESC, LiDAR, mux, teleop 등 차량 기본 실행 |
| 웹 조작 | `mission_control/dashboard.py` | 브라우저에서 차량 상태 확인 및 `/webop` 조작 |
| 수동 조작 | `joy_teleop`, `key_teleop.py` | 조이스틱/키보드로 차량 조작 |
| SLAM | `slam_toolbox`, `f1tenth_online_async.yaml` | LiDAR와 odom으로 맵 생성 |
| 위치추정 | `src/particle_filter/` | 저장된 맵 위에서 차량 위치 추정 |
| 경로추종 | `src/pure_pursuit/` | waypoint/raceline을 따라 주행 |
| 장애물 회피 | `src/stanley_avoidance/` | Stanley 제어와 LiDAR 기반 회피 |
| 안전 정지 | `src/safety_node/` | 충돌 위험이 있을 때 정지 명령 생성 |
| 상태추정 | `src/state_estimation/` | odom, IMU 등 상태추정 관련 기능 |

---

## 4. 빠른 시작

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

## 5. 전체 실험 흐름

일반적인 실험 순서는 다음과 같다.

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

---

## 6. 실행 명령어 전체 목록

아래 명령은 각각 다른 터미널에서 실행하는 경우가 많다.

### 6.1 빌드

```bash
cd ~/race_stack/f1tenth
source /opt/ros/foxy/setup.bash
bash scripts/01_build.sh
source install/setup.bash
```

### 6.2 차량 bringup

VESC, LiDAR, mux, teleop 등 차량 기본 노드를 실행한다.

```bash
cd ~/race_stack/f1tenth
source /opt/ros/foxy/setup.bash
source install/setup.bash
bash scripts/02_bringup.sh
```

### 6.3 웹 대시보드

브라우저에서 수동 조작, bringup 실행, SLAM 실행, 맵 저장 등을 할 수 있다.

```bash
cd ~/race_stack/f1tenth
source /opt/ros/foxy/setup.bash
source install/setup.bash
bash scripts/03_web_dashboard.sh
```

브라우저:

```text
http://localhost:5000
```

Flask가 없다는 오류가 나오면 아래를 실행한다.

```bash
python3 -m pip install --user flask
```

### 6.4 RViz2

LiDAR, map, TF, 차량 위치를 확인한다.

```bash
cd ~/race_stack/f1tenth
source /opt/ros/foxy/setup.bash
source install/setup.bash
bash scripts/04_rviz.sh
```

### 6.5 SLAM 맵 생성

LiDAR와 odom을 이용해 새로운 맵을 만든다.

```bash
cd ~/race_stack/f1tenth
source /opt/ros/foxy/setup.bash
source install/setup.bash
bash scripts/05_slam_start.sh
```

### 6.6 맵 저장

SLAM으로 만든 맵을 저장한다.

```bash
cd ~/race_stack/f1tenth
source /opt/ros/foxy/setup.bash
source install/setup.bash
bash scripts/06_save_map.sh maps/saved/my_map
```

저장 결과 예시:

```text
maps/saved/my_map.yaml
maps/saved/my_map.pgm
```

### 6.7 위치추정 Particle Filter

저장된 맵 위에서 차량 위치를 추정한다.

```bash
cd ~/race_stack/f1tenth
source /opt/ros/foxy/setup.bash
source install/setup.bash
bash scripts/07_localization.sh
```

### 6.8 Pure Pursuit 경로추종

waypoint 또는 raceline을 따라 차량이 주행하도록 한다.

```bash
cd ~/race_stack/f1tenth
source /opt/ros/foxy/setup.bash
source install/setup.bash
bash scripts/08_pure_pursuit.sh
```

### 6.9 Stanley 장애물 회피

Stanley Controller 기반 경로추종과 LiDAR 기반 장애물 회피를 실행한다.

```bash
cd ~/race_stack/f1tenth
source /opt/ros/foxy/setup.bash
source install/setup.bash
bash scripts/09_stanley_avoidance.sh
```

---

## 7. 기능별 설명

### 7.1 Bringup이란?

Bringup은 차량을 움직이기 위해 필요한 기본 노드들을 실행하는 단계다.

보통 아래 기능들이 포함된다.

- VESC 연결
- LiDAR 연결
- odom 발행
- `/scan` 발행
- `/tf` 발행
- 조이스틱/웹 조작 입력 처리
- mux를 통한 최종 `/drive` 명령 선택

bringup이 정상이어야 SLAM, localization, path following이 모두 정상적으로 동작한다.

확인 명령:

```bash
ros2 topic list
ros2 topic echo /scan
ros2 topic echo /odom
ros2 run tf2_tools view_frames
```

---

### 7.2 웹 대시보드는 무엇인가?

웹 대시보드는 `mission_control/dashboard.py`에서 실행되는 Flask 기반 조작 화면이다.

웹 대시보드에서 할 수 있는 것:

- 차량 Bringup 시작/정지
- SLAM 시작/정지
- 맵 저장
- 수동 모드 / 자율주행 모드 전환
- `/webop` 기반 수동 조작
- 최대 속도 / 최대 조향 제한 설정

웹 조작 흐름:

```text
브라우저 버튼
  ↓
mission_control/dashboard.py
  ↓
/webop
  ↓
mux
  ↓
/drive
  ↓
VESC
```

---

### 7.3 SLAM은 무엇인가?

SLAM은 차량이 움직이면서 주변 환경의 지도를 만드는 기능이다.

이 레포에서는 LiDAR `/scan`, odom `/odom`, TF `/tf`를 이용해 맵을 만든다.

SLAM에서 중요한 것:

- `/scan`이 정상적으로 나오는가?
- `/odom`이 정상적으로 나오는가?
- `map`, `odom`, `base_link`, `laser` frame이 연결되어 있는가?
- 차량을 너무 빠르게 움직이지 않는가?

결과물:

```text
my_map.yaml
my_map.pgm
```

이 맵은 이후 localization과 경로추종에서 사용된다.

---

### 7.4 Particle Filter 위치추정은 무엇인가?

Particle Filter는 저장된 맵 위에서 차량이 현재 어디에 있는지 추정하는 기능이다.

간단한 원리:

```text
여러 위치 후보 particle을 뿌림
  ↓
차량 움직임과 LiDAR 관측을 반영
  ↓
맵과 잘 맞는 후보를 남김
  ↓
현재 차량 위치를 추정
```

위치추정이 안정적이어야 Pure Pursuit나 Stanley가 제대로 동작한다.

RViz2에서 확인할 것:

- 차량 위치가 실제 위치와 비슷한가?
- `/scan`이 맵의 벽과 겹치는가?
- particle들이 차량 주변에 모이는가?
- pose가 갑자기 튀지 않는가?

---

### 7.5 Pure Pursuit는 무엇인가?

Pure Pursuit는 차량 앞쪽의 목표점을 바라보며 경로를 따라가는 알고리즘이다.

동작 흐름:

```text
현재 차량 위치 확인
  ↓
경로 위에서 앞쪽 목표점 선택
  ↓
목표점을 향하도록 조향각 계산
  ↓
/drive 발행
```

중요한 파라미터:

| 파라미터 | 의미 |
|---|---|
| `lookahead_distance` | 차량이 바라볼 앞쪽 목표점 거리 |
| `target_speed` 또는 `velocity` | 목표 속도 |
| `waypoint_path` | 따라갈 CSV 경로 파일 |
| `wheelbase` | 차량 축간거리 |

처음 실차 테스트에서는 반드시 낮은 속도로 시작한다.

---

### 7.6 Stanley Controller는 무엇인가?

Stanley Controller는 경로 방향과 차량 방향의 차이, 그리고 차량이 경로에서 얼마나 옆으로 벗어났는지를 이용해 조향각을 계산하는 경로추종 알고리즘이다.

주요 오차:

| 오차 | 의미 |
|---|---|
| heading error | 차량 방향과 경로 방향의 차이 |
| cross-track error | 차량이 경로에서 옆으로 벗어난 거리 |

Stanley는 이 두 오차를 줄이는 방향으로 조향한다.

---

### 7.7 Stanley Avoidance는 무엇인가?

Stanley Avoidance는 Stanley 경로추종에 LiDAR 기반 장애물 회피를 더한 기능이다.

동작 흐름:

```text
현재 위치 추정
  ↓
Stanley 경로추종 조향 계산
  ↓
/scan으로 앞쪽 장애물 확인
  ↓
장애물이 있으면 회피 조향 보정
  ↓
/drive 발행
```

처음 테스트할 때 주의할 점:

- 사람을 장애물로 세워 테스트하지 않는다.
- 부드러운 박스나 콘 같은 물체를 사용한다.
- 속도를 낮게 설정한다.
- emergency stop 방법을 준비한다.

---

### 7.8 Safety Node는 무엇인가?

Safety Node는 충돌 위험이 있을 때 차량을 멈추기 위한 안전 노드다.

보통 LiDAR `/scan`과 차량 속도 정보를 보고, 앞쪽 장애물과 충돌할 가능성이 크면 정지 명령을 만든다.

일반적인 개념:

```text
/scan으로 앞쪽 거리 확인
  ↓
현재 속도와 거리로 충돌 가능성 계산
  ↓
위험하면 정지 명령 발행
```

Safety Node에서 자주 등장하는 개념은 TTC이다.

| 용어 | 의미 |
|---|---|
| TTC | Time To Collision, 충돌까지 남은 시간 |
| threshold | 위험하다고 판단하는 기준값 |
| emergency brake | 위험 시 정지 명령 |

주의할 점:

- 실차 테스트에서 Safety Node는 가능하면 비활성화하지 않는다.
- Safety Node가 있어도 완전한 안전을 보장하지는 않는다.
- 항상 낮은 속도에서 테스트하고, 수동 정지 방법을 준비해야 한다.

---

## 8. 주요 폴더 구조

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

## 9. 폴더별 역할

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

## 10. 문서 읽는 순서

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

## 11. 중요한 ROS2 토픽

아래 이름들은 여러 노드가 함께 사용하므로 함부로 바꾸면 안 된다.

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

## 12. 중요한 frame 이름

| frame | 의미 |
|---|---|
| `map` | 전역 맵 좌표계 |
| `odom` | odometry 좌표계 |
| `base_link` | 차량 기준 좌표계 |
| `laser` | LiDAR 센서 좌표계 |

frame 이름을 바꾸면 RViz2, SLAM, localization, controller가 함께 깨질 수 있다.

---

## 13. 실차 실행 전 안전 체크리스트

이 레포는 실제 F1TENTH 차량을 움직일 수 있다.

특히 아래 토픽을 발행하는 코드는 차량을 실제로 구동할 수 있으므로 주의해야 한다.

```text
/drive
/webop
/teleop
```

실차에서 실행하기 전에는 반드시 다음을 확인한다.

```text
[ ] 차량 바퀴가 바닥에서 떨어져 있는가?
[ ] 주변에 사람이 없는가?
[ ] 배터리 전압이 정상인가?
[ ] VESC 연결이 정상인가?
[ ] LiDAR /scan이 정상인가?
[ ] /odom, /tf가 정상인가?
[ ] emergency stop 또는 수동 정지 방법이 있는가?
[ ] 목표 속도가 낮게 설정되어 있는가?
```

---

## 14. 자주 쓰는 확인 명령

| 목적 | 명령 |
|---|---|
| 토픽 목록 | `ros2 topic list` |
| LiDAR 확인 | `ros2 topic echo /scan` |
| odom 확인 | `ros2 topic echo /odom` |
| drive 명령 확인 | `ros2 topic echo /drive` |
| TF 확인 | `ros2 run tf2_tools view_frames` |
| 노드 확인 | `ros2 node list` |
| launch 파일 찾기 | `find src -name "*.launch.py" | sort` |
| config 파일 찾기 | `find src -name "*.yaml" -o -name "*.yml" | sort` |

---

## 15. 정리 원칙

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

맵 파일도 실험 환경마다 달라지므로 기본적으로 Git에 저장하지 않는다. 필요한 예제 맵이 생기면 별도 폴더와 설명을 만들어 관리한다.
