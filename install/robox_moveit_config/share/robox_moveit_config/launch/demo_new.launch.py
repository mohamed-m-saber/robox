# from launch import LaunchDescription
# from launch.actions import SetEnvironmentVariable, TimerAction
# from launch_ros.actions import Node, SetParameter
# from launch_ros.parameter_descriptions import ParameterValue
# from moveit_configs_utils import MoveItConfigsBuilder
# from launch.substitutions import Command, PathJoinSubstitution
# from launch_ros.substitutions import FindPackageShare
# import os
# import yaml
# from ament_index_python.packages import get_package_share_directory

# def generate_launch_description():
#     # Set ROS_DOMAIN_ID
#     set_domain_id = SetEnvironmentVariable('ROS_DOMAIN_ID', '3')
    
#     # Generate robot description URDF
#     robot_description_content = ParameterValue(
#         Command([
#             'xacro ',
#             PathJoinSubstitution([
#                 FindPackageShare("robox_moveit_config"),
#                 "config",
#                 "robox_arm.urdf.xacro"
#             ])
#         ]),
#         value_type=str
#     )
    
#     # Set global robot_description parameter
#     set_robot_description = SetParameter(name='robot_description', value=robot_description_content)
    
#     # MoveIt config builder with file paths
#     moveit_config = (
#         MoveItConfigsBuilder("robox_arm", package_name="robox_moveit_config")
#         .robot_description(file_path="config/robox_arm.urdf.xacro")
#         .robot_description_semantic(file_path="config/robox_arm.srdf")
#         .robot_description_kinematics(file_path="config/kinematics.yaml")
#         .planning_pipelines(pipelines=["ompl"])
#         .trajectory_execution(file_path="config/moveit_controllers.yaml")
#         .planning_scene_monitor(
#             publish_robot_description=True, 
#             publish_robot_description_semantic=True
#         )
#         .to_moveit_configs()
#     )
    
#     # Load kinematics.yaml explicitly
#     kinematics_yaml_path = os.path.join(
#         get_package_share_directory("robox_moveit_config"),
#         "config",
#         "kinematics.yaml"
#     )
#     with open(kinematics_yaml_path, 'r') as file:
#         kinematics_yaml = yaml.safe_load(file)
    
#     # Load controllers configuration
#     controllers_yaml = PathJoinSubstitution([
#         FindPackageShare("robox_moveit_config"),
#         "config",
#         "ros2_controllers.yaml"
#     ])
    
#     # Load planning parameters
#     planning_params = {
#         'robot_description_planning': {
#             'cartesian_limits': {
#                 'max_trans_vel': 1.0,
#                 'max_trans_acc': 2.25,
#                 'max_trans_dec': -5.0,
#                 'max_rot_vel': 1.57,
#                 'max_rot_acc': 3.5,
#                 'max_rot_dec': -5.0
#             },
#             'joint_limits': {
#                 'joint_one': {
#                     'has_velocity_limits': True,
#                     'max_velocity': 1.0,
#                     'has_acceleration_limits': True,
#                     'max_acceleration': 1.0
#                 },
#                 'joint_two': {
#                     'has_velocity_limits': True,
#                     'max_velocity': 1.0,
#                     'has_acceleration_limits': True,
#                     'max_acceleration': 1.0
#                 },
#                 'joint_three': {
#                     'has_velocity_limits': True,
#                     'max_velocity': 1.0,
#                     'has_acceleration_limits': True,
#                     'max_acceleration': 1.0
#                 },
#                 'joint_four': {
#                     'has_velocity_limits': True,
#                     'max_velocity': 1.0,
#                     'has_acceleration_limits': True,
#                     'max_acceleration': 1.0
#                 },
#                 'joint_five': {
#                     'has_velocity_limits': True,
#                     'max_velocity': 1.0,
#                     'has_acceleration_limits': True,
#                     'max_acceleration': 1.0
#                 },
#                 'joint_six': {
#                     'has_velocity_limits': True,
#                     'max_velocity': 1.0,
#                     'has_acceleration_limits': True,
#                     'max_acceleration': 0.5
#                 },
#                 'joint_seven': {
#                     'has_velocity_limits': True,
#                     'max_velocity': 1.0,
#                     'has_acceleration_limits': True,
#                     'max_acceleration': 0.5
#                 }
#             }
#         },
#         'robot_description_kinematics': kinematics_yaml
#     }
    
#     # Robot state publisher node
#     robot_state_publisher_node = Node(
#         package="robot_state_publisher",
#         executable="robot_state_publisher",
#         parameters=[
#             {
#                 'robot_description': robot_description_content,
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
#             {
#                 'robot_description': robot_description_content,
#             },
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
#         arguments=["arm_controller", "--controller-manager", "/controller_manager"],
#         output="screen"
#     )
    
#     # Gripper controller spawner
#     gripper_controller_spawner = Node(
#         package="controller_manager",
#         executable="spawner",
#         arguments=["gripper_controller", "--controller-manager", "/controller_manager"],
#         output="screen"
#     )
    
#     # Move group node with explicit robot description and kinematics
#     move_group_node = Node(
#         package="moveit_ros_move_group",
#         executable="move_group",
#         output="screen",
#         parameters=[
#             {
#                 'robot_description': robot_description_content,
#                 'octomap_frame': '',  # Disable Octomap
#             },
#             moveit_config.to_dict(),
#             planning_params,
#             kinematics_yaml
#         ]
#     )
    
#     # RViz node
#     rviz_config_file = PathJoinSubstitution([
#         FindPackageShare("robox_moveit_config"),
#         "config",
#         "moveit.rviz"
#     ])
    
#     rviz_node = Node(
#         package="rviz2",
#         executable="rviz2",
#         name="rviz2",
#         arguments=["-d", rviz_config_file],
#         parameters=[
#             {
#                 'robot_description': robot_description_content,
#             },
#             moveit_config.robot_description_semantic,
#             kinematics_yaml
#         ],
#         output="screen"
#     )
    
#     # Sequential launch with proper timing
#     return LaunchDescription([
#         set_domain_id,
#         set_robot_description,
        
#         # Start robot state publisher first
#         robot_state_publisher_node,
        
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
#             period=7.0,
#             actions=[rviz_node]
#         )
#     ])















from launch import LaunchDescription
from launch.actions import SetEnvironmentVariable, TimerAction
from launch_ros.actions import Node, SetParameter
from moveit_configs_utils import MoveItConfigsBuilder
from launch.substitutions import Command, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare
import os
import yaml
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    # Set ROS_DOMAIN_ID for DDS isolation
    set_domain_id = SetEnvironmentVariable('ROS_DOMAIN_ID', '3')

    # Robot description (URDF)
    robot_description_content = Command([
        'xacro ',
        PathJoinSubstitution([
            FindPackageShare("robox_moveit_config"),
            "config",
            "robox_arm.urdf.xacro"
        ])
    ])

    # Load kinematics.yaml
    kinematics_yaml_path = os.path.join(
        get_package_share_directory("robox_moveit_config"),
        "config",
        "kinematics.yaml"
    )
    with open(kinematics_yaml_path, 'r') as file:
        kinematics_yaml = yaml.safe_load(file)

    # Load moveit_controllers.yaml
    moveit_controllers_yaml_path = os.path.join(
        get_package_share_directory("robox_moveit_config"),
        "config",
        "moveit_controllers.yaml"
    )
    with open(moveit_controllers_yaml_path, 'r') as file:
        moveit_controllers_yaml = yaml.safe_load(file)

    # Load MoveIt config using MoveItConfigsBuilder
    moveit_config = (
        MoveItConfigsBuilder("robox_arm", package_name="robox_moveit_config")
        .robot_description(file_path="config/robox_arm.urdf.xacro")
        .robot_description_semantic(file_path="config/robox_arm.srdf")
        .robot_description_kinematics(file_path="config/kinematics.yaml")
        .planning_pipelines(pipelines=["ompl"])
        .planning_scene_monitor(
            publish_robot_description=True,
            publish_robot_description_semantic=True
        )
        .to_moveit_configs()
    )

    # Planning parameters (joint limits etc.)
    planning_params = {
        'robot_description_planning': {
            'cartesian_limits': {
                'max_trans_vel': 1.0,
                'max_trans_acc': 2.25,
                'max_trans_dec': -5.0,
                'max_rot_vel': 1.57,
                'max_rot_acc': 3.5,
                'max_rot_dec': -5.0
            },
            'joint_limits': {
                'joint_one': {
                    'has_velocity_limits': True,
                    'max_velocity': 1.0,
                    'has_acceleration_limits': True,
                    'max_acceleration': 1.0
                },
                'joint_two': {
                    'has_velocity_limits': True,
                    'max_velocity': 1.0,
                    'has_acceleration_limits': True,
                    'max_acceleration': 1.0
                },
                'joint_three': {
                    'has_velocity_limits': True,
                    'max_velocity': 1.0,
                    'has_acceleration_limits': True,
                    'max_acceleration': 1.0
                },
                'joint_four': {
                    'has_velocity_limits': True,
                    'max_velocity': 1.0,
                    'has_acceleration_limits': True,
                    'max_acceleration': 1.0
                },
                'joint_five': {
                    'has_velocity_limits': True,
                    'max_velocity': 1.0,
                    'has_acceleration_limits': True,
                    'max_acceleration': 1.0
                },
                'joint_six': {
                    'has_velocity_limits': True,
                    'max_velocity': 1.0,
                    'has_acceleration_limits': True,
                    'max_acceleration': 0.5
                },
                'joint_seven': {
                    'has_velocity_limits': True,
                    'max_velocity': 1.0,
                    'has_acceleration_limits': True,
                    'max_acceleration': 0.5
                }
            }
        },
        'robot_description_kinematics': kinematics_yaml
    }

    # Controller config YAML path
    controllers_yaml = PathJoinSubstitution([
        FindPackageShare("robox_moveit_config"),
        "config",
        "ros2_controllers.yaml"
    ])

    # Robot state publisher
    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[
            {'robot_description': robot_description_content}
        ],
        output="screen"
    )

    # Controller manager
    control_node = Node(
        package="controller_manager",
        executable="ros2_control_node",
        parameters=[
            {'robot_description': robot_description_content},
            controllers_yaml
        ],
        output="screen"
    )

    # Spawner nodes
    joint_state_broadcaster_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_state_broadcaster", "--controller-manager", "/controller_manager"],
        output="screen"
    )

    arm_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["arm_controller", "--controller-manager", "/controller_manager"],
        output="screen"
    )

    # gripper_controller_spawner = Node(
    #     package="controller_manager",
    #     executable="spawner",
    #     arguments=["gripper_controller", "--controller-manager", "/controller_manager"],
    #     output="screen"
    # )

    # Move group node
    move_group_node = Node(
        package="moveit_ros_move_group",
        executable="move_group",
        output="screen",
        parameters=[
            {'robot_description': robot_description_content},
            moveit_config.to_dict(),
            planning_params,
            moveit_controllers_yaml
        ]
    )

    # RViz config file
    rviz_config_file = PathJoinSubstitution([
        FindPackageShare("robox_moveit_config"),
        "config",
        "moveit.rviz"
    ])

    # RViz node
    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        arguments=["-d", rviz_config_file],
        parameters=[
            {'robot_description': robot_description_content},
            moveit_config.robot_description_semantic,
            kinematics_yaml
        ],
        output="screen"
    )

    # Launch description
    return LaunchDescription([
        set_domain_id,
        robot_state_publisher_node,
        control_node,
        TimerAction(period=2.0, actions=[joint_state_broadcaster_spawner]),
        TimerAction(period=3.0, actions=[arm_controller_spawner]),
        # TimerAction(period=4.0, actions=[gripper_controller_spawner]),
        TimerAction(period=5.0, actions=[move_group_node]),
        TimerAction(period=7.0, actions=[rviz_node])
    ])









