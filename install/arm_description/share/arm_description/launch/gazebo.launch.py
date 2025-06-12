from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument, SetEnvironmentVariable, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, LaunchConfiguration
from ament_index_python.packages import get_package_share_directory
import os
from pathlib import Path
from launch_ros.parameter_descriptions import ParameterValue

def generate_launch_description():
    arm_description_dir = get_package_share_directory("arm_description")

    model_arg = DeclareLaunchArgument(
        name="model",
        default_value=os.path.join(arm_description_dir, "urdf", "arm.urdf"),
        description="Absolute path to robot urdf file"
    )

    model_path = LaunchConfiguration("model", default=os.path.join(arm_description_dir, "urdf", "arm.urdf"))

    gazebo_resource_path = SetEnvironmentVariable(
        name='GZ_SIM_RESOURCE_PATH',
        value=[str(Path(arm_description_dir).parent.resolve())]
    )

    ros_distro = os.environ.get("ROS_DISTRO", "unknown")
    is_ignition = "True" if ros_distro == "humble" else "False"
    print(f"ROS_DISTRO: {ros_distro}")
    print(f"is_ignition: {is_ignition}")
    print(f"Model path: {os.path.join(arm_description_dir, 'urdf', 'arm.urdf')}")

    robot_description = ParameterValue(
    Command([
        "xacro",
        " ",  # <-- space separator
        LaunchConfiguration("model"),
        " ",  # <-- space separator
        "is_ignition:=",
        is_ignition
    ]),
    value_type=str
)

    physics_engine = "" if ros_distro == "humble" else "--physics-engine gz-physics-bullet-featherstone-plugin"

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [os.path.join(get_package_share_directory("ros_gz_sim"), "launch"), "/gz_sim.launch.py"]
        ),
        launch_arguments=[("gz_args", f"-v 4 -r empty.sdf {physics_engine}")]
    )

    gazebo_spawn_entity = Node(
        package="ros_gz_sim",
        executable="create",
        output="screen",
        arguments=["-topic", "robot_description", "-name", "arm_description"]
    )

    gz_ros2_bridge = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        arguments=["/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock]"]
    )

    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[{"robot_description": robot_description, "use_sim_time": True}]
    )

    joint_state_publisher_gui = Node(
        package="joint_state_publisher_gui",
        executable="joint_state_publisher_gui"
    )

    return LaunchDescription([
        model_arg,
        gazebo_resource_path,
        robot_state_publisher,
        gazebo,
        gazebo_spawn_entity,
        gz_ros2_bridge,
        joint_state_publisher_gui
    ])
