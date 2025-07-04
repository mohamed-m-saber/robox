// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from cube_msgs:msg/ColorPoseStamped.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "cube_msgs/msg/detail/color_pose_stamped__rosidl_typesupport_introspection_c.h"
#include "cube_msgs/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "cube_msgs/msg/detail/color_pose_stamped__functions.h"
#include "cube_msgs/msg/detail/color_pose_stamped__struct.h"


// Include directives for member types
// Member `header`
#include "std_msgs/msg/header.h"
// Member `header`
#include "std_msgs/msg/detail/header__rosidl_typesupport_introspection_c.h"
// Member `pose`
#include "geometry_msgs/msg/pose.h"
// Member `pose`
#include "geometry_msgs/msg/detail/pose__rosidl_typesupport_introspection_c.h"
// Member `color`
#include "rosidl_runtime_c/string_functions.h"

#ifdef __cplusplus
extern "C"
{
#endif

void cube_msgs__msg__ColorPoseStamped__rosidl_typesupport_introspection_c__ColorPoseStamped_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  cube_msgs__msg__ColorPoseStamped__init(message_memory);
}

void cube_msgs__msg__ColorPoseStamped__rosidl_typesupport_introspection_c__ColorPoseStamped_fini_function(void * message_memory)
{
  cube_msgs__msg__ColorPoseStamped__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember cube_msgs__msg__ColorPoseStamped__rosidl_typesupport_introspection_c__ColorPoseStamped_message_member_array[3] = {
  {
    "header",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(cube_msgs__msg__ColorPoseStamped, header),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "pose",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(cube_msgs__msg__ColorPoseStamped, pose),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "color",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(cube_msgs__msg__ColorPoseStamped, color),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers cube_msgs__msg__ColorPoseStamped__rosidl_typesupport_introspection_c__ColorPoseStamped_message_members = {
  "cube_msgs__msg",  // message namespace
  "ColorPoseStamped",  // message name
  3,  // number of fields
  sizeof(cube_msgs__msg__ColorPoseStamped),
  false,  // has_any_key_member_
  cube_msgs__msg__ColorPoseStamped__rosidl_typesupport_introspection_c__ColorPoseStamped_message_member_array,  // message members
  cube_msgs__msg__ColorPoseStamped__rosidl_typesupport_introspection_c__ColorPoseStamped_init_function,  // function to initialize message memory (memory has to be allocated)
  cube_msgs__msg__ColorPoseStamped__rosidl_typesupport_introspection_c__ColorPoseStamped_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t cube_msgs__msg__ColorPoseStamped__rosidl_typesupport_introspection_c__ColorPoseStamped_message_type_support_handle = {
  0,
  &cube_msgs__msg__ColorPoseStamped__rosidl_typesupport_introspection_c__ColorPoseStamped_message_members,
  get_message_typesupport_handle_function,
  &cube_msgs__msg__ColorPoseStamped__get_type_hash,
  &cube_msgs__msg__ColorPoseStamped__get_type_description,
  &cube_msgs__msg__ColorPoseStamped__get_type_description_sources,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_cube_msgs
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, cube_msgs, msg, ColorPoseStamped)() {
  cube_msgs__msg__ColorPoseStamped__rosidl_typesupport_introspection_c__ColorPoseStamped_message_member_array[0].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, std_msgs, msg, Header)();
  cube_msgs__msg__ColorPoseStamped__rosidl_typesupport_introspection_c__ColorPoseStamped_message_member_array[1].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, geometry_msgs, msg, Pose)();
  if (!cube_msgs__msg__ColorPoseStamped__rosidl_typesupport_introspection_c__ColorPoseStamped_message_type_support_handle.typesupport_identifier) {
    cube_msgs__msg__ColorPoseStamped__rosidl_typesupport_introspection_c__ColorPoseStamped_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &cube_msgs__msg__ColorPoseStamped__rosidl_typesupport_introspection_c__ColorPoseStamped_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
