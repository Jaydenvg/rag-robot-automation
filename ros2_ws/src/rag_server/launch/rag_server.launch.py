from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    """Launch RAG Server node"""
    
    rag_server_node = Node(
        package='rag_server',
        executable='rag_server',
        name='rag_server',
        output='screen',
        emulate_tty=True,
    )
    
    return LaunchDescription([
        rag_server_node,
    ])
