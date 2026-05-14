# F1TENTH 한국어 실험 문서

이 사이트는 F1TENTH 차량을 ROS2 환경에서 실험하기 위한 한국어 문서 사이트입니다.

## 시작하기

처음 보는 사람은 아래 순서로 읽으면 됩니다.

1. 전체 개요
2. 설치와 빌드
3. 수동조작과 웹조작
4. SLAM 맵 생성
5. 위치추정
6. Pure Pursuit 경로추종
7. Stanley 장애물 회피
8. config 설명
9. 문제해결
10. 실행 묶음과 주행 모드

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
SLAM 맵 생성
bash scripts/02_bringup.sh
bash scripts/04_rviz.sh
bash scripts/05_slam_start.sh
bash scripts/03_web_dashboard.sh
Pure Pursuit 주행
bash scripts/02_bringup.sh
bash scripts/04_rviz.sh
bash scripts/07_localization.sh
bash scripts/08_pure_pursuit.sh
Stanley Avoidance 주행
bash scripts/02_bringup.sh
bash scripts/04_rviz.sh
bash scripts/07_localization.sh
bash scripts/09_stanley_avoidance.sh

