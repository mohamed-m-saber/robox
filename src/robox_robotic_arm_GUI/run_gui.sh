#!/bin/bash
source /opt/ros/jazzy/setup.bash
source ~/robox_ws/install/setup.bash
cd ~/robox_ws/src/robox_robotic_arm_GUI
source venv/bin/activate
python3 main.py
