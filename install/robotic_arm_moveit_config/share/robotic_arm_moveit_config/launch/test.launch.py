from launch import LaunchDescription
from launch.actions import SetEnvironmentVariable, RegisterEventHandler, TimerAction
from launch.event_handlers import OnProcessStart
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from moveit_configs_utils import MoveItConfigsBuilder
from launch.substitutions import Command, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare
import os

def generate_launch_description():
    # Set ROS_DOMAIN_ID
    set_domain_id = SetEnvironmentVariable('ROS_DOMAIN_ID', '9')
    
    # MoveIt config builder with file paths
    moveit_config = (
        MoveItConfigsBuilder("robotic_arm", package_name="robotic_arm_moveit_config")
        .robot_description(file_path="config/robotic_arm.urdf.xacro")  # Fixed path
        .robot_description_semantic(file_path="config/robotic_arm.srdf")
        .robot_description_kinematics(file_path="config/kinematics.yaml")
        .planning_pipelines(pipelines=["ompl"])  # Only use OMPL to avoid Pilz issues
        .trajectory_execution(file_path="config/moveit_controllers.yaml")
        .planning_scene_monitor(
            publish_robot_description=True, 
            publish_robot_description_semantic=True
        )
        .to_moveit_configs()
    )
    
    # Load controllers configuration
    controllers_yaml = PathJoinSubstitution([
        FindPackageShare("robotic_arm_moveit_config"),
        "config",
        "ros2_controllers.yaml"
    ])
    
    # Load planning parameters - use dict if file doesn't exist
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
                'rotating_base_joint': {
                    'has_velocity_limits': True,
                    'max_velocity': 1.0,
                    'has_acceleration_limits': True,
                    'max_acceleration': 1.0
                },
                'shoulder_joint': {
                    'has_velocity_limits': True,
                    'max_velocity': 1.0,
                    'has_acceleration_limits': True,
                    'max_acceleration': 1.0
                },
                'elbow_joint': {
                    'has_velocity_limits': True,
                    'max_velocity': 1.0,
                    'has_acceleration_limits': True,
                    'max_acceleration': 1.0
                },
                'forearm_joint': {
                    'has_velocity_limits': True,
                    'max_velocity': 1.0,
                    'has_acceleration_limits': True,
                    'max_acceleration': 1.0
                },
                'wrist_joint': {
                    'has_velocity_limits': True,
                    'max_velocity': 1.0,
                    'has_acceleration_limits': True,
                    'max_acceleration': 1.0
                }
            #     'gripper_right_joint': {
            #         'has_velocity_limits': True,
            #         'max_velocity': 1.0,
            #         'has_acceleration_limits': True,
            #         'max_acceleration': 1.0
            #     }
             }
        }
    }
    
    # Robot state publisher node with XACRO processing
    robot_state_publisher_node = Node(
    package="robot_state_publisher",
    executable="robot_state_publisher",
    parameters=[
        {
            'robot_description': ParameterValue(
                Command([
                    'xacro ',
                    PathJoinSubstitution([
                        FindPackageShare("robotic_arm_moveit_config"),
                        "config",
                        "robotic_arm.urdf.xacro"
                    ])
                ]),
                value_type=str
            ),
            'use_sim_time': False  # Fix for timestamp synchronization
        }
    ],
    output="screen"
)
    
    # Controller manager node
    control_node = Node(
        package="controller_manager",
        executable="ros2_control_node",
        parameters=[
            moveit_config.robot_description,
            controllers_yaml
        ],
        output="screen"
    )
    
    # Joint state broadcaster spawner
    joint_state_broadcaster_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_state_broadcaster", "--controller-manager", "/controller_manager"],
        output="screen"
    )
    
    # Arm controller spawner
    arm_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["arm", "--controller-manager", "/controller_manager"],
        output="screen"
    )
    
    # Gripper controller spawner
    gripper_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["gripper", "--controller-manager", "/controller_manager"],
        output="screen"
    )
    
    # Move group node with proper parameter handling
    move_group_node = Node(
        package="moveit_ros_move_group",
        executable="move_group",
        output="screen",
        parameters=[
            moveit_config.to_dict(),
            planning_params
        ],
        arguments=["--ros-args", "--log-level", "info"],
    )
    
    # RViz node
    rviz_config_file = PathJoinSubstitution([
        FindPackageShare("robotic_arm_moveit_config"),
        "config",
        "moveit.rviz"
    ])
    
    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        arguments=["-d", rviz_config_file],
        parameters=[
            moveit_config.robot_description,
            moveit_config.robot_description_semantic,
            moveit_config.robot_description_kinematics,
        ],
        output="screen"
    )
    
    # Sequential launch with proper timing
    return LaunchDescription([
        set_domain_id,
        
        # Start robot state publisher and control node first
        robot_state_publisher_node,
        control_node,
        
        # Wait a bit then spawn controllers
        TimerAction(
            period=2.0,
            actions=[joint_state_broadcaster_spawner]
        ),
        
        TimerAction(
            period=3.0,
            actions=[arm_controller_spawner]
        ),
        
        TimerAction(
            period=4.0,
            actions=[gripper_controller_spawner]
        ),
        
        # Wait for controllers to be ready then start move_group
        TimerAction(
            period=5.0,
            actions=[move_group_node]
        ),
        
        # Finally start RViz
        TimerAction(
            period=6.0,
            actions=[rviz_node]
        )
    ])





# from launch import LaunchDescription
# from launch.actions import SetEnvironmentVariable, RegisterEventHandler
# from launch.event_handlers import OnProcessStart
# from launch_ros.actions import Node
# from launch_ros.parameter_descriptions import ParameterValue
# from moveit_configs_utils import MoveItConfigsBuilder
# from launch.substitutions import Command, PathJoinSubstitution
# from launch_ros.substitutions import FindPackageShare


# def generate_launch_description():
#     # Set ROS_DOMAIN_ID
#     set_domain_id = SetEnvironmentVariable('ROS_DOMAIN_ID', '9')

#     # MoveIt config builder
#     moveit_config = (
#         MoveItConfigsBuilder("robotic_arm", package_name="robotic_arm_moveit_config")
#         .robot_description(file_path="config/robotic_arm.urdf.xacro")
#         .robot_description_semantic(file_path="config/robotic_arm.srdf")
#         .robot_description_kinematics(file_path="config/kinematics.yaml")
#         .planning_pipelines(pipelines=["ompl"])
#         .trajectory_execution(file_path="config/moveit_controllers.yaml")
#         .planning_scene_monitor(
#             publish_robot_description=True, 
#             publish_robot_description_semantic=True
#         )
#         .to_moveit_configs()
#     )

#     # Controllers config
#     controllers_yaml = PathJoinSubstitution([
#         FindPackageShare("robotic_arm_moveit_config"),
#         "config",
#         "ros2_controllers.yaml"
#     ])

#     # Planning params (optional overrides)
#     planning_params = {
#         'robot_description_planning': {
#             'cartesian_limits': {
#                 'max_trans_vel': 1.0,
#                 'max_trans_acc': 2.25,
#                 'max_trans_dec': -5.0,
#                 'max_rot_vel': 1.57,
#                 'max_rot_acc': 3.5,
#                 'max_rot_dec': -5.0
#             }
#         }
#     }

#     # Robot state publisher node
#     robot_state_publisher_node = Node(
#         package="robot_state_publisher",
#         executable="robot_state_publisher",
#         parameters=[
#             {
#                 'robot_description': ParameterValue(
#                     Command([
#                         'xacro ',
#                         PathJoinSubstitution([
#                             FindPackageShare("robotic_arm_moveit_config"),
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

#     # Spawner nodes
#     joint_state_broadcaster_spawner = Node(
#         package="controller_manager",
#         executable="spawner",
#         arguments=["joint_state_broadcaster"],
#         output="screen"
#     )

#     arm_controller_spawner = Node(
#         package="controller_manager",
#         executable="spawner",
#         arguments=["arm"],
#         output="screen"
#     )

#     gripper_controller_spawner = Node(
#         package="controller_manager",
#         executable="spawner",
#         arguments=["gripper"],
#         output="screen"
#     )

#     # Move group node
#     move_group_node = Node(
#         package="moveit_ros_move_group",
#         executable="move_group",
#         output="screen",
#         parameters=[
#             moveit_config.to_dict(),
#             planning_params
#         ],
#         arguments=["--ros-args", "--log-level", "info"],
#     )

#     # RViz node
#     rviz_config_file = PathJoinSubstitution([
#         FindPackageShare("robotic_arm_moveit_config"),
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
#         ],
#         output="screen"
#     )

#     # IK Node
#     ik_node = Node(
#         package="arm_description",
#         executable="robot_arm_ik_node",
#         output="screen"
#     )

#     # Event-driven launch sequence
#     event_handlers = [
#         # When control_node starts, start joint_state_broadcaster
#         RegisterEventHandler(
#             OnProcessStart(
#                 target_action=control_node,
#                 on_start=[joint_state_broadcaster_spawner]
#             )
#         ),
#         # When joint_state_broadcaster starts, start arm controller
#         RegisterEventHandler(
#             OnProcessStart(
#                 target_action=joint_state_broadcaster_spawner,
#                 on_start=[arm_controller_spawner]
#             )
#         ),
#         # When arm controller starts, start gripper controller
#         RegisterEventHandler(
#             OnProcessStart(
#                 target_action=arm_controller_spawner,
#                 on_start=[gripper_controller_spawner]
#             )
#         ),
#         # When gripper controller starts, start move_group
#         RegisterEventHandler(
#             OnProcessStart(
#                 target_action=gripper_controller_spawner,
#                 on_start=[move_group_node]
#             )
#         ),
#         # When move_group starts, start RViz and IK node
#         RegisterEventHandler(
#             OnProcessStart(
#                 target_action=move_group_node,
#                 on_start=[rviz_node, ik_node]
#             )
#         )
#     ]

#     return LaunchDescription([
#         set_domain_id,
#         robot_state_publisher_node,
#         control_node,
#         *event_handlers
#     ])

# from launch import LaunchDescription
# from launch.actions import DeclareLaunchArgument, SetEnvironmentVariable, RegisterEventHandler
# from launch.event_handlers import OnProcessStart
# from launch.substitutions import LaunchConfiguration, Command, PathJoinSubstitution
# from launch_ros.actions import Node
# from launch_ros.parameter_descriptions import ParameterValue
# from launch_ros.substitutions import FindPackageShare
# from moveit_configs_utils import MoveItConfigsBuilder

# def generate_launch_description():
#     # Declare launch argument for RMW implementation
#     declare_rmw_arg = DeclareLaunchArgument(
#         'rmw_implementation',
#         default_value='rmw_fastrtps_cpp',
#         description='RMW implementation to use (e.g. rmw_fastrtps_cpp, rmw_cyclonedds_cpp)'
#     )
#     rmw_implementation = LaunchConfiguration('rmw_implementation')

#     # Set the environment variable dynamically based on the argument
#     set_rmw_implementation = SetEnvironmentVariable(
#         name='RMW_IMPLEMENTATION',
#         value=rmw_implementation
#     )

#     set_domain_id = SetEnvironmentVariable('ROS_DOMAIN_ID', '9')

#     moveit_config = (
#         MoveItConfigsBuilder("robotic_arm", package_name="robotic_arm_moveit_config")
#         .robot_description(file_path="config/robotic_arm.urdf.xacro")
#         .robot_description_semantic(file_path="config/robotic_arm.srdf")
#         .robot_description_kinematics(file_path="config/kinematics.yaml")
#         .planning_pipelines(pipelines=["ompl"])
#         .trajectory_execution(file_path="config/moveit_controllers.yaml")
#         .planning_scene_monitor(
#             publish_robot_description=True,
#             publish_robot_description_semantic=True
#         )
#         .to_moveit_configs()
#     )

#     controllers_yaml = PathJoinSubstitution([
#         FindPackageShare("robotic_arm_moveit_config"),
#         "config",
#         "ros2_controllers.yaml"
#     ])

#     planning_params = {
#         'robot_description_planning': {
#             'cartesian_limits': {
#                 'max_trans_vel': 1.0,
#                 'max_trans_acc': 2.25,
#                 'max_trans_dec': -5.0,
#                 'max_rot_vel': 1.57,
#                 'max_rot_acc': 3.5,
#                 'max_rot_dec': -5.0
#             }
#         }
#     }

#     robot_state_publisher_node = Node(
#         package="robot_state_publisher",
#         executable="robot_state_publisher",
#         name="robot_state_publisher_unique",
#         parameters=[
#             {
#                 'robot_description': ParameterValue(
#                     Command([
#                         'xacro ',
#                         PathJoinSubstitution([
#                             FindPackageShare("robotic_arm_moveit_config"),
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

#     control_node = Node(
#         package="controller_manager",
#         executable="ros2_control_node",
#         parameters=[
#             moveit_config.robot_description,
#             controllers_yaml,
#             {"use_sim_time": False}
#         ],
#         output="screen"
#     )

#     joint_state_broadcaster_spawner = Node(
#         package="controller_manager",
#         executable="spawner",
#         arguments=["joint_state_broadcaster"],
#         output="screen"
#     )

#     arm_controller_spawner = Node(
#         package="controller_manager",
#         executable="spawner",
#         arguments=["arm"],
#         output="screen"
#     )

#     gripper_controller_spawner = Node(
#         package="controller_manager",
#         executable="spawner",
#         arguments=["gripper"],
#         output="screen"
#     )

#     move_group_node = Node(
#         package="moveit_ros_move_group",
#         executable="move_group",
#         name="move_group_unique",
#         output="screen",
#         parameters=[
#             moveit_config.to_dict(),
#             planning_params,
#             {"use_sim_time": False}
#         ],
#         arguments=["--ros-args", "--log-level", "info"]
#     )

#     rviz_config_file = PathJoinSubstitution([
#         FindPackageShare("robotic_arm_moveit_config"),
#         "config",
#         "moveit.rviz"
#     ])

#     rviz_node = Node(
#         package="rviz2",
#         executable="rviz2",
#         name="rviz2_unique",
#         arguments=["-d", rviz_config_file],
#         parameters=[
#             moveit_config.robot_description,
#             moveit_config.robot_description_semantic,
#             moveit_config.robot_description_kinematics,
#             {"use_sim_time": False}
#         ],
#         output="screen"
#     )

#     ik_node = Node(
#         package="arm_description",
#         executable="robot_arm_ik_node",
#         name="go_to_pose_service_node_unique",
#         output="screen",
#         parameters=[
#             {"use_sim_time": False},
#             {"joint_state_topic": "/joint_states"},
#             {"monitored_state_timeout": 2.0}
#         ]
#     )

#     event_handlers = [
#         RegisterEventHandler(
#             OnProcessStart(
#                 target_action=control_node,
#                 on_start=[joint_state_broadcaster_spawner]
#             )
#         ),
#         RegisterEventHandler(
#             OnProcessStart(
#                 target_action=joint_state_broadcaster_spawner,
#                 on_start=[arm_controller_spawner]
#             )
#         ),
#         RegisterEventHandler(
#             OnProcessStart(
#                 target_action=arm_controller_spawner,
#                 on_start=[gripper_controller_spawner]
#             )
#         ),
#         RegisterEventHandler(
#             OnProcessStart(
#                 target_action=gripper_controller_spawner,
#                 on_start=[move_group_node]
#             )
#         ),
#         RegisterEventHandler(
#             OnProcessStart(
#                 target_action=move_group_node,
#                 on_start=[rviz_node, ik_node]
#             )
#         )
#     ]

#     return LaunchDescription([
#         declare_rmw_arg,
#         set_domain_id,
#         set_rmw_implementation,
#         robot_state_publisher_node,
#         control_node,
#         *event_handlers
#     ])

