# cmake_minimum_required(VERSION 3.8)
# project(arm_description)

# if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
#   add_compile_options(-Wall -Wextra -Wpedantic)
# endif()

# set(CMAKE_VERBOSE_MAKEFILE ON)

# # Dependencies
# find_package(ament_cmake REQUIRED)
# find_package(rclcpp REQUIRED)
# find_package(geometry_msgs REQUIRED)
# find_package(moveit_ros_planning_interface REQUIRED)
# find_package(moveit_msgs REQUIRED)
# find_package(moveit_core REQUIRED)
# find_package(rclcpp_action REQUIRED)
# find_package(controller_manager_msgs REQUIRED)
# find_package(tf2 REQUIRED)
# find_package(tf2_ros REQUIRED)
# find_package(tf2_geometry_msgs REQUIRED)

# # Create executable

# # Include directories
# # target_include_directories(robot_arm_ik_node PUBLIC
# #   $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
# #   $<INSTALL_INTERFACE:include>
# # )

# # Link dependencies
# ament_target_dependencies(robot_arm_ik_node
#   rclcpp
#   geometry_msgs
#   moveit_ros_planning_interface
#   moveit_msgs
#   moveit_core
#   rclcpp_action
#   controller_manager_msgs
#   tf2
#   tf2_ros
#   tf2_geometry_msgs
# )

# # Install executable
# # install(TARGETS robot_arm_ik_node
# #   DESTINATION lib/${PROJECT_NAME}
# # )

# # Install data files
# install(DIRECTORY meshes urdf launch rviz
#   DESTINATION share/${PROJECT_NAME}
# )

# if(BUILD_TESTING)
#   find_package(ament_lint_auto REQUIRED)
#   set(ament_cmake_copyright_FOUND TRUE)
#   set(ament_cmake_cpplint_FOUND TRUE)
#   ament_lint_auto_find_test_dependencies()
# endif()

# ament_package()



cmake_minimum_required(VERSION 3.8)
project(arm_description)

find_package(ament_cmake REQUIRED)

# Install robot description files
install(DIRECTORY meshes urdf launch rviz
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
