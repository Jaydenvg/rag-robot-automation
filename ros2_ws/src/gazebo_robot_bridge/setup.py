from setuptools import find_packages, setup

setup(
    name='gazebo_robot_bridge',
    version='0.0.1',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/gazebo_robot_bridge']),
        ('share/gazebo_robot_bridge', ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='jayden',
    maintainer_email='jayden@example.com',
    description='Gazebo Robot Bridge - ROS2 to Gazebo Control',
    license='MIT',
    entry_points={
        'console_scripts': [
            'gazebo_bridge = gazebo_robot_bridge.gazebo_bridge_node:main',
        ],
    },
)
