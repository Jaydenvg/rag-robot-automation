from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    """Launch complete RAG + Robot Control system"""
    
    rag_server_node = Node(
        package='rag_server',
        executable='rag_server',
        name='rag_server',
        output='screen',
        emulate_tty=True,
    )
    
    robot_controller_node = Node(
        package='robot_controller',
        executable='robot_controller',
        name='robot_controller',
        output='screen',
        emulate_tty=True,
    )
    
    decision_maker_node = Node(
        package='decision_maker',
        executable='decision_maker',
        name='decision_maker',
        output='screen',
        emulate_tty=True,
    )
    
    return LaunchDescription([
        rag_server_node,
        robot_controller_node,
        decision_maker_node,
    ])
