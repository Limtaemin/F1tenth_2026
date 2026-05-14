# 03. SLAM 맵 생성

이 문서는 F1TENTH 차량에서 LiDAR와 odom을 이용해 SLAM 맵을 생성하고 저장하는 방법을 설명한다.

SLAM은 `Simultaneous Localization and Mapping`의 약자로, 차량이 움직이면서 주변 환경의 지도를 만들고 동시에 자기 위치를 추정하는 과정이다.

---

## 1. 이 문서의 목표

- SLAM 실행 전 확인할 것
- bringup 실행
- RViz2 실행
- SLAM 실행
- 차량을 천천히 움직이며 맵 생성
- 맵 저장
- 저장된 map 파일 확인
- 자주 생기는 문제 해결

---

## 2. SLAM에서 중요한 토픽과 frame

| 이름 | 역할 |
|---|---|
| `/scan` | LiDAR 스캔 데이터 |
| `/odom` | 차량 이동량 정보 |
| `/tf` | 좌표계 변환 |
| `map` | 생성되는 지도 좌표계 |
| `odom` | odometry 좌표계 |
| `base_link` | 차량 중심 좌표계 |
| `laser` | LiDAR 센서 좌표계 |

일반적인 관계:

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

## 3. 실행 전 안전 체크리스트

```text
[ ] 차량 배터리가 충분한가?
[ ] VESC가 정상 연결되어 있는가?
[ ] LiDAR가 정상 연결되어 있는가?
[ ] 주변에 사람이 없는가?
[ ] 차량을 천천히 움직일 공간이 있는가?
[ ] 긴급 정지 방법을 알고 있는가?
[ ] 최대 속도를 낮게 제한했는가?
```

---

## 4. 실행 순서 요약

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

터미널 3: SLAM

```bash
cd ~/race_stack/f1tenth
source /opt/ros/foxy/setup.bash
source install/setup.bash
bash scripts/05_slam_start.sh
```

맵 저장:

```bash
cd ~/race_stack/f1tenth
source /opt/ros/foxy/setup.bash
source install/setup.bash
bash scripts/06_save_map.sh maps/saved/my_map
```

---

## 5. bringup 확인

```bash
ros2 topic list
```

확인할 주요 토픽:

```text
/scan
/odom
/tf
/tf_static
/drive
/webop
```

LiDAR 확인:

```bash
ros2 topic echo /scan
```

odom 확인:

```bash
ros2 topic echo /odom
```

TF 확인:

```bash
ros2 run tf2_tools view_frames
```

---

## 6. RViz2에서 확인할 항목

- Fixed Frame: `map` 또는 `odom`
- LaserScan: `/scan`
- Map: `/map`
- TF: `map`, `odom`, `base_link`, `laser`

처음에는 `/map`이 없거나 비어 있을 수 있다.  
SLAM이 실행되고 차량이 움직이기 시작하면 `/map`이 생성된다.

---

## 7. SLAM 실행

```bash
bash scripts/05_slam_start.sh
```

실제 실행 명령은 스크립트 내용을 기준으로 확인한다.

```bash
sed -n '1,160p' scripts/05_slam_start.sh
```

---

## 8. SLAM 중 차량 움직이는 방법

웹 대시보드를 사용할 경우:

```bash
python3 mission_control/dashboard.py
```

브라우저:

```text
http://localhost:5000
```

권장 설정:

```text
주행 모드: 수동 조작
최대 속도: 0.2 이하
최대 조향: 0.10 ~ 0.20 정도
```

좋은 맵을 만들기 위한 팁:

- 천천히 움직인다.
- 급가속, 급회전을 피한다.
- 벽이나 장애물 주변을 여러 각도에서 본다.
- 같은 구역을 한 번 이상 지나간다.
- LiDAR가 보기 어려운 유리, 검은 물체, 반사 물체는 주의한다.

---

## 9. 맵 저장

```bash
bash scripts/06_save_map.sh maps/saved/my_map
```

생성되는 파일:

```text
maps/saved/my_map.yaml
maps/saved/my_map.pgm
```

| 파일 | 역할 |
|---|---|
| `.yaml` | 맵 이미지 경로, 해상도, origin, threshold 등의 메타데이터 |
| `.pgm` | 실제 2D occupancy grid 맵 이미지 |

확인:

```bash
ls -lh maps/saved/
cat maps/saved/my_map.yaml
```

---

## 10. 자주 생기는 문제

### `/scan`이 안 나온다

```bash
ros2 topic list
ros2 topic echo /scan
ls /dev/ttyUSB*
ls /dev/ttyACM*
```

확인할 것:

- LiDAR 전원
- LiDAR USB 연결
- bringup 실행 여부
- LiDAR 포트 설정
- serial 권한

### `/odom`이 안 나온다

```bash
ros2 topic echo /odom
ls /dev/ttyUSB*
ls /dev/ttyACM*
```

확인할 것:

- VESC 연결
- VESC 포트 설정
- bringup 실행 여부

### RViz2에서 맵이 안 보인다

```bash
ros2 topic echo /map
ros2 topic list | grep map
```

RViz2에서 Fixed Frame을 `map`으로 설정하고 Map display topic을 `/map`으로 설정한다.

### 맵이 삐뚤어진다

가능한 원인:

- 차량을 너무 빠르게 움직임
- 급회전
- odom 품질 불량
- LiDAR 데이터 끊김
- TF 불안정
- 바퀴 미끄러짐

해결:

- 속도를 낮춘다.
- 회전을 천천히 한다.
- 같은 구역을 여러 번 지나간다.
- odom과 TF를 확인한다.

---

## 11. SLAM 완료 후 다음 단계

맵 저장까지 완료했다면 다음 단계는 위치추정이다.

다음 문서:

```text
docs/04_위치추정_particle_filter.md
```
