# Install script for directory: /home/saber/robox_ws/src/moveit2/moveit_ros/occupancy_map_monitor

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/home/saber/robox_ws/install/moveit_ros_occupancy_map_monitor")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "Release")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

# Set default install directory permissions.
if(NOT DEFINED CMAKE_OBJDUMP)
  set(CMAKE_OBJDUMP "/usr/bin/objdump")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libmoveit_ros_occupancy_map_monitor.so.2.14.0" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libmoveit_ros_occupancy_map_monitor.so.2.14.0")
    file(RPATH_CHECK
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libmoveit_ros_occupancy_map_monitor.so.2.14.0"
         RPATH "")
  endif()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE SHARED_LIBRARY FILES "/home/saber/robox_ws/build/moveit_ros_occupancy_map_monitor/libmoveit_ros_occupancy_map_monitor.so.2.14.0")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libmoveit_ros_occupancy_map_monitor.so.2.14.0" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libmoveit_ros_occupancy_map_monitor.so.2.14.0")
    file(RPATH_CHANGE
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libmoveit_ros_occupancy_map_monitor.so.2.14.0"
         OLD_RPATH "/home/saber/robox_ws/install/moveit_core/lib:/home/saber/ws_moveit/install/moveit_msgs/lib:/opt/ros/jazzy/lib:/opt/ros/jazzy/lib/x86_64-linux-gnu:"
         NEW_RPATH "")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/usr/bin/strip" "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libmoveit_ros_occupancy_map_monitor.so.2.14.0")
    endif()
  endif()
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE SHARED_LIBRARY FILES "/home/saber/robox_ws/build/moveit_ros_occupancy_map_monitor/libmoveit_ros_occupancy_map_monitor.so")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/moveit_ros_occupancy_map_monitor/moveit_ros_occupancy_map_server" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/moveit_ros_occupancy_map_monitor/moveit_ros_occupancy_map_server")
    file(RPATH_CHECK
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/moveit_ros_occupancy_map_monitor/moveit_ros_occupancy_map_server"
         RPATH "")
  endif()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/moveit_ros_occupancy_map_monitor" TYPE EXECUTABLE FILES "/home/saber/robox_ws/build/moveit_ros_occupancy_map_monitor/moveit_ros_occupancy_map_server")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/moveit_ros_occupancy_map_monitor/moveit_ros_occupancy_map_server" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/moveit_ros_occupancy_map_monitor/moveit_ros_occupancy_map_server")
    file(RPATH_CHANGE
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/moveit_ros_occupancy_map_monitor/moveit_ros_occupancy_map_server"
         OLD_RPATH "/home/saber/robox_ws/build/moveit_ros_occupancy_map_monitor:/home/saber/robox_ws/install/moveit_core/lib:/home/saber/ws_moveit/install/moveit_msgs/lib:/opt/ros/jazzy/lib:/opt/ros/jazzy/lib/x86_64-linux-gnu:"
         NEW_RPATH "")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/usr/bin/strip" "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/moveit_ros_occupancy_map_monitor/moveit_ros_occupancy_map_server")
    endif()
  endif()
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  include("/home/saber/robox_ws/build/moveit_ros_occupancy_map_monitor/CMakeFiles/moveit_ros_occupancy_map_server.dir/install-cxx-module-bmi-Release.cmake" OPTIONAL)
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/moveit_ros_occupancy_map_monitor" TYPE DIRECTORY FILES "/home/saber/robox_ws/src/moveit2/moveit_ros/occupancy_map_monitor/include/")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/moveit_ros_occupancy_map_monitor/environment" TYPE FILE FILES "/opt/ros/jazzy/lib/python3.12/site-packages/ament_package/template/environment_hook/library_path.sh")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/moveit_ros_occupancy_map_monitor/environment" TYPE FILE FILES "/home/saber/robox_ws/build/moveit_ros_occupancy_map_monitor/ament_cmake_environment_hooks/library_path.dsv")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/home/saber/robox_ws/build/moveit_ros_occupancy_map_monitor/gmock/cmake_install.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/home/saber/robox_ws/build/moveit_ros_occupancy_map_monitor/gtest/cmake_install.cmake")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/ament_index/resource_index/package_run_dependencies" TYPE FILE FILES "/home/saber/robox_ws/build/moveit_ros_occupancy_map_monitor/ament_cmake_index/share/ament_index/resource_index/package_run_dependencies/moveit_ros_occupancy_map_monitor")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/ament_index/resource_index/parent_prefix_path" TYPE FILE FILES "/home/saber/robox_ws/build/moveit_ros_occupancy_map_monitor/ament_cmake_index/share/ament_index/resource_index/parent_prefix_path/moveit_ros_occupancy_map_monitor")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/moveit_ros_occupancy_map_monitor/environment" TYPE FILE FILES "/opt/ros/jazzy/share/ament_cmake_core/cmake/environment_hooks/environment/ament_prefix_path.sh")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/moveit_ros_occupancy_map_monitor/environment" TYPE FILE FILES "/home/saber/robox_ws/build/moveit_ros_occupancy_map_monitor/ament_cmake_environment_hooks/ament_prefix_path.dsv")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/moveit_ros_occupancy_map_monitor/environment" TYPE FILE FILES "/opt/ros/jazzy/share/ament_cmake_core/cmake/environment_hooks/environment/path.sh")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/moveit_ros_occupancy_map_monitor/environment" TYPE FILE FILES "/home/saber/robox_ws/build/moveit_ros_occupancy_map_monitor/ament_cmake_environment_hooks/path.dsv")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/moveit_ros_occupancy_map_monitor" TYPE FILE FILES "/home/saber/robox_ws/build/moveit_ros_occupancy_map_monitor/ament_cmake_environment_hooks/local_setup.bash")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/moveit_ros_occupancy_map_monitor" TYPE FILE FILES "/home/saber/robox_ws/build/moveit_ros_occupancy_map_monitor/ament_cmake_environment_hooks/local_setup.sh")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/moveit_ros_occupancy_map_monitor" TYPE FILE FILES "/home/saber/robox_ws/build/moveit_ros_occupancy_map_monitor/ament_cmake_environment_hooks/local_setup.zsh")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/moveit_ros_occupancy_map_monitor" TYPE FILE FILES "/home/saber/robox_ws/build/moveit_ros_occupancy_map_monitor/ament_cmake_environment_hooks/local_setup.dsv")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/moveit_ros_occupancy_map_monitor" TYPE FILE FILES "/home/saber/robox_ws/build/moveit_ros_occupancy_map_monitor/ament_cmake_environment_hooks/package.dsv")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/ament_index/resource_index/packages" TYPE FILE FILES "/home/saber/robox_ws/build/moveit_ros_occupancy_map_monitor/ament_cmake_index/share/ament_index/resource_index/packages/moveit_ros_occupancy_map_monitor")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/share/moveit_ros_occupancy_map_monitor/cmake/moveit_ros_occupancy_map_monitorTargetsExport.cmake")
    file(DIFFERENT _cmake_export_file_changed FILES
         "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/share/moveit_ros_occupancy_map_monitor/cmake/moveit_ros_occupancy_map_monitorTargetsExport.cmake"
         "/home/saber/robox_ws/build/moveit_ros_occupancy_map_monitor/CMakeFiles/Export/498ff0c6d60ca2610fb9284153eb9936/moveit_ros_occupancy_map_monitorTargetsExport.cmake")
    if(_cmake_export_file_changed)
      file(GLOB _cmake_old_config_files "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/share/moveit_ros_occupancy_map_monitor/cmake/moveit_ros_occupancy_map_monitorTargetsExport-*.cmake")
      if(_cmake_old_config_files)
        string(REPLACE ";" ", " _cmake_old_config_files_text "${_cmake_old_config_files}")
        message(STATUS "Old export file \"$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/share/moveit_ros_occupancy_map_monitor/cmake/moveit_ros_occupancy_map_monitorTargetsExport.cmake\" will be replaced.  Removing files [${_cmake_old_config_files_text}].")
        unset(_cmake_old_config_files_text)
        file(REMOVE ${_cmake_old_config_files})
      endif()
      unset(_cmake_old_config_files)
    endif()
    unset(_cmake_export_file_changed)
  endif()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/moveit_ros_occupancy_map_monitor/cmake" TYPE FILE FILES "/home/saber/robox_ws/build/moveit_ros_occupancy_map_monitor/CMakeFiles/Export/498ff0c6d60ca2610fb9284153eb9936/moveit_ros_occupancy_map_monitorTargetsExport.cmake")
  if(CMAKE_INSTALL_CONFIG_NAME MATCHES "^([Rr][Ee][Ll][Ee][Aa][Ss][Ee])$")
    file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/moveit_ros_occupancy_map_monitor/cmake" TYPE FILE FILES "/home/saber/robox_ws/build/moveit_ros_occupancy_map_monitor/CMakeFiles/Export/498ff0c6d60ca2610fb9284153eb9936/moveit_ros_occupancy_map_monitorTargetsExport-release.cmake")
  endif()
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/moveit_ros_occupancy_map_monitor/cmake" TYPE FILE FILES "/home/saber/robox_ws/build/moveit_ros_occupancy_map_monitor/ament_cmake_export_targets/ament_cmake_export_targets-extras.cmake")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/moveit_ros_occupancy_map_monitor/cmake" TYPE FILE FILES "/home/saber/robox_ws/build/moveit_ros_occupancy_map_monitor/ament_cmake_export_dependencies/ament_cmake_export_dependencies-extras.cmake")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/moveit_ros_occupancy_map_monitor/cmake" TYPE FILE FILES
    "/home/saber/robox_ws/build/moveit_ros_occupancy_map_monitor/ament_cmake_core/moveit_ros_occupancy_map_monitorConfig.cmake"
    "/home/saber/robox_ws/build/moveit_ros_occupancy_map_monitor/ament_cmake_core/moveit_ros_occupancy_map_monitorConfig-version.cmake"
    )
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/moveit_ros_occupancy_map_monitor" TYPE FILE FILES "/home/saber/robox_ws/src/moveit2/moveit_ros/occupancy_map_monitor/package.xml")
endif()

if(CMAKE_INSTALL_COMPONENT)
  set(CMAKE_INSTALL_MANIFEST "install_manifest_${CMAKE_INSTALL_COMPONENT}.txt")
else()
  set(CMAKE_INSTALL_MANIFEST "install_manifest.txt")
endif()

string(REPLACE ";" "\n" CMAKE_INSTALL_MANIFEST_CONTENT
       "${CMAKE_INSTALL_MANIFEST_FILES}")
file(WRITE "/home/saber/robox_ws/build/moveit_ros_occupancy_map_monitor/${CMAKE_INSTALL_MANIFEST}"
     "${CMAKE_INSTALL_MANIFEST_CONTENT}")
