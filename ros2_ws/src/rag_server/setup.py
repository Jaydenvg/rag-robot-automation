from setuptools import find_packages, setup

setup(
    name='rag_server',
    version='0.0.1',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/rag_server']),
        ('share/rag_server', ['package.xml']),
        ('share/rag_server/launch', ['launch/rag_server.launch.py', 'launch/complete_system.launch.py']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='jayden',
    maintainer_email='jayden@example.com',
    description='RAG Server',
    license='MIT',
    entry_points={
        'console_scripts': [
            'rag_server = rag_server.rag_server_node:main',
        ],
    },
)
