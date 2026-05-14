#!/usr/bin/env python3

import os
import signal
import subprocess
import threading
from datetime import datetime

from flask import Flask, jsonify, request, render_template_string

import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_system_default

from ackermann_msgs.msg import AckermannDriveStamped


app = Flask(__name__)

# ===============================
# ---  PROCESS ORCHESTRATION  ---
# ===============================

bringup_proc = None
map_proc = None


def start_launch(cmd):
    return subprocess.Popen(
        cmd,
        preexec_fn=os.setsid,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def stop_launch(proc):
    if proc and proc.poll() is None:
        os.killpg(os.getpgid(proc.pid), signal.SIGINT)


def status_of(proc):
    if proc is None:
        return "stopped"

    rc = proc.poll()

    if rc is None:
        return "running"

    if rc == 0:
        return "stopped"

    return "failed"


def shutdown_handler(signum, frame):
    print("\n종료 요청을 받았습니다. 실행 중인 하위 프로세스에 SIGINT를 보냅니다.")

    stop_launch(bringup_proc)
    stop_launch(map_proc)

    # 프로세스가 정상 종료될 시간을 조금 준 뒤 강제 종료
    threading.Timer(2.0, lambda: os._exit(0)).start()


signal.signal(signal.SIGINT, shutdown_handler)
signal.signal(signal.SIGTERM, shutdown_handler)


# mission_control/dashboard.py 기준으로 레포 루트 계산
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

MAP_PARAM_FILE = os.path.join(
    REPO_ROOT,
    "src",
    "f1tenth_system",
    "f1tenth_stack",
    "config",
    "f1tenth_online_async.yaml",
)

MAP_SAVE_DIR = os.path.join(REPO_ROOT, "maps", "saved")


# ===============================
# ---   TELEOP SHARED STATE   ---
# ===============================

lock = threading.Lock()

speed = 0.0
steer = 0.0

MAX_SPEED = 1.0
STEER_MAG = 0.25

HZ = 20.0

# 기본값: 수동 모드
autonomous_mode = False


# ===============================
# -----------  HTML  ------------
# ===============================

HTML = """
<!doctype html>
<html lang="ko">
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>F1TENTH 실험 대시보드</title>

<style>
body {
  font-family: sans-serif;
  text-align: center;
  margin: 0;
  padding: 16px;
}

h2 {
  margin-bottom: 4px;
}

.notice {
  max-width: 720px;
  margin: 8px auto 14px auto;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background: #fafafa;
  font-size: 14px;
  line-height: 1.5;
}

.toolbar-block {
  max-width: 720px;
  margin: 0 auto;
  font-size: 14px;
  padding: 8px 0 10px 0;
  border-top: 2px solid #aaa;
  border-bottom: 2px solid #aaa;
}

.rowline {
  margin-top: 8px;
}

.small-btn {
  padding: 6px 10px;
  font-size: 13px;
  margin: 2px;
}

.status-dot {
  display:inline-block;
  width:12px;
  height:12px;
  border-radius:50%;
  margin-left: 4px;
  margin-right: 4px;
}

.running { background:#2ecc71; }
.stopped { background:#e74c3c; }
.failed { background:orange; }

input[type=number]{
  width:90px;
  text-align:center;
  font-size:16px;
}

.dpad-btn{
  border-radius:50%;
  width:85px;
  height:85px;
  font-size:18px;
  margin:6px;
}

.center-btn{
  background:#ff5555;
  color:white;
  font-weight: bold;
}

.mode-manual {
  color: blue;
  font-weight: bold;
}

.mode-auto {
  color: red;
  font-weight: bold;
}
</style>
</head>

<body>

<h2>F1TENTH 실험 대시보드</h2>

<div class="notice">
  실차 테스트 전에는 반드시 차량 바퀴를 바닥에서 띄우고,
  주변 안전을 확인하세요. 이 화면의 수동 조작 명령은
  <b>/webop</b> 토픽으로 발행됩니다.
</div>

<!-- ====== MODE TOGGLE ====== -->
<h3>
  주행 모드:
  <span id="modeLabel" class="mode-manual">수동 조작</span>
</h3>

<button class="small-btn" onclick="set_manual()">수동 모드</button>
<button class="small-btn" onclick="set_auto()">자율주행 모드</button>

<br><br>

<!-- ========= COMPACT ORCHESTRATOR ========= -->

<div class="toolbar-block">

  <!-- Bringup line -->
  <div class="rowline">
    <b>차량 Bringup:</b>
    <span id="bringupDot" class="status-dot stopped"></span>
    <span id="bringupText">정지됨</span>
    <button class="small-btn" onclick="bringup_start()">시작</button>
    <button class="small-btn" onclick="bringup_stop()">정지</button>
  </div>

  <!-- Map line -->
  <div class="rowline">
    <b>SLAM / 맵:</b>
    <span id="mapDot" class="status-dot stopped"></span>
    <span id="mapText">정지됨</span>
    <button class="small-btn" onclick="map_start()">SLAM 시작</button>
    <button class="small-btn" onclick="map_stop()">SLAM 정지</button>

    &nbsp; | &nbsp;
    <button class="small-btn" onclick="save_map()">맵 저장</button>
  </div>

</div>

<!-- ================= TELEOP SECTION ================= -->

<h3>수동 조작 패드</h3>

<div>
  최대 속도:
  <input id="maxSpeed" type="number" step="0.1" value="1.0">

  최대 조향:
  <input id="maxSteer" type="number" step="0.01" value="0.20">

  <button onclick="apply_limits()">적용</button>
</div>

<p id="limitView" style="font-weight:bold;"></p>

<p id="cmdView" style="font-size:18px;">속도=0.00 | 조향=0.00</p>

<div>
  <button class="dpad-btn" onclick="send('up')">전진</button>
</div>
<div>
  <button class="dpad-btn" onclick="send('left')">좌회전</button>
  <button class="dpad-btn center-btn" onclick="send('stop')">정지</button>
  <button class="dpad-btn" onclick="send('right')">우회전</button>
</div>
<div>
  <button class="dpad-btn" onclick="send('down')">후진</button>
</div>

<p style="font-size:13px;color:#666;">
  수동 모드에서만 웹 조작 명령이 발행됩니다.
  자율주행 모드에서는 웹 조작 명령을 발행하지 않습니다.
</p>

<script>
// --- 상태 문자열 한국어 변환 ---
function statusKo(status){
  if(status === "running") return "실행 중";
  if(status === "stopped") return "정지됨";
  if(status === "failed") return "오류";
  return status;
}

// --- orchestrator ---
function bringup_start(){ fetch("/bringup/start").then(update_state); }
function bringup_stop(){ fetch("/bringup/stop").then(update_state); }
function map_start(){ fetch("/map/start").then(update_state); }
function map_stop(){ fetch("/map/stop").then(update_state); }

function save_map(){
  fetch("/map/save")
    .then(r => r.json())
    .then(data => {
      if(data.msg){
        alert(data.msg);
      } else if(data.error){
        alert("맵 저장 오류: " + data.error);
      }
      update_state();
    });
}

// --- teleop ---
function send(cmd){
  fetch("/cmd", {
    method:"POST",
    headers:{'Content-Type':'application/json'},
    body:JSON.stringify({cmd:cmd})
  }).then(update_state);
}

function apply_limits(){
  fetch("/set_limits", {
    method:"POST",
    headers:{'Content-Type':'application/json'},
    body:JSON.stringify({
      max_speed:document.getElementById('maxSpeed').value,
      steer_mag:document.getElementById('maxSteer').value
    })
  }).then(update_state);
}

// --- mode switching ---
function set_manual(){ fetch("/mode/manual").then(update_state); }
function set_auto(){ fetch("/mode/auto").then(update_state); }

function update_state(){
 fetch("/state").then(r=>r.json()).then(s=>{

   // limits + command
   document.getElementById('limitView').innerText =
     `제한값: 최대 속도 ${s.max_speed.toFixed(2)}, 최대 조향 ${s.steer_mag.toFixed(2)}`;

   document.getElementById('cmdView').innerText =
     `속도 ${s.speed.toFixed(2)} , 조향 ${s.steer.toFixed(2)}`;

   // bringup state
   document.getElementById('bringupText').innerText = statusKo(s.bringup);
   document.getElementById('bringupDot').className = "status-dot " + s.bringup;

   // map state
   document.getElementById('mapText').innerText = statusKo(s.map);
   document.getElementById('mapDot').className = "status-dot " + s.map;

   // mode state
   const modeLabel = document.getElementById('modeLabel');
   modeLabel.innerText = s.autonomous ? "자율주행" : "수동 조작";
   modeLabel.className = s.autonomous ? "mode-auto" : "mode-manual";
 });
}

setInterval(update_state, 800);
update_state();
</script>

</body>
</html>
"""


@app.route("/")
def index():
    return render_template_string(HTML)


# ---------- orchestrator endpoints ----------

@app.route("/bringup/start")
def bringup_start():
    global bringup_proc

    if bringup_proc and bringup_proc.poll() is None:
        return "already running"

    bringup_proc = start_launch([
        "ros2",
        "launch",
        "f1tenth_stack",
        "bringup_launch.py",
    ])

    return "ok"


@app.route("/bringup/stop")
def bringup_stop():
    global bringup_proc

    stop_launch(bringup_proc)

    return "ok"


@app.route("/map/start")
def map_start():
    global map_proc

    if map_proc and map_proc.poll() is None:
        return "already running"

    map_proc = start_launch([
        "ros2",
        "launch",
        "slam_toolbox",
        "online_async_launch.py",
        f"params_file:={MAP_PARAM_FILE}",
    ])

    return "ok"


@app.route("/map/stop")
def map_stop():
    global map_proc

    stop_launch(map_proc)

    return "ok"


@app.route("/map/save")
def map_save():
    os.makedirs(MAP_SAVE_DIR, exist_ok=True)

    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    name = os.path.join(MAP_SAVE_DIR, f"map_{now}")

    ros_cmd = f"ros2 run nav2_map_server map_saver_cli -f {name}"

    try:
        subprocess.Popen(
            ["bash", "-i", "-c", ros_cmd],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT,
            start_new_session=True,
        )

        return jsonify(msg=f"맵 저장을 요청했습니다: {name}")

    except Exception as e:
        return jsonify(error=str(e)), 500


# ---------- shared status ----------

@app.route("/state")
def state():
    with lock:
        return jsonify(
            bringup=status_of(bringup_proc),
            map=status_of(map_proc),
            speed=speed,
            steer=steer,
            max_speed=MAX_SPEED,
            steer_mag=STEER_MAG,
            autonomous=autonomous_mode,
        )


# ---------- teleop config ----------

@app.route("/set_limits", methods=["POST"])
def set_limits():
    global MAX_SPEED, STEER_MAG

    d = request.get_json()

    with lock:
        MAX_SPEED = abs(float(d["max_speed"]))
        STEER_MAG = abs(float(d["steer_mag"]))

    return ("", 204)


@app.route("/cmd", methods=["POST"])
def cmd():
    global speed, steer

    c = request.get_json()["cmd"]

    with lock:
        if c == "up":
            speed += MAX_SPEED
        elif c == "down":
            speed -= MAX_SPEED
        elif c == "left":
            steer += STEER_MAG
        elif c == "right":
            steer -= STEER_MAG
        elif c == "stop":
            speed = 0.0
            steer = 0.0

        speed = max(-MAX_SPEED, min(MAX_SPEED, speed))
        steer = max(-STEER_MAG, min(STEER_MAG, steer))

    return ("", 204)


# ---------- mode endpoints ----------

@app.route("/mode/manual")
def mode_manual():
    global autonomous_mode

    with lock:
        autonomous_mode = False

    return ("", 204)


@app.route("/mode/auto")
def mode_auto():
    global autonomous_mode

    with lock:
        autonomous_mode = True

    return ("", 204)


# ===============================
# ROS2 TELEOP NODE
# ===============================

class DrivePublisher(Node):
    def __init__(self):
        super().__init__("web_teleop")

        self.pub = self.create_publisher(
            AckermannDriveStamped,
            "/webop",
            qos_profile_system_default,
        )

        self.create_timer(1.0 / HZ, self.on_timer)

    def on_timer(self):
        global autonomous_mode

        with lock:
            if autonomous_mode:
                return

            v = float(speed)
            s = float(steer)

        msg = AckermannDriveStamped()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.drive.speed = v
        msg.drive.steering_angle = s

        self.pub.publish(msg)


# ===============================
# MAIN
# ===============================

def main():
    rclpy.init()

    node = DrivePublisher()

    signal.signal(signal.SIGINT, shutdown_handler)
    signal.signal(signal.SIGTERM, shutdown_handler)

    web = threading.Thread(
        target=lambda: app.run(
            host="0.0.0.0",
            port=5000,
            debug=False,
            use_reloader=False,
        ),
        daemon=True,
    )

    web.start()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        print("\nKeyboardInterrupt received")

    finally:
        print("ROS 노드와 하위 프로세스를 종료합니다.")

        node.destroy_node()
        rclpy.shutdown()

        stop_launch(bringup_proc)
        stop_launch(map_proc)

        print("정상 종료 완료.")


if __name__ == "__main__":
    main()
