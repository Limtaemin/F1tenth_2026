# 07. config 파일 설명

이 문서는 `src/f1tenth_system/f1tenth_stack/config/` 안에 있는 YAML 파일들의 역할을 설명한다.

config 파일은 F1TENTH 시스템에서 매우 중요하다.

이 파일들은 다음을 결정한다.

```text
LiDAR 설정
VESC 모터/서보 설정
조이스틱 설정
주행 명령 우선순위
SLAM 설정
1. config 폴더 위치
src/f1tenth_system/f1tenth_stack/config

주요 파일:

f1tenth_online_async.yaml
joy_teleop.yaml
mux.yaml
sensors.yaml
vesc.yaml
vesc_fiesta.yaml
vesc_noekf.yaml
vesc_slash.yaml
2. 전체 요약
파일역할
f1tenth_online_async.yamlSLAM Toolbox로 맵 생성할 때 사용하는 설정
joy_teleop.yaml조이스틱 버튼/축을 Ackermann 주행 명령으로 변환
mux.yaml/drive, /teleop, /webop 중 어떤 명령을 우선 적용할지 결정
sensors.yamlLiDAR IP, frame, scan 범위 설정
vesc.yaml기본 VESC 모터/서보/odom 설정
vesc_fiesta.yamlFiesta 차체용 VESC 설정
vesc_slash.yamlSlash 차체용 VESC 설정
vesc_noekf.yamlTF 발행 방식이 다른 VESC 설정
3. f1tenth_online_async.yaml

SLAM Toolbox 설정 파일이다.

사용 목적:

LiDAR /scan을 사용해서 실시간으로 map을 생성

실행 예시:

ros2 launch slam_toolbox online_async_launch.py \
  params_file:=src/f1tenth_system/f1tenth_stack/config/f1tenth_online_async.yaml

중요한 항목:

항목의미
odom_frameodom 좌표계 이름
map_framemap 좌표계 이름
base_frame차량 또는 LiDAR 기준 frame
scan_topicLiDAR scan 토픽
modemapping 또는 localization 모드
resolutionmap 해상도
max_laser_rangeLiDAR 최대 사용 거리
do_loop_closingloop closure 사용 여부

주의:

base_frame, odom_frame, map_frame은 RViz2 /tf와 반드시 맞아야 한다.
4. joy_teleop.yaml

조이스틱 입력을 Ackermann 주행 명령으로 바꾸는 설정이다.

주요 역할:

조이스틱 버튼/스틱 입력
→ speed, steering_angle
→ /teleop 토픽 발행

중요한 항목:

항목의미
device_id사용할 조이스틱 장치 번호
deadzone작은 흔들림 무시 범위
autorepeat_rate조이스틱 명령 반복 발행 주기
deadman_buttons누르고 있어야 조작이 가능한 버튼
axis사용할 조이스틱 축 번호
scale입력값을 실제 속도/조향각으로 바꾸는 비율

예시 개념:

axis 1 → 속도
axis 3 → 조향
deadman button → 누르고 있을 때만 명령 발행
5. mux.yaml

주행 명령 우선순위를 정하는 파일이다.

F1TENTH에서는 여러 명령이 동시에 들어올 수 있다.

자율주행 알고리즘 → /drive
조이스틱 조작     → /teleop
웹 대시보드       → /webop

mux.yaml은 이 중 어떤 명령을 최종적으로 차량에 보낼지 결정한다.

주요 항목:

항목의미
topic입력으로 받을 토픽
timeout해당 토픽이 몇 초 동안 끊기면 무효로 볼지
priority우선순위

일반적인 우선순위:

/webop
> /teleop
> /drive

의미:

웹 대시보드가 가장 강한 수동 개입 권한을 가진다.

주의:

웹 대시보드가 계속 /webop을 발행하면 자율주행 /drive 명령이 무시될 수 있다.
6. sensors.yaml

LiDAR 설정 파일이다.

주요 항목:

항목의미
ip_addressLiDAR IP 주소
ip_portLiDAR 통신 포트
laser_frame_idLiDAR frame 이름
angle_min사용할 최소 각도
angle_max사용할 최대 각도
publish_intensityintensity 발행 여부
publish_multiechomulti echo 발행 여부

확인 명령어:

ros2 topic echo /scan
ros2 topic hz /scan

RViz2에서는 /scan을 LaserScan으로 추가해서 확인한다.

7. vesc.yaml

기본 VESC 설정 파일이다.

역할:

AckermannDriveStamped 명령
→ VESC 모터 ERPM 명령
→ 서보 position 명령
→ odom 계산

중요한 항목:

항목의미
speed_to_erpm_gainspeed를 ERPM으로 바꾸는 비율
speed_to_erpm_offsetERPM offset
steering_angle_to_servo_gain조향각을 서보 명령으로 바꾸는 비율
steering_angle_to_servo_offset서보 중심값
servo_min최소 서보 명령
servo_max최대 서보 명령
wheelbase차량 앞뒤 바퀴 축간거리
publish_tfodom → base_link TF 발행 여부
8. 조향 관련 핵심 값

서보가 이상하게 움직이면 주로 아래 값을 본다.

steering_angle_to_servo_gain
steering_angle_to_servo_offset
servo_min
servo_max

의미:

steering_angle_to_servo_offset
→ 조향 중앙값

steering_angle_to_servo_gain
→ 조향각이 서보 명령으로 바뀌는 비율과 방향

servo_min / servo_max
→ 조향 제한

문제 예시:

핸들이 반대로 꺾임
→ steering_angle_to_servo_gain 부호 확인

중앙이 안 맞음
→ steering_angle_to_servo_offset 조정

너무 많이 꺾임
→ servo_min / servo_max 조정
9. 속도 관련 핵심 값

속도는 주로 아래 값을 본다.

speed_to_erpm_gain
speed_to_erpm_offset

의미:

ERPM = speed_to_erpm_gain × speed + speed_to_erpm_offset

문제 예시:

속도가 너무 빠름
→ speed_to_erpm_gain 줄이기

명령을 줘도 너무 약함
→ speed_to_erpm_gain 증가

정지 명령인데 살짝 움직임
→ speed_to_erpm_offset 확인
10. vesc_fiesta.yaml, vesc_slash.yaml

차체 종류별 VESC 설정 파일이다.

차체마다 다음 값이 다를 수 있다.

wheelbase
steering_angle_to_servo_gain
steering_angle_to_servo_offset
speed_to_erpm_gain
servo_min
servo_max

따라서 내 차량이 어떤 차체인지 확인하고 맞는 설정 파일을 써야 한다.

11. vesc_noekf.yaml

TF 발행 방식이 다른 VESC 설정이다.

특히 중요한 항목:

publish_tf

개념:

publish_tf: true
→ VESC odom 노드가 odom → base_link TF를 직접 발행

publish_tf: false
→ 다른 노드, 예를 들어 EKF가 TF를 발행하도록 함

주의:

두 노드가 동시에 같은 TF를 발행하면 RViz2와 localization이 꼬일 수 있다.
12. config 수정 시 주의사항

config 파일은 launch 파일에서 직접 참조되는 경우가 많다.

따라서 파일 이름을 함부로 바꾸면 안 된다.

안전한 수정:

값 조정
주석 추가
문서 작성

위험한 수정:

파일명 변경
토픽명 변경
frame명 변경
패키지명 변경

특히 아래 이름은 여러 노드가 공유하므로 조심해야 한다.

/drive
/webop
/teleop
/scan
/odom
/map
/tf
base_link
laser
odom
map
13. config 확인용 명령어

현재 토픽 확인:

ros2 topic list

LiDAR 확인:

ros2 topic echo /scan
ros2 topic hz /scan

주행 명령 확인:

ros2 topic echo /drive
ros2 topic echo /webop
ros2 topic echo /teleop

TF 확인:

ros2 run tf2_tools view_frames

RViz2 실행:

rviz2
14. 결론

config 파일은 F1TENTH 시스템의 핵심 설정이다.

가장 자주 봐야 할 파일은 다음과 같다.

mux.yaml
→ 명령 우선순위 문제 확인

vesc.yaml
→ 모터/서보/odom 문제 확인

sensors.yaml
→ LiDAR 문제 확인

f1tenth_online_async.yaml
→ SLAM 맵 생성 문제 확인

실험 중 문제가 생기면 먼저 다음 순서로 확인한다.

1. /scan이 정상인가?
2. /odom이 정상인가?
3. /tf가 정상인가?
4. /drive 또는 /webop이 나오는가?
5. mux 우선순위가 맞는가?
6. vesc 설정이 실제 차량과 맞는가?

