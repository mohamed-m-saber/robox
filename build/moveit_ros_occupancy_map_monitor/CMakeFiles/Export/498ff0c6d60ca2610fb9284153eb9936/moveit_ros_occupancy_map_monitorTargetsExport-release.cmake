#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "moveit_ros_occupancy_map_monitor::moveit_ros_occupancy_map_monitor" for configuration "Release"
set_property(TARGET moveit_ros_occupancy_map_monitor::moveit_ros_occupancy_map_monitor APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(moveit_ros_occupancy_map_monitor::moveit_ros_occupancy_map_monitor PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libmoveit_ros_occupancy_map_monitor.so.2.14.0"
  IMPORTED_SONAME_RELEASE "libmoveit_ros_occupancy_map_monitor.so.2.14.0"
  )

list(APPEND _cmake_import_check_targets moveit_ros_occupancy_map_monitor::moveit_ros_occupancy_map_monitor )
list(APPEND _cmake_import_check_files_for_moveit_ros_occupancy_map_monitor::moveit_ros_occupancy_map_monitor "${_IMPORT_PREFIX}/lib/libmoveit_ros_occupancy_map_monitor.so.2.14.0" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
