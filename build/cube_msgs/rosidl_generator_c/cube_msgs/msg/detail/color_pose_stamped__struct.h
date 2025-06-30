// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from cube_msgs:msg/ColorPoseStamped.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "cube_msgs/msg/color_pose_stamped.h"


#ifndef CUBE_MSGS__MSG__DETAIL__COLOR_POSE_STAMPED__STRUCT_H_
#define CUBE_MSGS__MSG__DETAIL__COLOR_POSE_STAMPED__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

// Constants defined in the message

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__struct.h"
// Member 'pose'
#include "geometry_msgs/msg/detail/pose__struct.h"
// Member 'color'
#include "rosidl_runtime_c/string.h"

/// Struct defined in msg/ColorPoseStamped in the package cube_msgs.
typedef struct cube_msgs__msg__ColorPoseStamped
{
  std_msgs__msg__Header header;
  geometry_msgs__msg__Pose pose;
  rosidl_runtime_c__String color;
} cube_msgs__msg__ColorPoseStamped;

// Struct for a sequence of cube_msgs__msg__ColorPoseStamped.
typedef struct cube_msgs__msg__ColorPoseStamped__Sequence
{
  cube_msgs__msg__ColorPoseStamped * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} cube_msgs__msg__ColorPoseStamped__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // CUBE_MSGS__MSG__DETAIL__COLOR_POSE_STAMPED__STRUCT_H_
