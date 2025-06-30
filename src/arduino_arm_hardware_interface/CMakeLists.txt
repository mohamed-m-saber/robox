cmake_minimum_required(VERSION 3.8)
project(arduino_arm_hardware_interface)

# Dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(hardware_interface REQUIRED)
find_package(pluginlib REQUIRED)
find_package(PkgConfig REQUIRED)

pkg_check_modules(LIBSERIAL REQUIRED libserial)

# Include dirs
include_directories(
  include
  ${LIBSERIAL_INCLUDE_DIRS}
)

# Hardware interface plugin
add_library(arduino_arm_system SHARED
  src/arduino_arm_system.cpp
)

ament_target_dependencies(arduino_arm_system
  rclcpp
  hardware_interface
  pluginlib
)

target_link_libraries(arduino_arm_system
  ${LIBSERIAL_LIBRARIES}
)

# Export plugin
pluginlib_export_plugin_description_file(hardware_interface arduino_arm_system_plugin.xml)

install(
  DIRECTORY include/
  DESTINATION include/
)

install(
  TARGETS arduino_arm_system
  LIBRARY DESTINATION lib
)

ament_package()
