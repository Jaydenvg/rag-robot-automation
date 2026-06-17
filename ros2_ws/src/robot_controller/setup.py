from setuptools import find_packages, setup

setup(
    name='robot_controller',
    version='0.0.1',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/robot_controller']),
        ('share/robot_controller', ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='jayden',
    maintainer_email='jayden@example.com',
    description='Robot Controller Node for ROS2',
    license='MIT',
    entry_points={
        'console_scripts': [
            'robot_controller = robot_controller.robot_controller_node:main',
        ],
    },
)
