# from launch import LaunchDescription
# from launch.actions import IncludeLaunchDescription
# from launch.launch_description_sources import PythonLaunchDescriptionSource
# from launch_ros.actions import Node
# from ament_index_python.packages import get_package_share_directory
# import os


# def generate_launch_description():
#     # Path to demo.launch.py
#     demo_launch_path = os.path.join(
#         get_package_share_directory('robox_moveit_config'),
#         'launch',
#         'demo.launch.py'
#     )

#     return LaunchDescription([
#         # Include MoveIt demo launch file
#         IncludeLaunchDescription(
#             PythonLaunchDescriptionSource(demo_launch_path)
#         ),

#         # Run the QR Action Server (Python node executable)
#         Node(
#             package='arduinobot_py_examples',
#             executable='color_tracking_sub',
#             name='color_tracking_sub',
#             output='screen'
#         ),

#         # Run the QR Action Client (Python node executable)
#         Node(
#             package='color_pose_publisher',
#             executable='color_tracking_pub',
#             name='color_tracking_pub',
#             output='screen'
#         ),
#     ])










from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.substitutions import LaunchConfiguration
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
        # Declare target_color launch argument
        DeclareLaunchArgument(
            'target_color',
            default_value='Blue',
            description='Color to track'
        ),

        # Include MoveIt demo launch file
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(demo_launch_path)
        ),

        # Run the QR Action Server (Python node executable)
        Node(
            package='arduinobot_py_examples',
            executable='color_tracking_sub',
            name='color_tracking_sub',
            output='screen'
        ),

        # Run the Color Pose Publisher with target_color param
        Node(
            package='color_pose_publisher',
            executable='color_tracking_pub',
            name='color_tracking_pub',
            output='screen',
            parameters=[{
                'target_color': LaunchConfiguration('target_color')
            }]
        ),
    ])
