#!/usr/bin/env python3
"""Gazebo Robot Bridge - Controls Gazebo robot via ROS2"""

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import Float64
import subprocess
import time

class GazeboBridge(Node):
    """Bridge between ROS2 /cmd_vel and Gazebo robot control"""
    
    def __init__(self):
        super().__init__('gazebo_bridge')
        
        self.get_logger().info("\n" + "="*70)
        self.get_logger().info("Gazebo Robot Bridge Starting")
        self.get_logger().info("="*70)
        
        # Subscribe to cmd_vel from robot controller
        self.cmd_vel_sub = self.create_subscription(
            Twist,
            'cmd_vel',
            self.handle_cmd_vel,
            10
        )
        
        # Publishers for Gazebo joint commands
        self.left_wheel_pub = self.create_publisher(Float64, '/left_wheel_velocity_controller/commands', 10)
        self.right_wheel_pub = self.create_publisher(Float64, '/right_wheel_velocity_controller/commands', 10)
        
        # Status tracking
        self.last_cmd = None
        self.commands_sent = 0
        
        self.get_logger().info("✓ Subscribers initialized")
        self.get_logger().info("✓ Publishers initialized")
        self.get_logger().info("="*70)
        self.get_logger().info("Gazebo Bridge Ready!\n")
    
    def handle_cmd_vel(self, msg: Twist):
        """Convert Twist to wheel velocities and send to Gazebo"""
        linear_vel = msg.linear.x
        angular_vel = msg.angular.z
        
        # Differential drive kinematics
        wheel_radius = 0.1  # meters
        robot_width = 0.4   # meters between wheels
        
        # Calculate wheel velocities
        left_wheel_vel = (linear_vel - (angular_vel * robot_width / 2)) / wheel_radius
        right_wheel_vel = (linear_vel + (angular_vel * robot_width / 2)) / wheel_radius
        
        self.commands_sent += 1
        self.last_cmd = {
            'linear': linear_vel,
            'angular': angular_vel,
            'left_wheel': left_wheel_vel,
            'right_wheel': right_wheel_vel
        }
        
        self.get_logger().info(f"\n[Command #{self.commands_sent}] Received Twist")
        self.get_logger().info(f"  Linear velocity: {linear_vel:.2f} m/s")
        self.get_logger().info(f"  Angular velocity: {angular_vel:.2f} rad/s")
        self.get_logger().info(f"  Left wheel vel: {left_wheel_vel:.2f} rad/s")
        self.get_logger().info(f"  Right wheel vel: {right_wheel_vel:.2f} rad/s")
        
        # Publish wheel velocities to Gazebo
        left_msg = Float64()
        left_msg.data = left_wheel_vel
        self.left_wheel_pub.publish(left_msg)
        
        right_msg = Float64()
        right_msg.data = right_wheel_vel
        self.right_wheel_pub.publish(right_msg)
        
        self.get_logger().info("✓ Wheel commands published to Gazebo")


def main(args=None):
    rclpy.init(args=args)
    node = GazeboBridge()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        rclpy.shutdown()


if __name__ == '__main__':
    main()
