#!/usr/bin/env python3
"""Robot Controller Node for ROS2"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import Twist
import json

class RobotController(Node):
    """ROS2 Node that controls robot based on RAG responses"""
    
    def __init__(self):
        super().__init__('robot_controller')
        
        self.get_logger().info("\n" + "="*70)
        self.get_logger().info("Robot Controller Node Starting")
        self.get_logger().info("="*70)
        
        # Subscribers
        self.rag_response_sub = self.create_subscription(
            String,
            'rag_response',
            self.handle_rag_response,
            10
        )
        
        # Publishers
        self.cmd_vel_pub = self.create_publisher(Twist, 'cmd_vel', 10)
        self.status_pub = self.create_publisher(String, 'robot_status', 10)
        
        # Statistics
        self.commands_executed = 0
        self.last_command = None
        
        self.get_logger().info("✓ Subscribers initialized")
        self.get_logger().info("✓ Publishers initialized")
        self.get_logger().info("="*70)
        self.get_logger().info("Robot Controller Ready!\n")
    
    def handle_rag_response(self, msg: String):
        """Handle incoming RAG response and execute robot command"""
        response = msg.data
        
        self.get_logger().info(f"\n[RAG Response] Received {len(response)} chars")
        
        # Parse response and extract commands
        command = self.parse_response(response)
        
        if command:
            self.execute_command(command)
        else:
            self.get_logger().info("No actionable command found in response")
    
    def parse_response(self, response: str) -> dict:
        """Extract robot command from RAG response"""
        response_lower = response.lower()
        
        command = {}
        
        # Speed commands - check for speed values and keywords
        if 'stop' in response_lower or 'halt' in response_lower or 'emergency' in response_lower:
            command['action'] = 'stop'
            command['speed'] = 0.0
        elif '0.5' in response_lower or 'half' in response_lower or 'safe' in response_lower or 'maximum' in response_lower:
            command['action'] = 'move'
            command['speed'] = 0.5  # Safe max speed
        elif '0.2' in response_lower or 'slow' in response_lower or 'caution' in response_lower or 'careful' in response_lower:
            command['action'] = 'move'
            command['speed'] = 0.2  # Slow speed
        elif 'fast' in response_lower or 'accelerate' in response_lower or '1.0' in response_lower or 'quickly' in response_lower:
            command['action'] = 'move'
            command['speed'] = 1.0  # Fast speed
        else:
            command['action'] = 'idle'
            command['speed'] = 0.0
        
        # Direction commands
        if 'turn left' in response_lower or 'left' in response_lower:
            command['direction'] = 'left'
            command['angular'] = 0.5
        elif 'turn right' in response_lower or 'right' in response_lower:
            command['direction'] = 'right'
            command['angular'] = -0.5
        else:
            command['direction'] = 'straight'
            command['angular'] = 0.0
        
        return command if command.get('action') != 'idle' else {}
    
    def execute_command(self, command: dict):
        """Execute robot command"""
        self.commands_executed += 1
        action = command.get('action', 'idle')
        speed = command.get('speed', 0.0)
        angular = command.get('angular', 0.0)
        
        self.get_logger().info(f"\n[Command #{self.commands_executed}] Executing {action}")
        self.get_logger().info(f"  Linear velocity: {speed} m/s")
        self.get_logger().info(f"  Angular velocity: {angular} rad/s")
        
        # Create and publish Twist message
        twist = Twist()
        twist.linear.x = float(speed)
        twist.linear.y = 0.0
        twist.linear.z = 0.0
        twist.angular.x = 0.0
        twist.angular.y = 0.0
        twist.angular.z = float(angular)
        
        self.cmd_vel_pub.publish(twist)
        self.last_command = command
        
        self.get_logger().info("✓ Command published to /cmd_vel")
        
        # Publish status
        self.publish_status()
    
    def publish_status(self):
        """Publish robot status"""
        status_msg = String()
        status_msg.data = f"Robot Status: {self.commands_executed} commands executed. Last: {self.last_command}"
        self.status_pub.publish(status_msg)


def main(args=None):
    rclpy.init(args=args)
    node = RobotController()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        rclpy.shutdown()


if __name__ == '__main__':
    main()
