#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "moveit_planners_chomp::moveit_chomp_interface" for configuration "Release"
set_property(TARGET moveit_planners_chomp::moveit_chomp_interface APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(moveit_planners_chomp::moveit_chomp_interface PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libmoveit_chomp_interface.so.2.14.0"
  IMPORTED_SONAME_RELEASE "libmoveit_chomp_interface.so.2.14.0"
  )

list(APPEND _cmake_import_check_targets moveit_planners_chomp::moveit_chomp_interface )
list(APPEND _cmake_import_check_files_for_moveit_planners_chomp::moveit_chomp_interface "${_IMPORT_PREFIX}/lib/libmoveit_chomp_interface.so.2.14.0" )

# Import target "moveit_planners_chomp::moveit_chomp_planner_plugin" for configuration "Release"
set_property(TARGET moveit_planners_chomp::moveit_chomp_planner_plugin APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(moveit_planners_chomp::moveit_chomp_planner_plugin PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libmoveit_chomp_planner_plugin.so"
  IMPORTED_SONAME_RELEASE "libmoveit_chomp_planner_plugin.so"
  )

list(APPEND _cmake_import_check_targets moveit_planners_chomp::moveit_chomp_planner_plugin )
list(APPEND _cmake_import_check_files_for_moveit_planners_chomp::moveit_chomp_planner_plugin "${_IMPORT_PREFIX}/lib/libmoveit_chomp_planner_plugin.so" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
