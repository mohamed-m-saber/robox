

# from launch import LaunchDescription
# from launch.actions import SetEnvironmentVariable, RegisterEventHandler, TimerAction
# from launch.event_handlers import OnProcessStart
# from launch_ros.actions import Node
# from launch_ros.parameter_descriptions import ParameterValue
# from moveit_configs_utils import MoveItConfigsBuilder
# from launch.substitutions import Command, PathJoinSubstitution
# from launch_ros.substitutions import FindPackageShare
# import os

# def generate_launch_description():
#     # Set ROS_DOMAIN_ID
#     set_domain_id = SetEnvironmentVariable('ROS_DOMAIN_ID', '7')
    
#     # MoveIt config builder with file paths
#     moveit_config = (
#         MoveItConfigsBuilder("robotic_arm", package_name="moveit_config")
#         .robot_description(file_path="config/robotic_arm.urdf.xacro")
#         .robot_description_semantic(file_path="config/robotic_arm.srdf")
#         .robot_description_kinematics(file_path="config/kinematics.yaml")
#         .planning_pipelines(pipelines=["ompl","chomp","pilz_industrial_motion_planner"])
#         .trajectory_execution(file_path="config/moveit_controllers.yaml")
#         .planning_scene_monitor(
#             publish_robot_description=True, 
#             publish_robot_description_semantic=True
#         )
#         .to_moveit_configs()
#     )
    
#     # Load controllers configuration
#     controllers_yaml = PathJoinSubstitution([
#         FindPackageShare("moveit_config"),
#         "config",
#         "ros2_controllers.yaml"
#     ])
    
   
#     # Robot state publisher node with XACRO processing
#     robot_state_publisher_node = Node(
#         package="robot_state_publisher",
#         executable="robot_state_publisher",
#         parameters=[
#             {
#                 'robot_description': ParameterValue(
#                     Command([
#                         'xacro ',
#                         PathJoinSubstitution([
#                             FindPackageShare("moveit_config"),
#                             "config",
#                             "robotic_arm.urdf.xacro"
#                         ])
#                     ]),
#                     value_type=str
#                 ),
#                 'use_sim_time': False
#             }
#         ],
#         output="screen"
#     )
    
#     # ADD THIS: Joint State Publisher for initial joint positions
#     joint_state_publisher_node = Node(
#         package="joint_state_publisher",
#         executable="joint_state_publisher",
#         parameters=[
#             {
#                 'robot_description': ParameterValue(
#                     Command([
#                         'xacro ',
#                         PathJoinSubstitution([
#                             FindPackageShare("moveit_config"),
#                             "config",
#                             "robotic_arm.urdf.xacro"
#                         ])
#                     ]),
#                     value_type=str
#                 ),
#                 'use_sim_time': False
#             }
#         ],
#         output="screen"
#     )
    
#     # Controller manager node
#     control_node = Node(
#         package="controller_manager",
#         executable="ros2_control_node",
#         parameters=[
#             moveit_config.robot_description,
#             controllers_yaml
#         ],
#         output="screen"
#     )
    
#     # Joint state broadcaster spawner
#     joint_state_broadcaster_spawner = Node(
#         package="controller_manager",
#         executable="spawner",
#         arguments=["joint_state_broadcaster", "--controller-manager", "/controller_manager"],
#         output="screen"
#     )
    
#     # Arm controller spawner
#     arm_controller_spawner = Node(
#         package="controller_manager",
#         executable="spawner",
#         arguments=["arm", "--controller-manager", "/controller_manager"],
#         output="screen"
#     )
    
#     # Gripper controller spawner
#     gripper_controller_spawner = Node(
#         package="controller_manager",
#         executable="spawner",
#         arguments=["gripper", "--controller-manager", "/controller_manager"],
#         output="screen"
#     )
    
#     # Move group node with proper parameter handling
#     move_group_node = Node(
#         package="moveit_ros_move_group",
#         executable="move_group",
#         output="screen",
#         parameters=[moveit_config.to_dict(),],
#         arguments=["--ros-args", "--log-level", "info"],
#     )
    
#     # RViz node
#     rviz_config_file = PathJoinSubstitution([
#         FindPackageShare("moveit_config"),
#         "config",
#         "moveit.rviz"
#     ])
    
#     rviz_node = Node(
#         package="rviz2",
#         executable="rviz2",
#         name="rviz2",
#         arguments=["-d", rviz_config_file],
#         parameters=[
#             moveit_config.robot_description,
#             moveit_config.robot_description_semantic,
#             moveit_config.robot_description_kinematics,
#             moveit_config.planning_pipelines,
#         ],
#         output="screen"
#     )
    
#     # Sequential launch with proper timing
#     return LaunchDescription([
#         set_domain_id,
        
#         # Start robot state publisher first
#         robot_state_publisher_node,
        
#         # ADD THIS: Start joint state publisher
#         joint_state_publisher_node,
        
#         # Start control node
#         control_node,
        
#         # Wait a bit then spawn controllers
#         TimerAction(
#             period=2.0,
#             actions=[joint_state_broadcaster_spawner]
#         ),
        
#         TimerAction(
#             period=3.0,
#             actions=[arm_controller_spawner]
#         ),
        
#         TimerAction(
#             period=4.0,
#             actions=[gripper_controller_spawner]
#         ),
        
#         # Wait for controllers to be ready then start move_group
#         TimerAction(
#             period=5.0,
#             actions=[move_group_node]
#         ),
        
#         # Finally start RViz
#         TimerAction(
#             period=6.0,
#             actions=[rviz_node]
#         )
#     ])










from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, SetEnvironmentVariable, TimerAction
from launch.substitutions import Command, LaunchConfiguration, PathJoinSubstitution
from launch.conditions import IfCondition
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.substitutions import FindPackageShare
from moveit_configs_utils import MoveItConfigsBuilder

def generate_launch_description():
    # Declare launch arguments
    ros_domain_id = DeclareLaunchArgument(
        "ros_domain_id",
        default_value="7",
        description="ROS_DOMAIN_ID for the ROS 2 network"
    )
    use_gripper = DeclareLaunchArgument(
        "use_gripper",
        default_value="true",
        description="Whether to spawn the gripper controller"
    )

    # Set ROS_DOMAIN_ID
    set_domain_id = SetEnvironmentVariable('ROS_DOMAIN_ID', LaunchConfiguration('ros_domain_id'))

    # MoveIt config builder - following Panda pattern
    moveit_config = (
        MoveItConfigsBuilder("robotic_arm", package_name="moveit_config")
        .robot_description(file_path="config/robotic_arm.urdf.xacro")
        .robot_description_semantic(file_path="config/robotic_arm.srdf")
        .planning_scene_monitor(
            publish_robot_description=True,
            publish_robot_description_semantic=True
        )
        .trajectory_execution(file_path="config/moveit_controllers.yaml")
        .planning_pipelines(pipelines=["ompl", "chomp", "pilz_industrial_motion_planner"])
        .to_moveit_configs()
    )

    # Controller configuration
    controllers_yaml = PathJoinSubstitution([
        FindPackageShare("moveit_config"),
        "config",
        "ros2_controllers.yaml"
    ])

    # Robot state publisher
    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name="robot_state_publisher",
        output="screen",
        parameters=[moveit_config.robot_description]
    )

    # Controller manager
    control_node = Node(
        package="controller_manager",
        executable="ros2_control_node",
        parameters=[
            moveit_config.robot_description,
            controllers_yaml,
            {'use_sim_time': False}
        ],
        remappings=[
            ("/controller_manager/robot_description", "/robot_description"),
        ],
        output="screen"
    )

    # Static transform publisher
    static_tf = Node(
        package="tf2_ros",
        executable="static_transform_publisher",
        name="static_transform_publisher",
        output="log",
        arguments=["0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "world", "base_link"],
    )

    # Controller spawners
    joint_state_broadcaster_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_state_broadcaster", "--controller-manager", "/controller_manager"],
        output="screen"
    )

    arm_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["arm", "-c", "/controller_manager"],
        output="screen"
    )

    gripper_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["gripper", "-c", "/controller_manager"],
        output="screen",
        condition=IfCondition(LaunchConfiguration('use_gripper'))
    )

    # Move group node - following Panda pattern
    move_group_node = Node(
        package="moveit_ros_move_group",
        executable="move_group",
        output="screen",
        parameters=[moveit_config.to_dict()],
        arguments=["--ros-args", "--log-level", "info"],
    )

    # RViz node
    rviz_config_file = PathJoinSubstitution([
        FindPackageShare("moveit_config"),
        "config",
        "moveit.rviz"
    ])

    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="log",
        arguments=["-d", rviz_config_file],
        parameters=[
            moveit_config.robot_description,
            moveit_config.robot_description_semantic,
            moveit_config.planning_pipelines,
            moveit_config.robot_description_kinematics,
            moveit_config.joint_limits,
        ],
    )

    # Launch description with timed startup
    return LaunchDescription([
        ros_domain_id,
        use_gripper,
        set_domain_id,
        static_tf,
        robot_state_publisher_node,
        control_node,
        TimerAction(period=2.0, actions=[joint_state_broadcaster_spawner]),
        TimerAction(period=5.0, actions=[arm_controller_spawner]),
        TimerAction(period=6.0, actions=[gripper_controller_spawner]),
        TimerAction(period=7.0, actions=[move_group_node]),
        TimerAction(period=8.0, actions=[rviz_node]),
    ])