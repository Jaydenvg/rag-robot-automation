from setuptools import find_packages, setup

setup(
    name='decision_maker',
    version='0.0.1',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/decision_maker']),
        ('share/decision_maker', ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='jayden',
    maintainer_email='jayden@example.com',
    description='Decision Maker Node for ROS2',
    license='MIT',
    entry_points={
        'console_scripts': [
            'decision_maker = decision_maker.decision_maker_node:main',
        ],
    },
)
