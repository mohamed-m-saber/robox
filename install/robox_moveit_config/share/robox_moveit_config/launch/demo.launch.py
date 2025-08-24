from launch import LaunchDescription
from launch.actions import SetEnvironmentVariable
from launch_ros.actions import Node
from moveit_configs_utils import MoveItConfigsBuilder
from launch.substitutions import PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    # Set ROS_DOMAIN_ID for DDS isolation
    set_domain_id = SetEnvironmentVariable('ROS_DOMAIN_ID', '12')

    # MoveIt config using MoveItConfigsBuilder
    moveit_config = (
        MoveItConfigsBuilder("robox_arm", package_name="robox_moveit_config")
        .robot_description(file_path="config/robox_arm.urdf.xacro")
        .robot_description_semantic(file_path="config/robox_arm.srdf")
        .robot_description_kinematics(file_path="config/kinematics.yaml")
        .trajectory_execution(file_path="config/moveit_controllers.yaml")
        .planning_scene_monitor(
            publish_robot_description=True,
            publish_robot_description_semantic=True
        )
        .to_moveit_configs()
    )

    # Config paths
    controllers_yaml = PathJoinSubstitution([
        FindPackageShare("robox_moveit_config"),
        "config",
        "ros2_controllers.yaml"
    ])

    planning_params_yaml = PathJoinSubstitution([
        FindPackageShare("robox_moveit_config"),
        "config",
        "planning_parameters.yaml"
    ])

    rviz_config_file = PathJoinSubstitution([
        FindPackageShare("robox_moveit_config"),
        "config",
        "moveit.rviz"
    ])

    # Nodes
    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[moveit_config.robot_description],
        # output="screen"
    )

    control_node = Node(
        package="controller_manager",
        executable="ros2_control_node",
        parameters=[
            moveit_config.robot_description,
            controllers_yaml
        ],
        # output="screen"
    )

    joint_state_broadcaster_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_state_broadcaster"],
        # output="screen"
    )

    arm_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["arm_controller"],
        # output="screen"
    )

    move_group_node = Node(
        package="moveit_ros_move_group",
        executable="move_group",
        output="screen",
        parameters=[
            moveit_config.to_dict(),
            planning_params_yaml,
            {"moveit_controller_manager": "moveit_ros_control_interface/Ros2ControlManager"}
        ]
    )

    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        arguments=["-d", rviz_config_file],
        parameters=[
            moveit_config.robot_description,
            moveit_config.robot_description_semantic,
            moveit_config.robot_description_kinematics
        ],
        # output="screen"
    )

    # Launch description
    return LaunchDescription([
        set_domain_id,
        robot_state_publisher_node,
        control_node,
        joint_state_broadcaster_spawner,
        arm_controller_spawner,
        move_group_node,
        rviz_node
    ])
