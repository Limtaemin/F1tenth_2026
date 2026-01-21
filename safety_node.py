#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, QoSReliabilityPolicy, QoSHistoryPolicy
import numpy as np
import math

# ROS 2 Message Imports
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
from ackermann_msgs.msg import AckermannDriveStamped
from visualization_msgs.msg import Marker

class SafetyNode(Node):
    def __init__(self):
        super().__init__('safety_node')

        # 1. Declare Parameters
        # TTC Thresholds
        self.declare_parameter('ttc_full_brake', 0.6)   # Critical Stop
        self.declare_parameter('ttc_warning_start', 2.0) # Start slowing down here
        self.declare_parameter('min_dist_threshold', 0.30) 
        
        # Tuning: How aggressively to brake? 
        # Higher = Faster allowed speeds. Lower = More conservative.
        self.declare_parameter('braking_gain', 4.0) 

        # Get parameter values
        self.t_fb = self.get_parameter('ttc_full_brake').value
        self.t_warn = self.get_parameter('ttc_warning_start').value
        self.dist_threshold = self.get_parameter('min_dist_threshold').value
        self.gain = self.get_parameter('braking_gain').value

        # 2. State Variables
        self.current_speed = 0.0

        # 3. Subscribers
        self.lidar_sub = self.create_subscription(LaserScan, '/scan', self.scan_callback, 10)
        
        # Robust Odom QoS
        odom_qos = QoSProfile(
            reliability=QoSReliabilityPolicy.BEST_EFFORT,
            history=QoSHistoryPolicy.KEEP_LAST,
            depth=10
        )
        self.odom_sub = self.create_subscription(Odometry, '/odom', self.odom_callback, odom_qos)

        # 4. Publishers
        self.drive_pub = self.create_publisher(AckermannDriveStamped, '/drive', 1000)
        self.vis_pub = self.create_publisher(Marker, 'safety_viz', 10)

        self.get_logger().info("Proportional Safety Node Initialized")

    def odom_callback(self, msg):
        self.current_speed = msg.twist.twist.linear.x

    def scan_callback(self, scan_msg):
        ranges = np.array(scan_msg.ranges)
        
        # --- 1. PRE-PROCESSING ---
        ranges = np.where(np.isnan(ranges), np.inf, ranges)
        ranges = np.where(np.isinf(ranges), np.inf, ranges)

        # --- 2. RAW DISTANCE CHECK ---
        angle_range_rad = np.radians(20) 
        index_window = int(angle_range_rad / scan_msg.angle_increment)
        mid_index = len(ranges) // 2
        start_idx = max(0, mid_index - index_window)
        end_idx = min(len(ranges), mid_index + index_window)
        
        front_ranges = ranges[start_idx : end_idx]
        min_dist = np.min(front_ranges) if len(front_ranges) > 0 else np.inf

        # --- 3. iTTC CALCULATION ---
        indices = np.arange(len(ranges))
        angles = scan_msg.angle_min + (indices * scan_msg.angle_increment)
        closing_speeds = self.current_speed * np.cos(angles)
        closing_speeds = np.maximum(0, closing_speeds)

        with np.errstate(divide='ignore', invalid='ignore'):
            ittc = ranges / closing_speeds
        
        ittc = np.where(np.isinf(ittc), np.inf, ittc)
        ittc = np.where(np.isnan(ittc), np.inf, ittc)
        
        min_ittc = np.min(ittc) if len(ittc) > 0 else np.inf

        # --- 4. DYNAMIC BRAKING LOGIC ---
        marker_color = (1.0, 1.0, 1.0) # White (Safe)

        # CRITICAL: Full Stop
        if min_ittc <= self.t_fb or min_dist <= self.dist_threshold:
            self.publish_drive_command(0.0)
            
            reason = f"DIST {min_dist:.2f}m" if min_dist <= self.dist_threshold else f"iTTC {min_ittc:.2f}s"
            self.get_logger().error(f"FATAL: {reason} | Sending: 0.0 | Actual: {self.current_speed:.2f}")
            marker_color = (1.0, 0.0, 0.0) # Red

        # DYNAMIC: Proportional Braking
        elif min_ittc <= self.t_warn:
            # FLEXIBLE FORMULA: Speed = iTTC * Gain
            # Example: If TTC=1.5 and Gain=4.0 -> Max Speed allowed is 6.0 m/s
            # Example: If TTC=0.8 and Gain=4.0 -> Max Speed allowed is 3.2 m/s
            dynamic_target = min_ittc * self.gain
            
            # Ensure we don't accidentally speed up if user wants to go slow
            # We only cap the speed if the dynamic target is lower than current speed
            if dynamic_target < self.current_speed:
                self.publish_drive_command(dynamic_target)
                self.get_logger().warn(f"BRAKING: TTC {min_ittc:.2f}s | Limit: {dynamic_target:.2f} m/s | Actual: {self.current_speed:.2f}")
                marker_color = (1.0, 0.5, 0.0) # Orange
            else:
                # We are safe enough for current speed, just warn
                self.get_logger().info(f"MONITOR: TTC {min_ittc:.2f}s | Safe for current speed {self.current_speed:.2f} m/s")
                marker_color = (1.0, 1.0, 0.0) # Yellow

        else:
            # Safe State
            pass

        self.publish_marker(scan_msg.header.frame_id, *marker_color)

    def publish_drive_command(self, speed):
        msg = AckermannDriveStamped()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.drive.speed = float(speed)
        self.drive_pub.publish(msg)

    def publish_marker(self, frame_id, r, g, b):
        marker = Marker()
        marker.header.frame_id = frame_id
        marker.header.stamp = self.get_clock().now().to_msg()
        marker.id = 0
        marker.type = Marker.SPHERE
        marker.action = Marker.ADD
        marker.pose.position.x = 0.0; marker.pose.position.y = 0.0; marker.pose.position.z = 0.0
        marker.scale.x = 0.5; marker.scale.y = 0.5; marker.scale.z = 0.5
        marker.color.a = 1.0
        marker.color.r = r; marker.color.g = g; marker.color.b = b
        self.vis_pub.publish(marker)

def main(args=None):
    rclpy.init(args=args)
    safety_node = SafetyNode()
    try:
        rclpy.spin(safety_node)
    except KeyboardInterrupt:
        pass
    finally:
        safety_node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
