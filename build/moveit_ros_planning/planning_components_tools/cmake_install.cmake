# Install script for directory: /home/saber/robox_ws/src/moveit2/moveit_ros/planning/planning_components_tools

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/home/saber/robox_ws/install/moveit_ros_planning")
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
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/moveit_ros_planning/moveit_print_planning_model_info" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/moveit_ros_planning/moveit_print_planning_model_info")
    file(RPATH_CHECK
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/moveit_ros_planning/moveit_print_planning_model_info"
         RPATH "")
  endif()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/moveit_ros_planning" TYPE EXECUTABLE FILES "/home/saber/robox_ws/build/moveit_ros_planning/planning_components_tools/moveit_print_planning_model_info")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/moveit_ros_planning/moveit_print_planning_model_info" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/moveit_ros_planning/moveit_print_planning_model_info")
    file(RPATH_CHANGE
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/moveit_ros_planning/moveit_print_planning_model_info"
         OLD_RPATH "/home/saber/robox_ws/build/moveit_ros_planning/robot_model_loader:/home/saber/robox_ws/build/moveit_ros_planning/kinematics_plugin_loader:/home/saber/robox_ws/build/moveit_ros_planning/rdf_loader:/home/saber/robox_ws/install/moveit_core/lib:/home/saber/ws_moveit/install/moveit_msgs/lib:/opt/ros/jazzy/lib:/opt/ros/jazzy/lib/x86_64-linux-gnu:"
         NEW_RPATH "")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/usr/bin/strip" "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/moveit_ros_planning/moveit_print_planning_model_info")
    endif()
  endif()
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/moveit_ros_planning/moveit_print_planning_scene_info" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/moveit_ros_planning/moveit_print_planning_scene_info")
    file(RPATH_CHECK
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/moveit_ros_planning/moveit_print_planning_scene_info"
         RPATH "")
  endif()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/moveit_ros_planning" TYPE EXECUTABLE FILES "/home/saber/robox_ws/build/moveit_ros_planning/planning_components_tools/moveit_print_planning_scene_info")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/moveit_ros_planning/moveit_print_planning_scene_info" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/moveit_ros_planning/moveit_print_planning_scene_info")
    file(RPATH_CHANGE
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/moveit_ros_planning/moveit_print_planning_scene_info"
         OLD_RPATH "/home/saber/robox_ws/build/moveit_ros_planning/planning_scene_monitor:/home/saber/robox_ws/install/moveit_ros_occupancy_map_monitor/lib:/home/saber/robox_ws/build/moveit_ros_planning/robot_model_loader:/home/saber/robox_ws/build/moveit_ros_planning/kinematics_plugin_loader:/home/saber/robox_ws/build/moveit_ros_planning/rdf_loader:/home/saber/robox_ws/install/moveit_core/lib:/home/saber/ws_moveit/install/moveit_msgs/lib:/opt/ros/jazzy/lib:/home/saber/robox_ws/build/moveit_ros_planning/collision_plugin_loader:/opt/ros/jazzy/lib/x86_64-linux-gnu:"
         NEW_RPATH "")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/usr/bin/strip" "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/moveit_ros_planning/moveit_print_planning_scene_info")
    endif()
  endif()
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/moveit_ros_planning/moveit_display_random_state" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/moveit_ros_planning/moveit_display_random_state")
    file(RPATH_CHECK
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/moveit_ros_planning/moveit_display_random_state"
         RPATH "")
  endif()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/moveit_ros_planning" TYPE EXECUTABLE FILES "/home/saber/robox_ws/build/moveit_ros_planning/planning_components_tools/moveit_display_random_state")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/moveit_ros_planning/moveit_display_random_state" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/moveit_ros_planning/moveit_display_random_state")
    file(RPATH_CHANGE
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/moveit_ros_planning/moveit_display_random_state"
         OLD_RPATH "/home/saber/robox_ws/build/moveit_ros_planning/planning_scene_monitor:/home/saber/robox_ws/install/moveit_ros_occupancy_map_monitor/lib:/home/saber/robox_ws/build/moveit_ros_planning/robot_model_loader:/home/saber/robox_ws/build/moveit_ros_planning/kinematics_plugin_loader:/home/saber/robox_ws/build/moveit_ros_planning/rdf_loader:/home/saber/robox_ws/install/moveit_core/lib:/home/saber/ws_moveit/install/moveit_msgs/lib:/opt/ros/jazzy/lib:/home/saber/robox_ws/build/moveit_ros_planning/collision_plugin_loader:/opt/ros/jazzy/lib/x86_64-linux-gnu:"
         NEW_RPATH "")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/usr/bin/strip" "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/moveit_ros_planning/moveit_display_random_state")
    endif()
  endif()
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/moveit_ros_planning/moveit_visualize_robot_collision_volume" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/moveit_ros_planning/moveit_visualize_robot_collision_volume")
    file(RPATH_CHECK
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/moveit_ros_planning/moveit_visualize_robot_collision_volume"
         RPATH "")
  endif()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/moveit_ros_planning" TYPE EXECUTABLE FILES "/home/saber/robox_ws/build/moveit_ros_planning/planning_components_tools/moveit_visualize_robot_collision_volume")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/moveit_ros_planning/moveit_visualize_robot_collision_volume" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/moveit_ros_planning/moveit_visualize_robot_collision_volume")
    file(RPATH_CHANGE
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/moveit_ros_planning/moveit_visualize_robot_collision_volume"
         OLD_RPATH "/home/saber/robox_ws/build/moveit_ros_planning/planning_scene_monitor:/home/saber/robox_ws/install/moveit_core/lib:/home/saber/ws_moveit/install/moveit_msgs/lib:/opt/ros/jazzy/lib:/home/saber/robox_ws/install/moveit_ros_occupancy_map_monitor/lib:/home/saber/robox_ws/build/moveit_ros_planning/robot_model_loader:/home/saber/robox_ws/build/moveit_ros_planning/kinematics_plugin_loader:/home/saber/robox_ws/build/moveit_ros_planning/rdf_loader:/home/saber/robox_ws/build/moveit_ros_planning/collision_plugin_loader:/opt/ros/jazzy/lib/x86_64-linux-gnu:"
         NEW_RPATH "")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/usr/bin/strip" "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/moveit_ros_planning/moveit_visualize_robot_collision_volume")
    endif()
  endif()
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/moveit_ros_planning/moveit_evaluate_collision_checking_speed" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/moveit_ros_planning/moveit_evaluate_collision_checking_speed")
    file(RPATH_CHECK
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/moveit_ros_planning/moveit_evaluate_collision_checking_speed"
         RPATH "")
  endif()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/moveit_ros_planning" TYPE EXECUTABLE FILES "/home/saber/robox_ws/build/moveit_ros_planning/planning_components_tools/moveit_evaluate_collision_checking_speed")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/moveit_ros_planning/moveit_evaluate_collision_checking_speed" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/moveit_ros_planning/moveit_evaluate_collision_checking_speed")
    file(RPATH_CHANGE
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/moveit_ros_planning/moveit_evaluate_collision_checking_speed"
         OLD_RPATH "/home/saber/robox_ws/build/moveit_ros_planning/planning_scene_monitor:/home/saber/robox_ws/install/moveit_ros_occupancy_map_monitor/lib:/home/saber/robox_ws/build/moveit_ros_planning/robot_model_loader:/home/saber/robox_ws/build/moveit_ros_planning/kinematics_plugin_loader:/home/saber/robox_ws/build/moveit_ros_planning/rdf_loader:/home/saber/robox_ws/install/moveit_core/lib:/home/saber/ws_moveit/install/moveit_msgs/lib:/opt/ros/jazzy/lib:/home/saber/robox_ws/build/moveit_ros_planning/collision_plugin_loader:/opt/ros/jazzy/lib/x86_64-linux-gnu:"
         NEW_RPATH "")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/usr/bin/strip" "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/moveit_ros_planning/moveit_evaluate_collision_checking_speed")
    endif()
  endif()
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/moveit_ros_planning/moveit_publish_scene_from_text" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/moveit_ros_planning/moveit_publish_scene_from_text")
    file(RPATH_CHECK
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/moveit_ros_planning/moveit_publish_scene_from_text"
         RPATH "")
  endif()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/moveit_ros_planning" TYPE EXECUTABLE FILES "/home/saber/robox_ws/build/moveit_ros_planning/planning_components_tools/moveit_publish_scene_from_text")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/moveit_ros_planning/moveit_publish_scene_from_text" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/moveit_ros_planning/moveit_publish_scene_from_text")
    file(RPATH_CHANGE
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/moveit_ros_planning/moveit_publish_scene_from_text"
         OLD_RPATH "/home/saber/robox_ws/build/moveit_ros_planning/planning_scene_monitor:/home/saber/robox_ws/build/moveit_ros_planning/robot_model_loader:/home/saber/robox_ws/build/moveit_ros_planning/kinematics_plugin_loader:/home/saber/robox_ws/build/moveit_ros_planning/rdf_loader:/home/saber/robox_ws/install/moveit_core/lib:/home/saber/ws_moveit/install/moveit_msgs/lib:/opt/ros/jazzy/lib:/home/saber/robox_ws/install/moveit_ros_occupancy_map_monitor/lib:/home/saber/robox_ws/build/moveit_ros_planning/collision_plugin_loader:/opt/ros/jazzy/lib/x86_64-linux-gnu:"
         NEW_RPATH "")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/usr/bin/strip" "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/moveit_ros_planning/moveit_publish_scene_from_text")
    endif()
  endif()
endif()

