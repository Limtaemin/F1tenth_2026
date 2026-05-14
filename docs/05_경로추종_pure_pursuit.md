# 05. 경로추종 Pure Pursuit

이 문서는 F1TENTH 차량이 waypoint 또는 raceline을 따라 주행하도록 하는 Pure Pursuit 경로추종 방법을 설명한다.

Pure Pursuit는 차량 앞쪽의 목표점을 바라보며 조향각을 계산하는 경로추종 알고리즘이다.

---

## 1. 이 문서의 목표

- Pure Pursuit 개념 이해
- waypoint / raceline 파일 역할 이해
- 위치추정 실행
- Pure Pursuit 실행
- RViz2에서 경로와 차량 위치 확인
- 속도와 lookahead distance 조정
- 실차 테스트 순서
- 자주 생기는 문제 해결

---

## 2. Pure Pursuit란?

Pure Pursuit는 차량이 현재 위치에서 일정 거리 앞에 있는 목표점을 선택하고, 그 목표점을 향해 조향하는 방식이다.

흐름:

```text
1. 차량의 현재 위치를 확인한다.
2. 주행 경로에서 차량 앞쪽의 목표점을 찾는다.
3. 차량이 그 목표점을 향하도록 조향각을 계산한다.
4. 계산한 속도와 조향 명령을 /drive로 보낸다.
5. 이 과정을 계속 반복한다.
```

목표점을 찾는 거리를 `lookahead distance`라고 한다.

---

## 3. 필요한 정보

| 항목 | 설명 |
|---|---|
| 현재 차량 위치 | localization 또는 particle filter 결과 |
| 현재 차량 방향 | `map → base_link` 또는 관련 TF |
| 주행 경로 | waypoint 또는 raceline CSV |
| 목표 속도 | 차량이 따라갈 속도 |
| lookahead distance | 차량 앞쪽 목표점을 선택하는 거리 |
| `/drive` | 최종 차량 제어 명령 |

---

## 4. 실행 전 준비물

```text
[ ] 차량 bringup이 정상 동작한다.
[ ] /scan 토픽이 나온다.
[ ] /odom 토픽이 나온다.
[ ] /tf가 정상이다.
[ ] SLAM으로 저장한 맵이 있다.
[ ] localization이 안정적으로 동작한다.
[ ] waypoint 또는 raceline 파일이 있다.
```

waypoint 또는 raceline 파일 찾기:

```bash
cd ~/race_stack/f1tenth
find . -iname "*.csv" -o -iname "*waypoint*" -o -iname "*raceline*"
```

Pure Pursuit 관련 파일 확인:

```bash
find src/pure_pursuit -name "*.yaml" -o -name "*.yml" -o -name "*.py" -o -name "*.cpp" | sort
```

---

## 5. 실행 순서 요약

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

터미널 4: Pure Pursuit

```bash
cd ~/race_stack/f1tenth
source /opt/ros/foxy/setup.bash
source install/setup.bash
bash scripts/08_pure_pursuit.sh
```

---

## 6. 실행 전 스크립트 확인

```bash
sed -n '1,200p' scripts/08_pure_pursuit.sh
find src/pure_pursuit -maxdepth 4 -type f | sort
find . -iname "*.csv" | sort
```

---

## 7. RViz2에서 확인할 항목

- Fixed Frame: `map`
- Map: `/map`
- LaserScan: `/scan`
- TF: `map`, `odom`, `base_link`, `laser`
- 차량 현재 위치
- waypoint 또는 raceline
- 목표점 lookahead point

관련 토픽 찾기:

```bash
ros2 topic list | grep -E "path|waypoint|goal|target|pure|marker"
```

---

## 8. 주요 파라미터

| 파라미터 | 의미 |
|---|---|
| `lookahead_distance` | 차량 앞쪽 목표점을 찾는 거리 |
| `velocity` 또는 `target_speed` | 목표 속도 |
| `wheelbase` | 차량 축간거리 |
| `waypoint_path` | waypoint CSV 파일 경로 |
| `drive_topic` | 제어 명령 출력 토픽 |
| `map_frame` | 맵 기준 frame |
| `base_frame` | 차량 기준 frame |

파라미터 찾기:

```bash
grep -R "lookahead" -n src/pure_pursuit
grep -R "velocity\|speed" -n src/pure_pursuit
grep -R "waypoint\|raceline\|csv" -n src/pure_pursuit
```

---

## 9. lookahead distance 조정

| lookahead distance | 특징 |
|---|---|
| 너무 작음 | 조향이 민감하고 흔들릴 수 있음 |
| 적당함 | 경로를 안정적으로 따라감 |
| 너무 큼 | 코너를 크게 돌거나 경로를 벗어날 수 있음 |

처음에는 작은 속도와 함께 보수적인 값을 사용한다.

---

## 10. 실차 테스트 순서

```text
1. 차량 바퀴를 바닥에서 띄운다.
2. bringup을 실행한다.
3. localization을 실행한다.
4. RViz2에서 차량 위치가 맞는지 확인한다.
5. Pure Pursuit를 실행한다.
6. /drive 명령이 정상 범위인지 echo로 확인한다.
7. 정지 또는 emergency stop 방법을 준비한다.
8. 바퀴를 바닥에 내린다.
9. 아주 낮은 속도로 짧게 주행한다.
10. 문제가 있으면 즉시 정지한다.
```

`/drive` 확인:

```bash
ros2 topic echo /drive
```

---

## 11. 자주 생기는 문제

### 차량이 움직이지 않는다

확인할 것:

- bringup이 실행 중인가?
- Pure Pursuit 노드가 실행 중인가?
- localization이 실행 중인가?
- `/drive` 토픽이 발행되는가?
- VESC가 연결되어 있는가?
- mux가 `/drive` 명령을 받아들이는가?

### 차량이 엉뚱한 방향으로 간다

가능한 원인:

- 차량 위치추정이 틀림
- waypoint 좌표계가 현재 map과 다름
- 차량 시작 방향이 경로 방향과 다름
- 좌표 frame이 잘못 설정됨
- 조향 부호가 반대로 적용됨

### 차량이 경로 주변에서 흔들린다

해결:

- 속도를 낮춘다.
- lookahead distance를 조금 키운다.
- localization이 안정적인지 확인한다.
- waypoint가 부드러운지 확인한다.

---

## 12. 다음 단계

Pure Pursuit 경로추종이 안정적으로 동작하면 다음 단계는 Stanley 기반 장애물 회피다.

```text
docs/06_장애물회피_stanley_avoidance.md
```
