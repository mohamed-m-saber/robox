# from launch import LaunchDescription
# from launch.actions import IncludeLaunchDescription
# from launch.actions import ExecuteProcess

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
#         # Silently launch MoveIt demo
#         ExecuteProcess(
#             cmd=['ros2', 'launch', demo_launch_path],
#             output='log'
#         ),

#         # Run the QR Action Server (Python node executable)
#         Node(
#             package='arduinobot_py_examples',
#             executable='ppc_action_server_stacking',
#             name='ppc_action_server_stacking',
#             output='log',
#             prefix='stdbuf -oL'        ),

#         # Run the QR Action Client (Python node executable)
#         Node(
#             package='color_pose_publisher',
#             executable='ppc_action_client',
#             name='ppc_action_client',
#             output='log',
#             prefix='stdbuf -oL'        ),
#     ])


from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration

from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    # Path to MoveIt demo.launch.py
    demo_launch_path = os.path.join(
        get_package_share_directory('robox_moveit_config'),
        'launch',
        'demo.launch.py'
    )

    # Declare color priority launch arguments
    blue_priority_arg = DeclareLaunchArgument('blue_priority', default_value='1')
    red_priority_arg = DeclareLaunchArgument('red_priority', default_value='2')
    green_priority_arg = DeclareLaunchArgument('green_priority', default_value='3')

    return LaunchDescription([
        # Declare arguments
        blue_priority_arg,
        red_priority_arg,
        green_priority_arg,

        # Include MoveIt demo
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(demo_launch_path)
        ),

        # Action Server node
        Node(
            package='arduinobot_py_examples',
            executable='ppc_action_server_stacking',
            name='ppc_action_server_stacking',
            output='screen',
            prefix='stdbuf -oL'
        ),

        # Action Client node with parameters
        Node(
            package='color_pose_publisher',
            executable='ppc_action_client',
            name='ppc_action_client',
            output='screen',
            prefix='stdbuf -oL',
            parameters=[{
                'blue_priority':  LaunchConfiguration('blue_priority'),
                'red_priority':   LaunchConfiguration('red_priority'),
                'green_priority': LaunchConfiguration('green_priority')
            }]
        ),
    ])
