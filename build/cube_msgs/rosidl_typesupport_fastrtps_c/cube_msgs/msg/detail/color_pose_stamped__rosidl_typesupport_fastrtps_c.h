// generated from rosidl_typesupport_fastrtps_c/resource/idl__rosidl_typesupport_fastrtps_c.h.em
// with input from cube_msgs:msg/ColorPoseStamped.idl
// generated code does not contain a copyright notice
#ifndef CUBE_MSGS__MSG__DETAIL__COLOR_POSE_STAMPED__ROSIDL_TYPESUPPORT_FASTRTPS_C_H_
#define CUBE_MSGS__MSG__DETAIL__COLOR_POSE_STAMPED__ROSIDL_TYPESUPPORT_FASTRTPS_C_H_


#include <stddef.h>
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_interface/macros.h"
#include "cube_msgs/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
#include "cube_msgs/msg/detail/color_pose_stamped__struct.h"
#include "fastcdr/Cdr.h"

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_cube_msgs
bool cdr_serialize_cube_msgs__msg__ColorPoseStamped(
  const cube_msgs__msg__ColorPoseStamped * ros_message,
  eprosima::fastcdr::Cdr & cdr);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_cube_msgs
bool cdr_deserialize_cube_msgs__msg__ColorPoseStamped(
  eprosima::fastcdr::Cdr &,
  cube_msgs__msg__ColorPoseStamped * ros_message);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_cube_msgs
size_t get_serialized_size_cube_msgs__msg__ColorPoseStamped(
  const void * untyped_ros_message,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_cube_msgs
size_t max_serialized_size_cube_msgs__msg__ColorPoseStamped(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_cube_msgs
bool cdr_serialize_key_cube_msgs__msg__ColorPoseStamped(
  const cube_msgs__msg__ColorPoseStamped * ros_message,
  eprosima::fastcdr::Cdr & cdr);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_cube_msgs
size_t get_serialized_size_key_cube_msgs__msg__ColorPoseStamped(
  const void * untyped_ros_message,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_cube_msgs
size_t max_serialized_size_key_cube_msgs__msg__ColorPoseStamped(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_cube_msgs
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, cube_msgs, msg, ColorPoseStamped)();

#ifdef __cplusplus
}
#endif

#endif  // CUBE_MSGS__MSG__DETAIL__COLOR_POSE_STAMPED__ROSIDL_TYPESUPPORT_FASTRTPS_C_H_
