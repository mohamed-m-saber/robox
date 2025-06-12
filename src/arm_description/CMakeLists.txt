cmake_minimum_required(VERSION 3.8)
project(arm_description)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# Enable verbose makefile for debugging
set(CMAKE_VERBOSE_MAKEFILE ON)

# Find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(moveit_ros_planning_interface REQUIRED)
find_package(moveit_msgs REQUIRED)
find_package(moveit_core REQUIRED)
find_package(rclcpp_action REQUIRED)
find_package(controller_manager_msgs REQUIRED)
find_package(rosidl_default_generators REQUIRED)
find_package(tf2 REQUIRED)
find_package(tf2_ros REQUIRED)
find_package(tf2_geometry_msgs REQUIRED)

# Generate interfaces
rosidl_generate_interfaces(${PROJECT_NAME}
  "srv/GoToPose.srv"
  DEPENDENCIES geometry_msgs
)

# Get the generated interface target
rosidl_get_typesupport_target(cpp_typesupport_target
  ${PROJECT_NAME} "rosidl_typesupport_cpp")

# Declare the executable
add_executable(robot_arm_ik_node src/pose.cpp)

# Specify include directories for TF2 and others
target_include_directories(robot_arm_ik_node PUBLIC
  ${tf2_INCLUDE_DIRS}
  ${tf2_ros_INCLUDE_DIRS}
  ${tf2_geometry_msgs_INCLUDE_DIRS}
)

# Add dependencies
ament_target_dependencies(robot_arm_ik_node
  rclcpp
  geometry_msgs
  moveit_ros_planning_interface
  moveit_msgs
  moveit_core
  rclcpp_action
  controller_manager_msgs
  tf2
  tf2_ros
  tf2_geometry_msgs
)

# Link the generated interfaces and TF2 libraries
target_link_libraries(robot_arm_ik_node
  ${cpp_typesupport_target}
  ${tf2_LIBRARIES}
  ${tf2_ros_LIBRARIES}
  ${tf2_geometry_msgs_LIBRARIES}
)

# Ensure the executable depends on the interface generation
add_dependencies(robot_arm_ik_node ${PROJECT_NAME})

# Install the executable
install(TARGETS robot_arm_ik_node
  DESTINATION lib/${PROJECT_NAME}
)

# Install other package resources
install(
  DIRECTORY meshes urdf launch rviz srv
  DESTINATION share/${PROJECT_NAME}
)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  set(ament_cmake_copyright_FOUND TRUE)
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()