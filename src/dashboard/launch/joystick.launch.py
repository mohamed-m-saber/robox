from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():
    # Path to demo.launch.py
    demo_launch_path = os.path.join(
        get_package_share_directory('robox_arm'),
        'launch',
        'joystick_arm_display.launch.py'
    )

    return LaunchDescription([
        # Include MoveIt demo launch file
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(demo_launch_path)
        ),

        Node(
            package='arduinobot_py_examples',
            executable='joystick_controller',
            name='joystick_controller',
            output='screen'
        ),

        Node(
            package='joy',
            executable='joy_node',
            name='joy_node',
            output='screen'
        ),
    ])






