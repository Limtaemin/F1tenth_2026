# 06. 장애물회피 Stanley Avoidance

이 문서는 F1TENTH 차량에서 Stanley Controller 기반 경로추종과 LiDAR 기반 장애물 회피를 실행하는 방법을 설명한다.

Stanley avoidance 단계는 차량이 경로를 따라가면서 동시에 장애물을 피하려고 조향 명령을 만들기 때문에 실차에서 실행하기 전에는 반드시 낮은 속도와 넓은 공간에서 테스트해야 한다.

---

## 1. 이 문서의 목표

- Stanley Controller 개념 이해
- 장애물 회피 흐름 이해
- 실행 전 준비물 확인
- bringup 실행
- localization 실행
- Stanley avoidance 실행
- RViz2와 토픽으로 상태 확인
- 실차 안전 테스트 순서
- 자주 생기는 문제 해결

---

## 2. Stanley Controller란?

Stanley Controller는 차량이 목표 경로를 따라가도록 조향각을 계산하는 경로추종 알고리즘이다.

주로 두 가지 오차를 이용한다.

| 오차 | 의미 |
|---|---|
| heading error | 차량이 바라보는 방향과 경로 방향 사이의 각도 차이 |
| cross-track error | 차량이 경로에서 옆으로 얼마나 벗어났는지 |

Stanley Controller는 이 두 오차를 줄이는 방향으로 조향 명령을 만든다.

---

## 3. 장애물 회피의 기본 흐름

```text
LiDAR /scan 수신
  ↓
차량 앞쪽 장애물 거리 확인
  ↓
장애물이 없으면 Stanley 경로추종
  ↓
장애물이 있으면 회피 조향 계산
  ↓
/drive로 속도와 조향 명령 발행
```

---

## 4. 중요한 토픽과 frame

| 이름 | 역할 |
|---|---|
| `/drive` | 차량 구동 명령 |
| `/scan` | LiDAR 스캔 데이터 |
| `/odom` | 차량 odometry |
| `/map` | 맵 |
| `/tf` | 좌표계 변환 |
| `map` | 전역 맵 좌표계 |
| `odom` | odometry 좌표계 |
| `base_link` | 차량 중심 좌표계 |
| `laser` | LiDAR 센서 좌표계 |

---

## 5. 실행 전 준비물

```text
[ ] 차량 bringup이 정상 동작한다.
[ ] /scan 토픽이 나온다.
[ ] /odom 토픽이 나온다.
[ ] /tf가 정상이다.
[ ] SLAM으로 저장한 맵이 있다.
[ ] localization이 안정적으로 동작한다.
[ ] 경로 파일 또는 raceline 파일이 있다.
[ ] Pure Pursuit 또는 기본 경로추종이 먼저 테스트되어 있다.
```

Stanley avoidance 관련 파일 확인:

```bash
cd ~/race_stack/f1tenth
find src/stanley_avoidance -maxdepth 5 -type f | sort
find src/stanley_avoidance -name "*.yaml" -o -name "*.yml" | sort
grep -R "stanley\|obstacle\|avoid\|scan\|drive\|speed" -n src/stanley_avoidance
```

---

## 6. 실행 전 안전 체크리스트

```text
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
```

---

## 7. 실행 순서 요약

터미널 1: bringup

```bash
cd ~/race_stack/f1tenth
source /opt/ros/foxy/setup.bash
source install/setup.bash
bash scripts/02_bringup.sh
```

터미널 2: RViz2

```bash
cd ~/race_stack/f1tenth
source /opt/ros/foxy/setup.bash
source install/setup.bash
bash scripts/04_rviz.sh
```

터미널 3: localization

```bash
cd ~/race_stack/f1tenth
source /opt/ros/foxy/setup.bash
source install/setup.bash
bash scripts/07_localization.sh
```

터미널 4: Stanley avoidance

```bash
cd ~/race_stack/f1tenth
source /opt/ros/foxy/setup.bash
source install/setup.bash
bash scripts/09_stanley_avoidance.sh
```

---

## 8. RViz2에서 확인할 항목

- Fixed Frame: `map`
- Map: `/map`
- LaserScan: `/scan`
- TF: `map`, `odom`, `base_link`, `laser`
- 차량 현재 위치
- 주행 경로 또는 raceline
- 장애물 감지 영역
- 회피 목표점 또는 marker

관련 토픽 찾기:

```bash
ros2 topic list | grep -E "path|waypoint|goal|target|marker|stanley|obstacle|avoid"
```

---

## 9. 주요 파라미터

| 파라미터 | 의미 |
|---|---|
| `stanley_gain` | 경로 오차 보정 강도 |
| `target_speed` | 목표 속도 |
| `obstacle_distance` | 장애물 감지 기준 거리 |
| `avoidance_gain` | 회피 조향 강도 |
| `max_steering_angle` | 최대 조향 제한 |
| `wheelbase` | 차량 축간거리 |
| `waypoint_path` | waypoint 또는 raceline 파일 경로 |
| `drive_topic` | 제어 명령 출력 토픽 |
| `scan_topic` | LiDAR 입력 토픽 |

파라미터 찾기:

```bash
grep -R "gain\|speed\|velocity\|obstacle\|distance\|steer\|wheelbase" -n src/stanley_avoidance
```

---

## 10. 실차 테스트 순서

```text
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
```

확인:

```bash
ros2 topic echo /drive
ros2 topic echo /scan
```

---

## 11. 자주 생기는 문제

### 차량이 움직이지 않는다

확인할 것:

- bringup이 실행 중인가?
- Stanley avoidance 노드가 실행 중인가?
- localization이 실행 중인가?
- `/drive` 토픽이 발행되는가?
- VESC가 연결되어 있는가?
- 목표 속도가 0으로 되어 있지 않은가?

### 장애물을 못 피한다

가능한 원인:

- `/scan`이 정상적으로 들어오지 않음
- 장애물 감지 거리가 너무 짧음
- LiDAR 각도 범위 설정이 잘못됨
- 회피 조향 강도가 너무 작음
- 속도가 너무 빠름
- 장애물이 LiDAR에 잘 보이지 않음

### 장애물이 없는데도 회피한다

가능한 원인:

- LiDAR 노이즈
- 장애물 감지 거리 기준이 너무 큼
- 바닥이나 차량 일부를 장애물로 인식
- scan 각도 범위 설정이 넓거나 잘못됨
- 반사 물체 또는 유리

---

## 12. 다음 단계

Stanley avoidance까지 문서화했다면 다음 단계는 문제해결 문서다.

```text
docs/08_문제해결.md
```
