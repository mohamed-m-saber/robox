from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():
    demo_launch_path = os.path.join(
        get_package_share_directory('robox_moveit_config'),
        'launch',
        'demo.launch.py'
    )

    return LaunchDescription([
        # Silently launch MoveIt demo
        ExecuteProcess(
            cmd=['ros2', 'launch', demo_launch_path],
            output='log'
        ),

        # Action Server node: print() only, ROS logs to file
        Node(
            package='arduinobot_py_examples',
            executable='ppc_action_server',
            name='ppc_action_server',
            output='log',
            prefix='stdbuf -oL'
        ),

        # Action Client node: print() only, ROS logs to file
        Node(
            package='color_pose_publisher',
            executable='ppc_action_client',
            name='ppc_action_client',
            output='log',
            prefix='stdbuf -oL'
        ),
    ])
