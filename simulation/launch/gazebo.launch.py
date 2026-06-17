from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from pathlib import Path
import os

def generate_launch_description():
    """Launch Gazebo simulation with RAG robot"""
    
    # Get paths
    gazebo_ros_pkg = os.path.join(os.environ['GAZEBO_MODEL_PATH'].split(':')[0], '..', '..')
    
    # Gazebo server
    gazebo_server = Node(
        package='gz_ros2_control',
        executable='gz_ros2_control_node',
        parameters=[{'sim_mode': True}],
        remappings=[('/cmd_vel', 'cmd_vel')],
        output='screen'
    )
    
    # Launch Gazebo with world
    world_file = os.path.join(
        os.path.dirname(__file__),
        '..',
        'worlds',
        'rag_robot.world'
    )
    
    gazebo = Node(
        package='gazebo_ros',
        executable='gazebo',
        arguments=['-s', 'libgazebo_ros_init.so', '-s', 'libgazebo_ros_factory.so', world_file],
        output='screen'
    )
    
    return LaunchDescription([
        gazebo,
    ])
