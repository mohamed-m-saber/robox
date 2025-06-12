from launch import LaunchDescription
from launch.actions import SetEnvironmentVariable, DeclareLaunchArgument, TimerAction, RegisterEventHandler, OpaqueFunction
from launch.event_handlers import OnProcessStart
from launch.substitutions import LaunchConfiguration, Command, FindExecutable, PathJoinSubstitution
from launch.conditions import IfCondition
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from ament_index_python.packages import get_package_share_directory
import os
import yaml


def load_file(package_name, file_path):
    """Load file content"""
    package_path = get_package_share_directory(package_name)
    absolute_file_path = os.path.join(package_path, file_path)
    
    if not os.path.exists(absolute_file_path):
        raise FileNotFoundError(f"File not found: {absolute_file_path}")
    
    try:
        with open(absolute_file_path, 'r') as file:
            return file.read()
    except Exception as e:
        raise Exception(f"Error reading file {absolute_file_path}: {e}")


def load_yaml(package_name, file_path):
    """Load yaml file"""
    package_path = get_package_share_directory(package_name)
    absolute_file_path = os.path.join(package_path, file_path)
    
    if not os.path.exists(absolute_file_path):
        raise FileNotFoundError(f"YAML file not found: {absolute_file_path}")
    
    try:
        with open(absolute_file_path, 'r') as file:
            return yaml.safe_load(file)
    except Exception as e:
        raise Exception(f"Error parsing YAML file {absolute_file_path}: {e}")


def generate_launch_description():
    # Set ROS_DOMAIN_ID
    set_domain_id = SetEnvironmentVariable('ROS_DOMAIN_ID', '9')

    # Launch arguments
    declare_use_sim_time = DeclareLaunchArgument(
        "use_sim_time", default_value="false"
    )

    # Package paths
    arm_description_pkg = "arm_description"
    moveit_config_pkg = "robotic_arm_moveit_config"

    # Load robot description
    robot_description_content = Command([
        FindExecutable(name="xacro"), " ",
        PathJoinSubstitution([
            FindPackageShare(arm_description_pkg),
            "urdf", "arm.urdf"
        ])
    ])

    robot_description = {"robot_description": robot_description_content}

    # Load SRDF
    robot_description_semantic_content = load_file(
        moveit_config_pkg, "config/robotic_arm.srdf"
    )
    robot_description_semantic = {
        "robot_description_semantic": robot_description_semantic_content
    }

    # Load kinematics
    kinematics_yaml = load_yaml(moveit_config_pkg, "config/kinematics.yaml")
    robot_description_kinematics = {"robot_description_kinematics": kinematics_yaml}

    # Load controllers config
    controllers_yaml = load_yaml(moveit_config_pkg, "config/ros2_controllers.yaml")

    # Planning parameters
    ompl_planning_pipeline_config = {
        "move_group": {
            "planning_plugin": "ompl_interface/OMPLPlanner",
            "request_adapters": """default_planner_request_adapters/AddTimeOptimalParameterization default_planner_request_adapters/ResolveConstraintFrames default_planner_request_adapters/FixWorkspaceBounds default_planner_request_adapters/FixStartStateBounds default_planner_request_adapters/FixStartStateCollision default_planner_request_adapters/FixStartStatePathConstraints""",
            "start_state_max_bounds_error": 0.1,
        }
    }

    ompl_planning_yaml = load_yaml(moveit_config_pkg, "config/ompl.yaml")
    ompl_planning_pipeline_config["move_group"].update(ompl_planning_yaml)

    # Planning scene monitor parameters
    planning_scene_monitor_parameters = {
        "publish_planning_scene": True,
        "publish_geometry_updates": True,
        "publish_state_updates": True,
        "publish_transforms_updates": True,
    }

    # Robot State Publisher
    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name="robot_state_publisher",
        output="screen",
        parameters=[
            robot_description,
            {"use_sim_time": LaunchConfiguration("use_sim_time")}
        ]
    )

    # ros2_control Node
    control_node = Node(
        package="controller_manager",
        executable="ros2_control_node",
        name="controller_manager",
        parameters=[
            robot_description,
            controllers_yaml,
            {"use_sim_time": LaunchConfiguration("use_sim_time")}
        ],
        output="screen",
        arguments=['--ros-args', '--log-level', 'info']
    )

    # Joint State Broadcaster Spawner
    joint_state_broadcaster_spawner = Node(
        package="controller_manager",
        executable="spawner",
        name="joint_state_broadcaster_spawner",
        arguments=["joint_state_broadcaster", "--controller-manager", "/controller_manager"],
        output="screen"
    )

    # Arm Controller Spawner
    arm_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        name="arm_controller_spawner",
        arguments=["arm", "--controller-manager", "/controller_manager"],
        output="screen"
    )

    # Gripper Controller Spawner
    gripper_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        name="gripper_controller_spawner",
        arguments=["gripper", "--controller-manager", "/controller_manager"],
        output="screen"
    )

    # MoveGroup Node
    move_group_node = Node(
        package="moveit_ros_move_group",
        executable="move_group",
        name="move_group",
        output="screen",
        parameters=[
            robot_description,
            robot_description_semantic,
            robot_description_kinematics,
            ompl_planning_pipeline_config,
            planning_scene_monitor_parameters,
            {"use_sim_time": LaunchConfiguration("use_sim_time")}
        ]
    )

    # RViz Node
    rviz_config_file = PathJoinSubstitution([
        FindPackageShare(moveit_config_pkg),
        "config", "moveit.rviz"
    ])

    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        arguments=["-d", rviz_config_file],
        parameters=[
            robot_description,
            robot_description_semantic,
            robot_description_kinematics,
            {"use_sim_time": LaunchConfiguration("use_sim_time")}
        ],
        output="screen"
    )

    # Event handlers for proper sequencing
    control_node_event_handler = RegisterEventHandler(
        OnProcessStart(
            target_action=robot_state_publisher_node,
            on_start=[
                TimerAction(
                    period=2.0,
                    actions=[control_node]
                )
            ]
        )
    )

    joint_state_broadcaster_event_handler = RegisterEventHandler(
        OnProcessStart(
            target_action=control_node,
            on_start=[
                TimerAction(
                    period=3.0,
                    actions=[joint_state_broadcaster_spawner]
                )
            ]
        )
    )

    controllers_event_handler = RegisterEventHandler(
        OnProcessStart(
            target_action=joint_state_broadcaster_spawner,
            on_start=[
                TimerAction(
                    period=1.0,
                    actions=[arm_controller_spawner, gripper_controller_spawner]
                )
            ]
        )
    )

    move_group_event_handler = RegisterEventHandler(
        OnProcessStart(
            target_action=arm_controller_spawner,
            on_start=[
                TimerAction(
                    period=2.0,
                    actions=[move_group_node]
                )
            ]
        )
    )

    rviz_event_handler = RegisterEventHandler(
        OnProcessStart(
            target_action=move_group_node,
            on_start=[
                TimerAction(
                    period=3.0,
                    actions=[rviz_node]
                )
            ]
        )
    )

    return LaunchDescription([
        set_domain_id,
        declare_use_sim_time,
        
        robot_state_publisher_node,
        
        control_node_event_handler,
        joint_state_broadcaster_event_handler,
        controllers_event_handler,
        move_group_event_handler,
        rviz_event_handler,
    ])