#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "moveit_simple_controller_manager::moveit_simple_controller_manager" for configuration "Release"
set_property(TARGET moveit_simple_controller_manager::moveit_simple_controller_manager APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(moveit_simple_controller_manager::moveit_simple_controller_manager PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libmoveit_simple_controller_manager.so.2.14.0"
  IMPORTED_SONAME_RELEASE "libmoveit_simple_controller_manager.so.2.14.0"
  )

list(APPEND _cmake_import_check_targets moveit_simple_controller_manager::moveit_simple_controller_manager )
list(APPEND _cmake_import_check_files_for_moveit_simple_controller_manager::moveit_simple_controller_manager "${_IMPORT_PREFIX}/lib/libmoveit_simple_controller_manager.so.2.14.0" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
