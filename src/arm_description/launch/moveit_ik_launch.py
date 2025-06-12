#!/usr/bin/env python3

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
import os
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    
    # Declare launch arguments
    use_sim_time = LaunchConfiguration('use_sim_time', default='false')
    
    # Package directories
    arm_description_dir = get_package_share_directory('arm_description')
    moveit_config_dir = get_package_share_directory('robotic_arm_moveit_config')
    
    return LaunchDescription([
        
        # Launch Arguments
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='false',
            description='Use simulation time'
        ),
        
        # Launch MoveIt with RViz
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([
                PathJoinSubstitution([
                    FindPackageShare('robotic_arm_moveit_config'),
                    'launch',
                    'demo.launch.py'
                ])
            ]),
            launch_arguments={
                'use_sim_time': use_sim_time
            }.items()
        ),
        
        # Launch the GoToPose service node
        Node(
            package='arm_description',
            executable='robot_arm_ik_node',
            name='go_to_pose_service_node',
            output='screen',
            parameters=[{'use_sim_time': use_sim_time}],
            emulate_tty=True,
        ),
        
        # Launch the interactive client (optional - uncomment if you want it to start automatically)
        # Node(
        #     package='arm_description',
        #     executable='interactive_pose_client.py',
        #     name='interactive_pose_client',
        #     output='screen',
        #     parameters=[{'use_sim_time': use_sim_time}],
        #     emulate_tty=True,
        # ),
        
        # Launch a pose publisher node for RViz interaction
        Node(
            package='arm_description',
            executable='rviz_pose_publisher.py',
            name='rviz_pose_publisher',
            output='screen',
            parameters=[{'use_sim_time': use_sim_time}],
            emulate_tty=True,
        ),
        
    ])