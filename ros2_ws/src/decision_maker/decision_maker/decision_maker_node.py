#!/usr/bin/env python3
"""Decision Maker Node for ROS2"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import Twist
import json
import time

class DecisionMaker(Node):
    """ROS2 Node that makes decisions based on RAG responses and robot state"""
    
    def __init__(self):
        super().__init__('decision_maker')
        
        self.get_logger().info("\n" + "="*70)
        self.get_logger().info("Decision Maker Node Starting")
        self.get_logger().info("="*70)
        
        # Subscribers
        self.rag_response_sub = self.create_subscription(
            String,
            'rag_response',
            self.handle_rag_response,
            10
        )
        
        self.robot_status_sub = self.create_subscription(
            String,
            'robot_status',
            self.handle_robot_status,
            10
        )
        
        # Publishers
        self.decision_pub = self.create_publisher(String, 'decision_output', 10)
        self.safety_alert_pub = self.create_publisher(String, 'safety_alert', 10)
        
        # State tracking
        self.robot_state = {}
        self.last_rag_response = None
        self.decisions_made = 0
        self.safety_violations = 0
        
        # Safety constraints
        self.max_speed = 0.5  # m/s
        self.min_safe_distance = 0.5  # meters (simulated)
        self.max_angular_velocity = 1.0  # rad/s
        
        self.get_logger().info("✓ Subscribers initialized")
        self.get_logger().info("✓ Publishers initialized")
        self.get_logger().info("✓ Safety constraints loaded")
        self.get_logger().info("="*70)
        self.get_logger().info("Decision Maker Ready!\n")
    
    def handle_robot_status(self, msg: String):
        """Handle robot status updates"""
        try:
            self.robot_state = json.loads(msg.data) if msg.data.startswith('{') else {'raw': msg.data}
        except:
            self.robot_state = {'raw': msg.data}
    
    def handle_rag_response(self, msg: String):
        """Handle RAG response and make decision"""
        response = msg.data
        self.last_rag_response = response
        
        self.get_logger().info(f"\n[Decision Maker] Processing RAG response ({len(response)} chars)")
        
        # Extract command from response
        command = self.parse_response(response)
        
        if not command:
            self.get_logger().info("No command to process")
            return
        
        # Validate command against safety constraints
        is_safe, reason = self.validate_safety(command)
        
        if not is_safe:
            self.decisions_made += 1
            self.safety_violations += 1
            alert = f"Safety violation #{self.safety_violations}: {reason}"
            self.get_logger().warn(alert)
            
            # Publish safety alert
            alert_msg = String()
            alert_msg.data = alert
            self.safety_alert_pub.publish(alert_msg)
            
            # Override with safe command
            command = self.get_safe_override(command)
        
        # Make final decision
        decision = self.make_decision(command)
        
        # Log and publish decision
        self.decisions_made += 1
        self.log_decision(decision)
        self.publish_decision(decision)
    
    def parse_response(self, response: str) -> dict:
        """Extract command from RAG response"""
        response_lower = response.lower()
        command = {}
        
        # Speed parsing
        if 'stop' in response_lower or 'halt' in response_lower:
            command['action'] = 'stop'
            command['speed'] = 0.0
        elif '0.5' in response_lower or 'safe' in response_lower or 'maximum' in response_lower:
            command['action'] = 'move'
            command['speed'] = 0.5
        elif '0.2' in response_lower or 'slow' in response_lower or 'caution' in response_lower:
            command['action'] = 'move'
            command['speed'] = 0.2
        elif 'fast' in response_lower or '1.0' in response_lower:
            command['action'] = 'move'
            command['speed'] = 1.0
        else:
            command['action'] = 'idle'
            command['speed'] = 0.0
        
        # Direction parsing
        if 'turn left' in response_lower:
            command['direction'] = 'left'
            command['angular'] = 0.5
        elif 'turn right' in response_lower:
            command['direction'] = 'right'
            command['angular'] = -0.5
        else:
            command['direction'] = 'straight'
            command['angular'] = 0.0
        
        return command
    
    def validate_safety(self, command: dict) -> tuple:
        """Validate command against safety constraints"""
        speed = command.get('speed', 0.0)
        angular = abs(command.get('angular', 0.0))
        
        # Check speed limit
        if speed > self.max_speed:
            return False, f"Speed {speed} exceeds max {self.max_speed}"
        
        # Check angular velocity limit
        if angular > self.max_angular_velocity:
            return False, f"Angular velocity {angular} exceeds max {self.max_angular_velocity}"
        
        # Check for conflicting commands
        if command.get('action') == 'stop' and command.get('speed', 0) > 0:
            return False, "Conflicting command: stop with non-zero speed"
        
        # Simulate obstacle detection
        if command.get('action') == 'move' and command.get('speed', 0) > 0.4:
            # In a real system, this would query a sensor
            obstacle_detected = False  # Simulated sensor
            if obstacle_detected:
                return False, "Obstacle detected ahead"
        
        return True, "Safe"
    
    def get_safe_override(self, command: dict) -> dict:
        """Get safe version of unsafe command"""
        safe_command = command.copy()
        
        # Limit speed
        if safe_command.get('speed', 0) > self.max_speed:
            self.get_logger().info(f"Limiting speed from {safe_command['speed']} to {self.max_speed}")
            safe_command['speed'] = self.max_speed
        
        # Limit angular velocity
        if abs(safe_command.get('angular', 0)) > self.max_angular_velocity:
            angular = safe_command['angular']
            safe_command['angular'] = min(abs(angular), self.max_angular_velocity) * (1 if angular > 0 else -1)
        
        return safe_command
    
    def make_decision(self, command: dict) -> dict:
        """Make final decision based on command and robot state"""
        decision = {
            'timestamp': time.time(),
            'command': command,
            'confidence': 0.9,  # Simulated confidence score
            'rationale': 'Command passed safety validation'
        }
        
        # Add state-based decision logic
        if command.get('action') == 'stop':
            decision['priority'] = 'high'
            decision['execution_time'] = 'immediate'
        elif command.get('action') == 'move':
            decision['priority'] = 'normal'
            decision['execution_time'] = 'immediate'
        else:
            decision['priority'] = 'low'
            decision['execution_time'] = 'deferred'
        
        return decision
    
    def log_decision(self, decision: dict):
        """Log decision details"""
        self.get_logger().info(f"\n[Decision #{self.decisions_made}] Made at {decision['timestamp']:.2f}")
        self.get_logger().info(f"  Action: {decision['command'].get('action')}")
        self.get_logger().info(f"  Speed: {decision['command'].get('speed')} m/s")
        self.get_logger().info(f"  Priority: {decision['priority']}")
        self.get_logger().info(f"  Confidence: {decision['confidence']:.0%}")
        self.get_logger().info(f"  Rationale: {decision['rationale']}")
    
    def publish_decision(self, decision: dict):
        """Publish decision output"""
        decision_msg = String()
        decision_msg.data = json.dumps({
            'decision_id': self.decisions_made,
            'action': decision['command'].get('action'),
            'speed': decision['command'].get('speed'),
            'angular': decision['command'].get('angular'),
            'priority': decision['priority'],
            'confidence': decision['confidence']
        })
        self.decision_pub.publish(decision_msg)
        self.get_logger().info("✓ Decision published to /decision_output")


def main(args=None):
    rclpy.init(args=args)
    node = DecisionMaker()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        rclpy.shutdown()


if __name__ == '__main__':
    main()
