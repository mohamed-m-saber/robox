from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import Command
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    urdf_file = os.path.join(
        get_package_share_directory("robox_arm"),
        "urdf",
        "robox_arm.urdf"
    )

    robot_description = Command(["cat ", urdf_file])

    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[{"robot_description": robot_description}],
        output="screen"
    )

    rviz_config_file = os.path.join(
        get_package_share_directory("robox_arm"),
        "rviz",
        "robot.rviz"
    )

    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="screen",
        arguments=["-d", rviz_config_file]
    )

    return LaunchDescription([
        robot_state_publisher,
        rviz_node
    ])
