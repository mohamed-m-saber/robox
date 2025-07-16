from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():
    # Path to demo.launch.py
    demo_launch_path = os.path.join(
        get_package_share_directory('robox_moveit_config'),
        'launch',
        'demo.launch.py'
    )

    return LaunchDescription([
        # Include MoveIt demo launch file
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(demo_launch_path)
        ),

        # Run the QR Action Server (Python node executable)
        Node(
            package='arduinobot_py_examples',
            executable='qr_action_server',
            name='qr_action_server',
            output='screen'
        ),

        # Run the QR Action Client (Python node executable)
        Node(
            package='color_pose_publisher',
            executable='qr_action_client',
            name='qr_action_client',
            output='screen'
        ),
    ])
