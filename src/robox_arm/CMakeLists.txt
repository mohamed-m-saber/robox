cmake_minimum_required(VERSION 3.8)
project(robox_arm)

find_package(ament_cmake REQUIRED)

# Install robot description files
install(DIRECTORY meshes urdf launch rviz
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
