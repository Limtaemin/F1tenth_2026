# 07. config 파일 설명

이 문서는 F1TENTH 레포에서 사용하는 YAML 설정 파일의 역할을 설명한다.

config 파일은 차량 하드웨어, 센서, 조작 입력, SLAM, 위치추정, 제어기의 동작 방식을 결정한다.  
따라서 topic 이름, frame 이름, 포트 이름, 맵 경로를 수정할 때는 주의해야 한다.

---

## 1. config 폴더 위치

주요 config 파일은 보통 아래 폴더에 있다.

```bash
src/f1tenth_system/f1tenth_stack/config/
```

현재 레포에서 YAML 파일을 찾으려면 아래 명령을 사용한다.

```bash
cd ~/race_stack/f1tenth
find src -name "*.yaml" -o -name "*.yml" | sort
```

---

## 2. 주요 config 파일

`src/f1tenth_system/f1tenth_stack/config/` 안에는 보통 다음과 같은 파일들이 있다.

| 파일 | 역할 |
|---|---|
| `f1tenth_online_async.yaml` | SLAM Toolbox 맵 생성 설정 |
| `joy_teleop.yaml` | 조이스틱 입력을 주행 명령으로 변환하는 설정 |
| `mux.yaml` | 여러 주행 명령 중 어떤 입력을 우선 사용할지 결정 |
| `sensors.yaml` | 센서 관련 설정 |
| `vesc.yaml` | VESC 모터/서보 기본 설정 |
| `vesc_fiesta.yaml` | 특정 차량용 VESC 설정 |
| `vesc_noekf.yaml` | EKF 없이 사용하는 VESC 설정 |
| `vesc_slash.yaml` | Slash 차량용 VESC 설정 |

실제 파일 목록은 레포 상태에 따라 다를 수 있으므로 항상 `find` 명령으로 확인한다.

---

## 3. config 파일이 결정하는 것

config 파일은 다음 항목들을 결정한다.

| 항목 | 설명 |
|---|---|
| LiDAR 설정 | LiDAR 포트, frame, scan topic |
| VESC 설정 | 모터, 서보, odom, 포트, 속도 변환 |
| 조이스틱 설정 | 버튼/축 입력을 주행 명령으로 변환 |
| mux 설정 | `/webop`, `/teleop`, 자율주행 명령의 우선순위 |
| SLAM 설정 | map frame, odom frame, scan topic, 맵 생성 파라미터 |
| localization 설정 | 저장된 맵, particle 개수, 초기 위치 |
| controller 설정 | 속도, 조향, waypoint, gain |

---

## 4. 함부로 바꾸면 안 되는 이름

아래 topic 이름은 여러 노드가 공유할 수 있으므로 함부로 바꾸지 않는다.

| 이름 | 의미 |
|---|---|
| `/drive` | 최종 차량 구동 명령 |
| `/webop` | 웹 대시보드 수동 조작 명령 |
| `/teleop` | 조이스틱/키보드 수동 조작 명령 |
| `/scan` | LiDAR 스캔 데이터 |
| `/odom` | 차량 odometry |
| `/map` | 맵 |
| `/tf` | 좌표계 변환 |
| `/tf_static` | 고정 좌표계 변환 |

아래 frame 이름도 그대로 유지하는 것이 좋다.

| frame | 의미 |
|---|---|
| `map` | 전역 맵 좌표계 |
| `odom` | odometry 좌표계 |
| `base_link` | 차량 기준 좌표계 |
| `laser` | LiDAR 기준 좌표계 |

이름을 바꾸면 RViz2, SLAM, localization, controller가 동시에 깨질 수 있다.

---

## 5. `f1tenth_online_async.yaml`

이 파일은 SLAM Toolbox로 맵을 만들 때 사용하는 설정이다.

주로 다음 항목을 포함한다.

| 항목 | 설명 |
|---|---|
| map frame | 보통 `map` |
| odom frame | 보통 `odom` |
| base frame | 보통 `base_link` |
| scan topic | 보통 `/scan` |
| map update interval | 맵 업데이트 주기 |
| resolution | 맵 해상도 |
| solver 설정 | SLAM 최적화 관련 설정 |

관련 실행 흐름:

```bash
bash scripts/02_bringup.sh
bash scripts/04_rviz.sh
bash scripts/05_slam_start.sh
```

확인 명령:

```bash
grep -n "map_frame\|odom_frame\|base_frame\|scan" src/f1tenth_system/f1tenth_stack/config/f1tenth_online_async.yaml
```

---

## 6. `joy_teleop.yaml`

이 파일은 조이스틱 입력을 차량 조작 명령으로 바꾸는 설정이다.

주로 다음 항목을 포함한다.

| 항목 | 설명 |
|---|---|
| 버튼 매핑 | 어떤 버튼이 어떤 명령인지 결정 |
| 축 매핑 | 조향, 속도 축 결정 |
| scale | 입력값을 얼마나 크게 사용할지 결정 |
| output topic | 변환된 조작 명령을 보낼 topic |

주의할 점:

- 버튼 번호는 조이스틱 모델마다 다를 수 있다.
- 속도 scale을 너무 크게 하면 차량이 급가속할 수 있다.
- 처음 테스트할 때는 바퀴를 띄운 상태에서 확인한다.

확인 명령:

```bash
grep -n "button\|axis\|scale\|topic" src/f1tenth_system/f1tenth_stack/config/joy_teleop.yaml
```

---

## 7. `mux.yaml`

이 파일은 여러 조작 입력 중 어떤 입력을 최종 주행 명령으로 사용할지 결정한다.

예를 들어 다음 입력들이 동시에 있을 수 있다.

| 입력 | 설명 |
|---|---|
| `/webop` | 웹 대시보드 수동 조작 |
| `/teleop` | 조이스틱/키보드 수동 조작 |
| 자율주행 controller | Pure Pursuit, Stanley 등 |
| safety node | 긴급 정지 또는 충돌 방지 |

mux는 이런 입력 중 우선순위가 높은 명령을 `/drive`로 보낸다.

확인할 항목:

| 항목 | 설명 |
|---|---|
| input topic | 입력으로 받을 topic |
| output topic | 최종 출력 topic |
| priority | 입력 우선순위 |
| timeout | 입력이 끊겼을 때 처리 시간 |

확인 명령:

```bash
grep -n "/drive\|/webop\|/teleop\|priority\|timeout" src/f1tenth_system/f1tenth_stack/config/mux.yaml
```

---

## 8. `sensors.yaml`

이 파일은 센서 관련 설정을 포함한다.

주로 다음 항목을 확인한다.

| 항목 | 설명 |
|---|---|
| LiDAR topic | 보통 `/scan` |
| LiDAR frame | 보통 `laser` |
| 센서 포트 | `/dev/ttyUSB*`, `/dev/ttyACM*` 등 |
| 센서 주기 | scan publish 주기 |

LiDAR가 안 나올 때 확인할 명령:

```bash
ros2 topic list | grep scan
ros2 topic echo /scan
```

장치 확인:

```bash
ls /dev/ttyUSB*
ls /dev/ttyACM*
```

---

## 9. `vesc.yaml`

이 파일은 VESC 기반 모터/서보 제어 설정을 포함한다.

주로 다음 항목을 확인한다.

| 항목 | 설명 |
|---|---|
| VESC 포트 | VESC가 연결된 serial 장치 |
| speed gain | 속도 명령 변환 계수 |
| steering gain | 조향 명령 변환 계수 |
| odom topic | 보통 `/odom` |
| drive topic | 보통 `/drive` |
| frame | `odom`, `base_link` 등 |

VESC 장치 확인:

```bash
ls /dev/ttyUSB*
ls /dev/ttyACM*
```

VESC 관련 설정 확인:

```bash
grep -n "vesc\|port\|speed\|steer\|odom\|drive" src/f1tenth_system/f1tenth_stack/config/vesc.yaml
```

주의:

- VESC 포트가 틀리면 차량이 움직이지 않을 수 있다.
- speed gain이나 steering gain을 잘못 바꾸면 차량이 예상과 다르게 움직일 수 있다.
- 실차에서 수정 전에는 반드시 바퀴를 띄운 상태로 테스트한다.

---

## 10. controller 관련 config

Pure Pursuit나 Stanley avoidance 패키지에도 별도 config가 있을 수 있다.

확인 명령:

```bash
find src/pure_pursuit -name "*.yaml" -o -name "*.yml" | sort
find src/stanley_avoidance -name "*.yaml" -o -name "*.yml" | sort
```

자주 확인하는 항목:

| 항목 | 설명 |
|---|---|
| waypoint path | 주행할 CSV 경로 파일 |
| target speed | 목표 속도 |
| lookahead distance | Pure Pursuit 목표점 거리 |
| stanley gain | Stanley 제어 gain |
| obstacle distance | 장애물 감지 거리 |
| drive topic | 보통 `/drive` |
| scan topic | 보통 `/scan` |

속도나 gain은 한 번에 크게 바꾸지 않는다.  
처음에는 기본값 또는 낮은 속도로 테스트한다.

---

## 11. config 수정 전 체크리스트

config를 수정하기 전에는 아래 순서를 권장한다.

1. 현재 git 상태 확인
2. 수정할 파일 백업
3. 한 번에 하나의 값만 수정
4. 변경 내용 확인
5. 빌드 또는 실행 테스트
6. 문제가 있으면 되돌리기

명령어:

```bash
cd ~/race_stack/f1tenth

git status
cp path/to/config.yaml path/to/config.yaml.bak
git diff
```

수정 후 확인:

```bash
colcon build --symlink-install
source install/setup.bash
```

변경을 되돌리려면:

```bash
git checkout -- path/to/config.yaml
```

백업 파일을 만들었다면 테스트 후 필요 없을 때 삭제한다.

```bash
rm path/to/config.yaml.bak
```

---

## 12. config 수정 후 확인할 것

수정 후에는 아래 항목을 확인한다.

| 확인 항목 | 명령 |
|---|---|
| 토픽 목록 | `ros2 topic list` |
| LiDAR | `ros2 topic echo /scan` |
| odom | `ros2 topic echo /odom` |
| drive | `ros2 topic echo /drive` |
| TF | `ros2 run tf2_tools view_frames` |
| 노드 | `ros2 node list` |

TF 확인 시 `frames.gv`, `frames.pdf`가 생성될 수 있다.  
이 파일들은 실행 결과물이므로 Git에 올리지 않는다.

---

## 13. 바꿔도 되는 값과 조심해야 하는 값

### 비교적 바꿔도 되는 값

아래 값들은 실험 목적에 따라 조정할 수 있다.

- 목표 속도
- lookahead distance
- Stanley gain
- 장애물 감지 거리
- particle 개수
- map 파일 경로
- waypoint 파일 경로

단, 처음에는 작은 값부터 바꾼다.

### 조심해야 하는 값

아래 값들은 여러 노드가 공유하므로 조심해야 한다.

- topic 이름
- frame 이름
- launch 파일에서 넘기는 config 경로
- VESC 포트
- LiDAR 포트
- odom frame
- map frame
- base frame

특히 아래 이름은 현재 문서화 단계에서 바꾸지 않는다.

- `/drive`
- `/webop`
- `/teleop`
- `/scan`
- `/odom`
- `/map`
- `/tf`
- `base_link`
- `laser`
- `odom`
- `map`

---

## 14. 추천 원칙

config를 수정할 때는 아래 원칙을 따른다.

1. 한 번에 하나의 값만 바꾼다.
2. 바꾸기 전 `git diff`를 확인한다.
3. 바꾼 뒤 `ros2 topic list`로 토픽을 확인한다.
4. RViz2에서 `/scan`, `/map`, `/tf`를 확인한다.
5. 실차 주행 전에는 반드시 바퀴를 띄우고 테스트한다.
6. topic 이름과 frame 이름은 충분히 이해하기 전까지 바꾸지 않는다.

현재 단계에서는 config 자체를 크게 수정하지 않고, 어떤 config가 어떤 역할을 하는지 문서로 정리하는 것을 목표로 한다.
