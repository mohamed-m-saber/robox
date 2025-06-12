from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, RegisterEventHandler
from launch.substitutions import LaunchConfiguration, Command
from launch.event_handlers import OnProcessStart
from moveit_configs_utils import MoveItConfigsBuilder
from ament_index_python.packages import get_package_share_directory
from launch_ros.actions import Node
import os

def generate_launch_description():
    # Declare launch arguments
    is_sim_arg = DeclareLaunchArgument(
        "is_sim", default_value="True", description="Run in simulation mode"
    )

    is_sim = LaunchConfiguration("is_sim")

    # Configure MoveIt
    moveit_config = (
        MoveItConfigsBuilder("robotic_arm", package_name="robotic_arm_moveit_config")
        .robot_description(
            file_path=os.path.join(
                get_package_share_directory("arm_description"), "urdf", "arm.urdf"
            )
        )
        .robot_description_semantic(file_path="config/robotic_arm.srdf")
        .trajectory_execution(file_path="config/moveit_controllers.yaml")
        .to_moveit_configs()
    )

    # Robot state publisher
    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[
            {
                "robot_description": Command(
                    [
                        "xacro ",
                        os.path.join(
                            get_package_share_directory("arm_description"),
                            "urdf",
                            "arm.urdf",
                        ),
                        " is_ignition:=False",
                    ]
                )
            },
            {"use_sim_time": is_sim},
        ],
        output="screen",
    )

    # Controller manager
    controller_manager = Node(
        package="controller_manager",
        executable="ros2_control_node",
        parameters=[
            moveit_config.robot_description,
            os.path.join(
                get_package_share_directory("robot_moveit_config"),
                "config",
                "ros2_controllers.yaml",
            ),
            {"use_sim_time": is_sim},
        ],
        output="screen",
    )

    # MoveIt move_group node
    move_group_node = Node(
        package="moveit_ros_move_group",
        executable="move_group",
        output="screen",
        parameters=[
            moveit_config.to_dict(),
            {"use_sim_time": is_sim},
            {"publish_robot_description_semantic": True},
        ],
        arguments=["--ros-args", "--log-level", "info"],
    )

    # RViz node
    rviz_config = os.path.join(
        get_package_share_directory("robot_moveit_config"), "config", "moveit.rviz"
    )
    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="screen",
        arguments=["-d", rviz_config],
        parameters=[
            moveit_config.robot_description,
            moveit_config.robot_description_semantic,
            moveit_config.robot_description_kinematics,
            moveit_config.joint_limits,
            {"use_sim_time": is_sim},
        ],
    )

    # Spawner nodes for controllers
    joint_state_broadcaster_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_state_broadcaster"],
        output="screen",
    )

    arm_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["arm"],
        output="screen",
    )

    gripper_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["gripper"],
        output="screen",
    )

    # Ensure spawners start after controller_manager
    spawner_event_handler = RegisterEventHandler(
        event_handler=OnProcessStart(
            target_action=controller_manager,
            on_start=[
                joint_state_broadcaster_spawner,
                arm_controller_spawner,
                gripper_controller_spawner,
            ],
        )
    )

    return LaunchDescription([
        is_sim_arg,
        robot_state_publisher,
        controller_manager,
        spawner_event_handler,
        move_group_node,
        rviz_node,
    ])