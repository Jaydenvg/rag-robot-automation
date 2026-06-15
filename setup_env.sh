#!/bin/bash

# Source ROS2
source /opt/ros/jazzy/setup.bash

# Navigate to project
cd ~/rag_robot_automation

# Activate Python virtual environment
source venv_rag/bin/activate

# Source ROS2 workspace
cd ros2_ws
source install/setup.bash
cd ..

echo "Environment setup complete!"
echo "Python venv: activated"
echo "ROS2: Jazzy"
echo "Ready to work on RAG Automation Project"
