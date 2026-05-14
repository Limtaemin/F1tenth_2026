# 04. 위치추정 Particle Filter

이 문서는 저장된 맵 위에서 F1TENTH 차량의 위치를 추정하는 방법을 설명한다.

위치추정은 차량이 이미 만들어진 맵 안에서 “내가 지금 어디에 있는지”를 계산하는 과정이다. 이 레포에서는 `particle_filter` 패키지를 사용해 위치를 추정한다.

---

## 1. 이 문서의 목표

- 위치추정이 왜 필요한지 이해
- Particle Filter의 역할 이해
- 저장된 맵 준비
- bringup 실행
- RViz2 실행
- localization 실행
- RViz2에서 위치 확인
- 위치가 틀어질 때 확인할 것

---

## 2. 위치추정이 필요한 이유

SLAM 단계에서는 차량이 움직이면서 맵을 만든다.  
하지만 경로추종이나 장애물 회피를 하려면, 먼저 차량이 저장된 맵 위에서 현재 어디에 있는지 알아야 한다.

Pure Pursuit나 Stanley controller는 다음 정보가 필요하다.

- 차량의 현재 위치
- 차량의 현재 방향
- 주행할 waypoint 또는 raceline
- 맵 기준 좌표계

위치추정이 불안정하면 차량은 경로를 제대로 따라가지 못한다.

---

## 3. Particle Filter란?

Particle Filter는 여러 개의 후보 위치를 동시에 유지하면서, LiDAR 관측값과 맵을 비교해 가장 그럴듯한 차량 위치를 찾는 방식이다.

동작 흐름:

```text
1. 차량이 있을 법한 위치 후보를 여러 개 뿌린다.
2. 차량이 움직이면 후보 위치도 같이 움직인다.
3. LiDAR로 본 주변 모양과 저장된 맵을 비교한다.
4. 실제 관측과 잘 맞는 후보는 살린다.
5. 안 맞는 후보는 줄인다.
6. 최종적으로 가장 그럴듯한 위치를 추정한다.
```

---

## 4. 중요한 토픽과 frame

| 이름 | 역할 |
|---|---|
| `/scan` | LiDAR 스캔 데이터 |
| `/odom` | 차량 이동량 정보 |
| `/map` | 저장된 맵 |
| `/tf` | 좌표계 변환 |
| `map` | 전역 맵 좌표계 |
| `odom` | odometry 좌표계 |
| `base_link` | 차량 중심 좌표계 |
| `laser` | LiDAR 센서 좌표계 |

일반적인 frame 관계:

```text
map
 ↓
odom
 ↓
base_link
 ↓
laser
```

---

## 5. 실행 전 준비물

SLAM 단계에서 만든 맵이 있어야 한다.

```text
maps/saved/my_map.yaml
maps/saved/my_map.pgm
```

확인:

```bash
cd ~/race_stack/f1tenth
ls -lh maps/saved/
cat maps/saved/my_map.yaml
```

---

## 6. 실행 순서 요약

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

---

## 7. localization 실행 전 확인

실제 어떤 launch 파일과 map 파일을 사용하는지 먼저 확인한다.

```bash
sed -n '1,200p' scripts/07_localization.sh
find src/particle_filter -name "*.launch.py" -o -name "*.yaml" -o -name "*.yml" | sort
```

---

## 8. RViz2에서 확인할 항목

- Fixed Frame: `map`
- Map: `/map`
- LaserScan: `/scan`
- TF: `map`, `odom`, `base_link`, `laser`
- Pose 또는 inferred pose
- Particle cloud

관련 토픽을 찾으려면:

```bash
ros2 topic list | grep -E "pose|particle|infer|local"
```

---

## 9. 초기 위치 설정

초기 위치가 틀리면 RViz2에서 차량 위치가 엉뚱한 곳에 보일 수 있다.

RViz2에서 설정하는 방법:

1. RViz2 상단의 `2D Pose Estimate` 선택
2. 맵 위에서 차량이 실제로 있는 위치 클릭
3. 차량이 바라보는 방향으로 드래그
4. particle들이 주변으로 모이는지 확인

---

## 10. 정상 동작 판단 기준

정상이라면 다음과 같이 보인다.

- 맵 위의 차량 위치가 실제 차량 위치와 비슷하다.
- 차량을 앞으로 움직이면 RViz2에서도 앞으로 움직인다.
- 차량을 회전시키면 RViz2에서도 같은 방향으로 회전한다.
- LaserScan이 맵의 벽과 대체로 겹친다.
- particle들이 차량 주변에 모인다.
- 시간이 지나도 pose가 갑자기 튀지 않는다.

---

## 11. 주요 확인 명령

```bash
ros2 topic list
ros2 topic echo /scan
ros2 topic echo /odom
ros2 topic echo /map
ros2 run tf2_tools view_frames
ros2 node list
ros2 topic list | grep -E "pose|particle|infer|local"
```

---

## 12. 자주 생기는 문제

### 맵이 안 보인다

확인할 것:

- `/map` 토픽이 나오는가?
- RViz2 Fixed Frame이 `map`인가?
- Map display topic이 `/map`인가?
- map yaml 경로가 맞는가?

### 위치가 엉뚱한 곳에서 시작한다

해결:

1. RViz2 Fixed Frame을 `map`으로 설정한다.
2. `2D Pose Estimate`로 실제 차량 위치를 찍는다.
3. 차량 방향을 실제 방향과 맞춘다.
4. 천천히 움직이며 particle이 모이는지 확인한다.

### 차량이 움직이면 위치가 튄다

가능한 원인:

- odom이 불안정함
- LiDAR scan이 끊김
- TF가 끊기거나 frame 이름이 다름
- 차량이 너무 빠르게 움직임
- 바퀴가 미끄러짐

---

## 13. 위치추정 완료 후 다음 단계

위치추정이 안정적으로 되면 다음 단계는 경로추종이다.

다음 문서:

```text
docs/05_경로추종_pure_pursuit.md
```
