# F1TENTH 한국어 실험 문서

이 사이트는 F1TENTH 차량을 ROS2 환경에서 실험하기 위한 한국어 문서 사이트입니다.

## 시작하기

처음 보는 사람은 아래 순서로 읽으면 됩니다.

<div class="grid cards" markdown>

- **1. 전체 개요**  
  레포 구조와 전체 실험 흐름을 먼저 이해합니다.

- **2. 설치와 빌드**  
  ROS2 환경, 의존성, 빌드 방법을 확인합니다.

- **3. 수동조작과 웹조작**  
  웹 대시보드와 `/webop` 기반 수동 조작을 확인합니다.

- **4. SLAM 맵 생성**  
  LiDAR와 odom으로 맵을 만들고 저장합니다.

- **5. 위치추정**  
  저장된 맵 위에서 차량 위치를 추정합니다.

- **6. 주행 모드**  
  Pure Pursuit와 Stanley 실행 묶음을 구분합니다.

</div>

## 주요 실행 묶음

| 목적 | 실행 묶음 |
|---|---|
| 직접 조작 | Bringup + Web Dashboard |
| 맵 생성 | Bringup + RViz2 + SLAM + 수동조작 |
| 위치추정 | Bringup + RViz2 + Localization |
| Pure Pursuit 주행 | Bringup + RViz2 + Localization + Pure Pursuit |
| Stanley 주행 | Bringup + RViz2 + Localization + Stanley Avoidance |

## 빠른 실행 예시

### 웹 수동조작

```bash
bash scripts/02_bringup.sh
bash scripts/03_web_dashboard.sh
```

### SLAM 맵 생성

```bash
bash scripts/02_bringup.sh
bash scripts/04_rviz.sh
bash scripts/05_slam_start.sh
bash scripts/03_web_dashboard.sh
```

### Pure Pursuit 주행

```bash
bash scripts/02_bringup.sh
bash scripts/04_rviz.sh
bash scripts/07_localization.sh
bash scripts/08_pure_pursuit.sh
```

### Stanley Avoidance 주행

```bash
bash scripts/02_bringup.sh
bash scripts/04_rviz.sh
bash scripts/07_localization.sh
bash scripts/09_stanley_avoidance.sh
```

## 관련 링크

- [GitHub 저장소](https://github.com/Limtaemin/f1tenth)
