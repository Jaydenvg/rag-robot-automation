#!/usr/bin/env python3
"""RAG Server Node for ROS2"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import sys
from pathlib import Path
import time

RAG_PATH = Path.home() / "rag_robot_automation" / "rag_system"
sys.path.insert(0, str(RAG_PATH))

try:
    from rag_pipeline import RAGPipeline
except ImportError as e:
    print(f"ERROR: Cannot import RAG pipeline from {RAG_PATH}")
    sys.exit(1)


class RAGServer(Node):
    """ROS2 Node for RAG queries"""
    
    def __init__(self):
        super().__init__('rag_server')
        
        self.get_logger().info("\n" + "="*70)
        self.get_logger().info("RAG Server Starting")
        self.get_logger().info("="*70)
        
        self.get_logger().info("Loading RAG Pipeline...")
        try:
            self.rag = RAGPipeline(use_cached_embeddings=True, model="mistral")
            self.get_logger().info("✓ RAG Pipeline loaded")
        except Exception as e:
            self.get_logger().error(f"✗ Failed to load RAG: {e}")
            raise
        
        self.response_pub = self.create_publisher(String, 'rag_response', 10)
        self.query_sub = self.create_subscription(
            String, 'rag_query', self.query_callback, 10
        )
        
        self.query_count = 0
        
        self.get_logger().info("✓ Ready")
        self.get_logger().info("="*70 + "\n")
    
    def query_callback(self, msg: String):
        """Handle query"""
        self.query_count += 1
        query = msg.data
        
        self.get_logger().info(f"\n[Query #{self.query_count}] {query}")
        
        try:
            start = time.time()
            result = self.rag.query(query)
            elapsed = time.time() - start
            
            response = String()
            response.data = result['response']
            self.response_pub.publish(response)
            
            self.get_logger().info(f"✓ Response in {elapsed:.1f}s")
        except Exception as e:
            self.get_logger().error(f"✗ Error: {e}")
            error = String()
            error.data = f"ERROR: {str(e)}"
            self.response_pub.publish(error)


def main(args=None):
    rclpy.init(args=args)
    node = RAGServer()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        rclpy.shutdown()


if __name__ == '__main__':
    main()
